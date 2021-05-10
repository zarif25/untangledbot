import requests
from bs4 import BeautifulSoup
from datetime import datetime


class Story():
    def __init__(self, url):
        print(f"Initializing Story: {url}")
        self.url = url
        self.soup = BeautifulSoup(
            requests
            .get(url)
            .text,
            'lxml'
        )

    def get_title(self):
        return self.soup.find(id='news-details-page').h1.text

    def get_sub_title(self):
        return self.soup.find(class_='article_lead_text').h5.text

    def get_src(self):
        src = self.soup.find(class_='authorName')
        if not (src and src.text):
            src = self.soup.find(id='article_notations').p.text.split(', ')[-1].strip()
        else:
            src = src.text
        src = src.strip(' >')
        if src == '':
            src = 'bdnews24.com'
        return src

    def get_date(self):
        return datetime.strptime(
            self.soup
            .find(class_='dateline')
            .find_all('span')[1]
            .text
            .split(':')[0][:-2]
            .strip(),
            '%d %b %Y'
        ).strftime("%A, %b %d, %Y")

    def get_img(self):
        return requests.get(
            self.soup
            .find(class_='gallery-image-box print-only')
            .div
            .img['src'],
            stream=True
        ).raw

    def get_all(self):
        return (
            self.get_title(),
            self.get_sub_title(),
            self.get_src(),
            self.get_date(),
            self.get_img()
        )


class Provider():
    def __init__(self, url):
        print(f"Initializing Provider: {url}")
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')

    def scrape_stories(self):
        return [Story(url['href']) for url in self.soup.find(id='homepagetabs-tabs-2-2').find_all('a') if not url['href'].startswith('https://opinion')]
