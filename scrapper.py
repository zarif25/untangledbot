import requests
from logger import log_error, log_warning, log_info
from bs4 import BeautifulSoup
from datetime import date, datetime
from urllib.parse import urlparse
from outer_source import get_source_link


def exception_handler(info_name):
    def outer(func):
        def inner(*args):
            info = None
            try:
                info = func(*args)
            except Exception as e:
                log_error(f"problem in {info_name}", e)
            return info
        return inner
    return outer


class Story():
    def __init__(self, url, netloc):
        log_info("INITIALIZING STORY", url)
        self.url = url
        self.netloc = netloc
        self.hash = self.__get_hash(url)

    def __get_hash(self, url):
        if self.netloc in ['bdnews24.com', 'www.dhakatribune.com']:
            url_parts = urlparse(url).path.split('/')
            hash = url_parts[-1]
            if not hash:
                hash = url_parts[-2]
            return hash
        else:
            # TODO: hash stories from other providers
            pass

    def scrape(self):
        log_info("SCRAPING", self.url)
        self.soup = BeautifulSoup(requests.get(self.url).text, 'lxml')
        if self.netloc == 'www.dhakatribune.com':
            self.soup = self.soup.find(class_="report-mainhead")
        self.title = self.__get_title()
        self.description = self.__get_description()
        self.src = self.__get_src()
        self.date = self.__get_date()
        self.img = self.__get_img()
        self.src_link = self.__get_src_link()

    def is_valid(self):
        return None in [
            self.title,
            self.description,
            self.src,
            self.date,
            self.src_link
        ]

    @exception_handler('title')
    def __get_title(self):
        if self.netloc == 'bdnews24.com':
            return self.soup.find(id='news-details-page').h1.text
        elif self.netloc == 'www.dhakatribune.com':
            return self.soup.h1.text

    @exception_handler('description')
    def __get_description(self):
        if self.netloc == 'bdnews24.com':
            return self.soup.find(class_='article_lead_text').h5.text
        elif self.netloc == 'www.dhakatribune.com':
            return self.soup.find(class_="highlighted-content").p.text

    @exception_handler('src')
    def __get_src(self):
        if self.netloc == 'bdnews24.com':
            src = self.soup.find(class_='byline').text
            src = (
                src
                .replace(">", "")
                .replace(",\n", ", ")
                .replace("\n", "")
                .strip()
            )
            if src == '':
                src = 'bdnews24.com'
        elif self.netloc == 'www.dhakatribune.com':
            src = self.soup.a.text.strip(" \n")
            outside_src = ['afp', 'bss', 'reuters',
                           'unb', 'new york times', 'washington']
            if src in ["Tribune Desk", "Showtime Desk", "Tribune Report", "Tribune Editorial"]:
                src = "Dhaka Tribune"
            elif not any([o_s in src.lower() for o_s in outside_src]):
                src += ", Dhaka Tribune"
        return src

    @exception_handler('date')
    def __get_date(self):
        if self.netloc == 'bdnews24.com':
            date_str = self.soup.find(class_='dateline').find_all('span')[
                1].text.split(':')[0][:-2].strip()
            date_format = '%d %b %Y'
        elif self.netloc == 'www.dhakatribune.com':
            date_str = self.soup.ul.li.text.strip('\n')[23:].split(',')
            date_str[0] = date_str[0][:-2]
            date_str = ''.join(date_str)
            date_format = '%B %d %Y'
        return datetime.strptime(
            date_str, date_format).strftime("%A, %b %d, %Y")

    @exception_handler('img')
    def __get_img(self):
        if self.netloc == 'bdnews24.com':
            img_url = self.soup.find(
                class_='gallery-image-box print-only').div.img['src']
        elif self.netloc == 'www.dhakatribune.com':
            img_url = self.soup.find(class_="reports-big-img").img['src']
            if img_url.endswith(".gif"):
                img_url = self.soup.find(id="gallery-grid").img['src']
        return requests.get(img_url, stream=True).raw

    @exception_handler('source link')
    def __get_src_link(self):
        if self.src == None:
            raise Exception("Source link cannot be generated without source")
        if self.src.endswith(('bdnews24.com', 'Dhaka Tribune')):
            return self.url
        else:
            return get_source_link(self.src, self.title)

    def get_all(self):
        return (
            self.title,
            self.description,
            self.src,
            self.date,
            self.img,
            self.src_link
        )


class Provider():

    prev_hashes = {'bdnews24.com': '',
                   'www.dhakatribune.com': ''}

    def __init__(self, url):
        self.url = url
        self.__netloc = urlparse(url).netloc
        log_info("INITIALIZING PROVIDER", self.__netloc)

    def get_latest_stories(self):
        """returns list of latest stories"""
        urls = self.__scrape_story_urls()
        stories = self.__urls_to_stories(urls)
        latest_stories = self.__get_latest_stories(stories)
        self.__update_prev_hash(latest_stories)
        return latest_stories

    def __scrape_story_urls(self):
        """returns urls to all stories in the recent section of the provider in ascending order of time"""
        log_info("SCRAPING", self.__netloc)
        soup = BeautifulSoup(requests.get(self.url).text, 'lxml')
        try:
            if self.__netloc == 'bdnews24.com':
                a_tags = soup.find(id='homepagetabs-tabs-2-2').find_all('a')
                urls = [a_tag['href'] for a_tag in a_tags]
            elif self.__netloc == 'www.dhakatribune.com':
                h2_tags = soup.find(class_='just_in_news').find_all("h2")
                urls = ["https://www.dhakatribune.com"+h2_tag.a['href']
                        for h2_tag in h2_tags]
            else:
                raise Exception(
                    "you never taught me how to scrape this provider :(")
        except Exception as e:
            log_error("problem in recent stories", e)
        return urls

    def __urls_to_stories(self, urls):
        """returns a list of stories from a list of urls"""
        return [Story(url, self.__netloc) for url in urls]

    @staticmethod
    def __get_latest_hash(stories):
        """return the hash of first story if stories is not empty else none"""
        return stories[0].hash if stories else None

    def __get_prev_hash(self):
        """returns previous hash"""
        return Provider.prev_hashes[self.__netloc]

    def __update_prev_hash(self, stories):
        """finds the hash of the latest story and updates the previous hash"""
        latest_hash = self.__get_latest_hash(stories)
        if latest_hash:
            Provider.prev_hashes[self.__netloc] = latest_hash

    def __get_latest_stories(self, stories):
        """trims the stories that are already uploaded"""
        prev_hash = self.__get_prev_hash()
        latest_stories = []
        for story in stories:
            if story.hash == prev_hash:
                break
            latest_stories.append(story)
        return latest_stories
