from datetime import datetime

import requests
from bs4 import BeautifulSoup
from discord_webhook import log_info_to_discord

from providers.utils.constants import SOURCE_MAPPING

from . import Provider, Story
from .utils.exception_handler import does_not_exist_check


class DHKTribuneStory(Story):
    def __init__(self, soup, provider_name):
        self.name = soup.base_url
        self.__soup = soup
        self.__url = soup.base_url
        super().__init__(provider_name)

    @does_not_exist_check('title')
    def get_title(self):
        return self.__soup.h1.text.strip()

    @does_not_exist_check('summary')
    def get_summary(self):
        return self.__soup.find(class_="highlighted-content").p.text.strip()

    @does_not_exist_check('date')
    def get_dtime(self):
        date_str = self.__soup.ul.li.text
        date_str = date_str.strip('\n')[23:].split(',')
        date_str[0] = date_str[0][:-2]
        date_str = ''.join(date_str).strip()
        return datetime.strptime(date_str, '%B %d %Y')

    @does_not_exist_check('source')
    def get_source(self):
        source = (
            self.__soup.a.text
            .strip()
            .strip(" \n,")
        )
        for key, value in SOURCE_MAPPING.items():
            if key in source.lower():
                return value
        log_info_to_discord(
            f"Found an unknow source in {self.provider_name}: {source}\nSo, I used '{self.provider_name}' as source instead.\n"
            "You may add this source to providers/utils/constants.py file in the next version .")
        return self.provider_name

    def get_base_url(self):
        return self.__url

    @does_not_exist_check('image url')
    def get_img_url(self):
        img_url = self.__soup.find(class_="reports-big-img").img['src']
        if img_url.endswith(".gif"):
            img_url = self.__soup.find(id="gallery-grid").img['src']
        return img_url


class DHKTribune(Provider):
    def __init__(self) -> None:
        super().__init__(
            url='https://www.dhakatribune.com/',
            story_class=DHKTribuneStory,
            name="Dhaka Tribune"
        )

    def get_story_soups(self) -> Story:
        # get soup of main page
        soup = BeautifulSoup(requests.get(self.url).text, 'lxml')

        # get urls recent stories
        h2_tags = soup.find(class_='just_in_news').find_all("h2")
        urls = ["https://www.dhakatribune.com"+h2_tag.a['href']
                for h2_tag in h2_tags]

        soups = []
        for url in urls:
            soup = BeautifulSoup(requests.get(url).text, 'lxml').find(
                class_="report-mainhead")
            soup.base_url = url
            soups.append(soup)
        return soups
