import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)

class Story():
    def __init__(self, url, netloc):
        logging.info(f"INITIALIZING STORY: {url}")
        self.url = url
        self.netloc = netloc
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')

    def get_title(self):
        try:
            if self.netloc == 'bdnews24.com':
                return self.soup.find(id='news-details-page').h1.text
            else:
                raise Exception(f"ERROR: you never taught me how to scrape this provider :(")
        except Exception as e:
            logging.error(f"something seems wrong with the title in this story | {e}")

    def get_description(self):
        try:
            if self.netloc == 'bdnews24.com':
                return self.soup.find(class_='article_lead_text').h5.text
            else:
                raise Exception("you never taught me how to scrape this provider :(")
        except Exception as e:
            logging.error(f"something seems wrong with the description in this story | {e}")

    def get_src(self):
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
            else:
                raise Exception("you never taught me how to scrape this provider :(")
        except Exception as e:
            logging.error(f"something seems wrong with the source in this story | {e}")

    def get_date(self):
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
            else:
                raise Exception("you never taught me how to scrape this provider :(")
        except Exception as e:
            logging.error(f"something seems wrong with the date in this story | {e}")

    def get_img(self):
        try:
            if self.netloc == 'bdnews24.com':
                return requests.get(
                    self.soup
                    .find(class_='gallery-image-box print-only')
                    .div
                    .img['src'],
                    stream=True
                ).raw
            else:
                raise Exception("you never taught me how to scrape this provider :(")
        except Exception as e:
            logging.error(f"something seems wrong with the image in this story | {e}")

    def get_all(self):
        logging.info(f"SCRAPING: {self.url}")
        return (
            self.get_title(),
            self.get_description(),
            self.get_src(),
            self.get_date(),
            self.get_img(),
        )


class Provider():
    def __init__(self, url):
        self.netloc = urlparse(url).netloc
        logging.info(f"INITIALIZING PROVIDER: {self.netloc}")
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')

    def scrape_stories(self):
        logging.info(f"SCRAPING: {self.netloc}")
        try:
            if self.netloc == 'bdnews24.com':
                a_tags = self.soup.find(id='homepagetabs-tabs-2-2').find_all('a')
                urls = [a_tag['href'] for a_tag in a_tags]
                return [Story(url, self.netloc) for url in urls if not url.startswith('https://opinion')]
            else:
                raise Exception("you never taught me how to scrape this provider :(")
        except Exception as e:
            logging.error(f"something seems wrong with the recent stories in this provider | {e}")
        return []
