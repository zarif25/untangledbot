import requests
from logger import log_error, log_warning, log_info
from bs4 import BeautifulSoup
from datetime import date, datetime
from urllib.parse import urlparse
from news_hash import url_to_hash


previous_hashes = {
    'bdnews24.com': "",
    'www.dhakatribune.com': ""
}

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
        try:
            if self.netloc == 'bdnews24.com':
                return self.soup.find(id='news-details-page').h1.text
            elif self.netloc == 'www.dhakatribune.com':
                return self.soup.h1.text
        except Exception as e:
            log_error("problem in title", e)

    def __get_description(self):
        try:
            if self.netloc == 'bdnews24.com':
                return self.soup.find(class_='article_lead_text').h5.text
            elif self.netloc == 'www.dhakatribune.com':
                return self.soup.find(class_="highlighted-content").p.text
        except Exception as e:
            log_error("problem in description", e)

    def __get_src(self):
        try:
            if self.netloc == 'bdnews24.com':
                src = self.soup.find(class_='authorName')
                if not (src and src.text):
                    src = self.soup.find(id='article_notations').p.text
                else:
                    src = src.text
                src = src.strip(' >')
                if src == '':
                    src = 'bdnews24.com'
            elif self.netloc == 'www.dhakatribune.com':
                src = self.soup.a.text.strip('\n')
            
            if src in ["Tribune Desk", "Showtime Desk", "Tribune Report"]:
                src = "Dhaka Tribune"
            elif src in ["Salma Nasreen"]:
                src += ", Dhaka Tribune"
            return src
        except Exception as e:
            log_error("problem in source", e)

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
            return requests.get(img,stream=True).raw
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
        self.netloc = urlparse(url).netloc
        log_info("INITIALIZING PROVIDER", self.netloc)
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')

    def scrape_latest_stories(self):
        log_info("SCRAPING", self.netloc)
        stories = []
        try:
            if self.netloc == 'bdnews24.com':
                a_tags = self.soup.find(id='homepagetabs-tabs-2-2').find_all('a')
                urls = [a_tag['href'] for a_tag in a_tags]
                latest_hash = url_to_hash(urls[0])
                log_info('latest hash in bdnews24', latest_hash)
                previous_hash = previous_hashes[self.netloc]
                log_info('previous hash in bdnews24', previous_hash)
                for url in urls:
                    if url_to_hash(url) == previous_hash:
                        break
                    if not url.startswith('https://opinion'):
                        stories.append(Story(url, self.netloc))
                previous_hashes[self.netloc] = latest_hash
            elif self.netloc == 'www.dhakatribune.com':
                h2_tags = self.soup.find(class_='just_in_news').find_all("h2")
                urls = ["https://www.dhakatribune.com"+h2_tag.a['href'] for h2_tag in h2_tags]
                latest_hash = url_to_hash(urls[0])
                log_info('latest hash in dhktribune', latest_hash)
                previous_hash = previous_hashes[self.netloc]
                log_info('previous hash in dhktribune', previous_hash)
                for url in urls:
                    if url_to_hash(url) == previous_hash:
                        break
                    stories.append(Story(url, self.netloc))
                previous_hashes[self.netloc] = latest_hash
            else:
                raise Exception("you never taught me how to scrape this provider :(")
        except Exception as e:
            log_error("problem in recent stories", e)
        return stories  # TODO: what happens when this is returned?