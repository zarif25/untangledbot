import requests
from logger import log_error, log_warning, log_info
from bs4 import BeautifulSoup
from datetime import date, datetime
from urllib.parse import urlparse
from news_hash import url_to_hash, previous_hashes


class Story():
    def __init__(self, url, netloc):
        log_info("INITIALIZING STORY", url)
        self.url = url
        self.netloc = netloc
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')
        if self.netloc == 'www.dhakatribune.com':
            self.soup = self.soup.find(class_="report-mainhead")

    def scrape(self):
        log_info("SCRAPING", self.url)
        self.title = self.__get_title()
        self.description = self.__get_description()
        self.src = self.__get_src()
        self.date = self.__get_date()
        self.img = self.__get_img()
        self.src_link = self.__get_src_link()

    def __get_title(self):
        title = None
        try:
            if self.netloc == 'bdnews24.com':
                title = self.soup.find(id='news-details-page').h1.text
            elif self.netloc == 'www.dhakatribune.com':
                title = self.soup.h1.text
        except Exception as e:
            log_error("problem in title", e)
        return title

    def __get_description(self):
        description = None
        try:
            if self.netloc == 'bdnews24.com':
                description = self.soup.find(
                    class_='article_lead_text').h5.text
            elif self.netloc == 'www.dhakatribune.com':
                description = self.soup.find(
                    class_="highlighted-content").p.text
        except Exception as e:
            log_error("problem in description", e)
        return description

    def __get_src(self):
        src = None
        try:
            if self.netloc == 'bdnews24.com':
                src = self.soup.find(class_='authorName')
                if not (src and src.text):
                    src = self.soup.find(id='article_notations').p.text
                else:
                    src = src.text
                src = src.strip(' >\n')
                if src == '':
                    src = 'bdnews24.com'
                src = src.split('>')[-1].split('\n')[-1].strip(" >\n")
            elif self.netloc == 'www.dhakatribune.com':
                src = self.soup.a.text.strip(" \n")
                outside_src = ['afp', 'bss', 'reuters',
                               'unb', 'new york times', 'washington']

                if src in ["Tribune Desk", "Showtime Desk", "Tribune Report", "Tribune Editorial"]:
                    src = "Dhaka Tribune"
                elif not any([o_s in src.lower() for o_s in outside_src]):
                    src += ", Dhaka Tribune"
        except Exception as e:
            log_error("problem in source", e)
        return src

    def __get_date(self):
        try:
            if self.netloc == 'bdnews24.com':
                return datetime.strptime(
                    self.soup
                    .find(class_='dateline')
                    .find_all('span')[1]
                    .text
                    .split(':')[0][:-2]
                    .strip(),
                    '%d %b %Y'
                ).strftime("%A, %b %d, %Y")
            elif self.netloc == 'www.dhakatribune.com':
                date_str = self.soup.ul.li.text.strip('\n')[23:].split(',')
                date_str[0] = date_str[0][:-2]
                date_str = ''.join(date_str)
                return datetime.strptime(
                    date_str,
                    "%B %d %Y"
                ).strftime("%A, %b %d, %Y")
        except Exception as e:
            log_error("problem in date", e)

    def __get_img(self):
        try:
            if self.netloc == 'bdnews24.com':
                img = self.soup.find(
                    class_='gallery-image-box print-only').div.img['src']
            elif self.netloc == 'www.dhakatribune.com':
                img = self.soup.find(class_="reports-big-img").img['src']
                if img.endswith(".gif"):
                    img = self.soup.find(id="gallery-grid").img['src']
            return requests.get(img, stream=True).raw
        except Exception as e:
            log_warning("problem in image", e)

    def __get_src_link(self):
        if self.src != None and self.src.endswith(('bdnews24.com', 'Dhaka Tribune')):
            return self.url

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
    def __init__(self, url):
        self.url = url
        self.__netloc = urlparse(url).netloc
        log_info("INITIALIZING PROVIDER", self.__netloc)

    def get_latest_stories(self):
        """returns list of latest stories"""
        latest_urls = self.__get_latest_urls(self.__scrape_story_urls())
        self.__update_prev_hash(latest_urls)
        return self.__urls_to_stories(latest_urls)

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
                urls = ["https://www.dhakatribune.com"+h2_tag.a['href'] for h2_tag in h2_tags]
            else:
                raise Exception("you never taught me how to scrape this provider :(")
        except Exception as e:
            log_error("problem in recent stories", e)
        return urls

    def __get_latest_hash(self, urls):
        """return the hash of first url if urls is not empty else none"""
        if urls:
            latest_hash = url_to_hash(urls[0])
            log_info('latest hash in bdnews24', latest_hash)
            return latest_hash
        return None

    def __get_prev_hash(self):
        """returns previous hash"""
        previous_hash = previous_hashes[self.__netloc]
        log_info('previous hash in bdnews24', previous_hash)
        return previous_hash

    def __update_prev_hash(self, urls):
        """finds the hash of the url of the latest story and updates the previous hash"""
        latest_hash = self.__get_latest_hash(urls)
        if latest_hash:
            previous_hashes[self.__netloc] = latest_hash

    def __get_latest_urls(self, urls):
        """trims the urls that are already uploaded"""
        prev_hash = self.__get_prev_hash()
        latest_urls = []
        for url in urls:
            if url_to_hash(url) == prev_hash:
                break
            latest_urls.append(url)
        return latest_urls
    
    def __urls_to_stories(self, urls):
        """returns a list of stories from a list of urls"""
        return [Story(url, self.__netloc) for url in urls]