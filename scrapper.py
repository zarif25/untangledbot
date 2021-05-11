import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse


class Story():
    def __init__(self, url, netloc):
        print(f"Initializing Story: {url}")
        self.url = url
        self.netloc = netloc
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')
        self.title = self.get_title()
        self.description = self.get_description()
        self.src = self.get_src()
        self.date = self.get_date()
        self.img = self.get_img()

    def get_title(self):
        try:
            if self.netloc == 'bdnews24.com':
                return self.soup.find(id='news-details-page').h1.text
            else:
                raise Exception(f"ERROR you never taught me how to scrape {self.url} :(")
        except Exception as e:
            print(f"ERROR something seems wrong with the title in {self.url} |", e)

    def get_description(self):
        try:
            if self.netloc == 'bdnews24.com':
                return self.soup.find(class_='article_lead_text').h5.text
            else:
                raise Exception(f"ERROR you never taught me how to scrape {self.url} :(")
        except Exception as e:
            print(f"ERROR something seems wrong with the description in {self.url} |", e)

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
                raise Exception(f"ERROR you never taught me how to scrape {self.url} :(")
        except Exception as e:
            print(f"ERROR something seems wrong with the source in {self.url} |", e)

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
                raise Exception(f"ERROR you never taught me how to scrape {self.url} :(")
        except Exception as e:
            print(f"ERROR something seems wrong with the date in {self.url} |", e)

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
                raise Exception(f"ERROR you never taught me how to scrape {self.url} :(")
        except Exception as e:
            print(f"ERROR something seems wrong with the image in {self.url} |", e)

    def get_all(self):
        return (
            self.title,
            self.description,
            self.src,
            self.date,
            self.img
        )


class Provider():
    def __init__(self, url):
        print(f"Initializing Provider: {url}")
        self.url = url
        self.netloc = urlparse(url).netloc
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')

    def scrape_stories(self):
        try:
            if self.netloc == 'bdnews24.com':
                a_tags = self.soup.find(id='homepagetabs-tabs-2-2').find_all('a')
                urls = [a_tag['href'] for a_tag in a_tags]
                return [Story(url, self.netloc) for url in urls if not url.startswith('https://opinion')]
            else:
                raise Exception(f"ERROR you never taught me how to scrape {self.url} :(")
        except Exception as e:
            print(f"ERROR something seems wrong with the recent stories in {self.url} |", e)
        return []
