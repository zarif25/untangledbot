import requests
from logger import log_error, log_warning, log_info
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse



class Story():
    def __init__(self, url, netloc):
        log_info("INITIALIZING STORY", url)
        self.url = url
        self.netloc = netloc
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')

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
        except Exception as e:
            log_error("problem in title", e)

    def __get_description(self):
        try:
            if self.netloc == 'bdnews24.com':
                return self.soup.find(class_='article_lead_text').h5.text
        except Exception as e:
            log_error("problem in description", e)

    def __get_src(self):
        try:
            if self.netloc == 'bdnews24.com':
                src = self.soup.find(class_='authorName')
                if not (src and src.text):
                    src = self.soup.find(
                        id='article_notations').p.text.split(', ')[-1].strip()
                else:
                    src = src.text
                src = src.strip(' >')
                if src == '':
                    src = 'bdnews24.com'
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
        except Exception as e:
            log_error("problem in date", e)

    def __get_img(self):
        try:
            if self.netloc == 'bdnews24.com':
                return requests.get(
                    self.soup
                    .find(class_='gallery-image-box print-only')
                    .div
                    .img['src'],
                    stream=True
                ).raw
        except Exception as e:
            log_warning("problem in image", e)

    def __get_src_link(self):
        if self.netloc == 'bdnews24.com':
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

    def scrape_stories(self):
        log_info("SCRAPING", self.netloc)
        try:
            if self.netloc == 'bdnews24.com':
                a_tags = self.soup.find(
                    id='homepagetabs-tabs-2-2').find_all('a')
                urls = [a_tag['href'] for a_tag in a_tags]
                return [Story(url, self.netloc) for url in urls if not url.startswith('https://opinion')]
            else:
                raise Exception(
                    "you never taught me how to scrape this provider :(")
        except Exception as e:
            log_error("problem in recent stories", e)
        return [] #TODO: what happens when this is returned?
