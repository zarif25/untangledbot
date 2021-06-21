from datetime import datetime

import requests
from bs4 import BeautifulSoup

from . import Provider, Story
from .utils.exception_handler import does_not_exist_check


class BnTribuneStory(Story):
    def __init__(self, soup, provider_name):
        self.name = soup.base_url
        self.__soup = soup
        self.__url = soup.base_url
        super().__init__(provider_name, lang='bn')

    @does_not_exist_check('title')
    def get_title(self):
        return self.__soup.h1.text.strip()

    @does_not_exist_check('summary')
    def get_summary(self):
        return self.__soup.article.p.text.strip()

    @does_not_exist_check('date')
    def get_dtime(self):
        date_str = self.__soup.find(class_='tts_time')['content'].split('T')[0]
        return datetime.strptime(date_str, "%Y-%m-%d")

    @does_not_exist_check('topic')
    def get_topic(self) -> str:
        return super().get_topic(
            self.__soup.find(class_='secondary_logo').a['href'].split('/')[1]
        )

    def get_source(self):
        return "বাংলা ট্রিবিউন"

    def get_base_url(self):
        return self.__url

    @does_not_exist_check('image url')
    def get_img_url(self):
        return "https:"+self.__soup.find(class_="featured_image").img['src'].strip()


class BnTribune(Provider):
    def __init__(self) -> None:
        super().__init__(
            url='https://www.banglatribune.com/archive/',
            story_class=BnTribuneStory,
            name="বাংলা ট্রিবিউন"
        )

    def get_story_soups(self) -> Story:
        # get soup of main page
        soup = BeautifulSoup(requests.get(self.url).text,
                             'lxml').find(class_='summery_view')

        # get urls recent stories
        a_tags = soup.find_all('a')
        urls = ["https:"+a_tag['href']
                for a_tag in a_tags if 'link_overlay' in a_tag.attrs['class']][:10]

        soups = []
        for url in urls:
            soup = BeautifulSoup(requests.get(url).text, 'lxml')
            soup.base_url = url
            soups.append(soup)

        return soups
