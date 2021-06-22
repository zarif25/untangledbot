from datetime import datetime
from discord_webhook import log_error_to_discord
from providers.utils.constants import SOURCE_MAPPING

import requests
from bs4 import BeautifulSoup

from . import Provider, Story
from .utils.exception_handler import does_not_exist_check


class Bdnews24Story(Story):
    def __init__(self, soup, provider_name):
        self.name = soup.base_url
        self.__soup = soup
        super().__init__(provider_name)

    @does_not_exist_check('title')
    def get_title(self):
        return self.__soup.find(id='news-details-page').h1.text.strip()

    @does_not_exist_check('summary')
    def get_summary(self):
        return self.__soup.find(class_='article_lead_text').h5.text.strip()

    @does_not_exist_check('date')
    def get_dtime(self):
        date_str = self.__soup.find(class_='dateline').find_all('span')[1]
        date_str = date_str.text.split(':')[0][:-2].strip()
        return datetime.strptime(date_str, '%d %b %Y')

    @does_not_exist_check('source')
    def get_source(self):
        source = self.__soup.find(class_='byline').text.strip()
        for key, value in SOURCE_MAPPING.items():
            if key in source.lower():
                return value
        log_error_to_discord(
            f"Found an unknow source in {self.provider_name}: {source}\n"
            f"So, I used '{self.provider_name}' as source instead.\n"
            "You should add this source to providers/utils/constants.py file in the next version.")
        return self.provider_name

    def get_base_url(self):
        return self.__soup.base_url

    @does_not_exist_check('image url')
    def get_img_url(self):
        return self.__soup.find(class_='gallery-image-box print-only').div.img['src']


class Bdnews24(Provider):
    def __init__(self) -> None:
        super().__init__(
            url='http://bdnews24.com/',
            story_class=Bdnews24Story,
            name="bdnews24"
        )

    def get_story_soups(self):
        # get soup of main page
        soup = BeautifulSoup(requests.get(self.url).text, 'lxml')

        # get urls recent stories
        a_tags = soup.find(id='homepagetabs-tabs-2-2').find_all('a')
        urls = [a_tag['href'] for a_tag in a_tags]

        soups = []
        for url in urls:
            soup = BeautifulSoup(requests.get(url).text, 'lxml')
            soup.base_url = url
            soups.append(soup)

        return soups
