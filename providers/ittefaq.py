import requests
from bs4 import BeautifulSoup

from . import Provider, Story
from .utils.bn2en import to_en_datetime
from .utils.exception_handler import does_not_exist_check


class IttefaqStory(Story):
    def __init__(self, soup, provider_name):
        self.name = soup.base_url
        self.__url = soup.base_url
        self.__soup = soup
        super().__init__(provider_name, lang='bn')

    @does_not_exist_check('title')
    def get_title(self):
        return self.__soup.find(id='dtl_hl_block').h1.text.strip()

    @does_not_exist_check('summary')
    def get_summary(self):
        return self.__soup.find(id='dtl_content_block').strong.text.strip()

    @does_not_exist_check('date')
    def get_dtime(self):
        date_str = self.__soup.find(
            class_='post_date_time').find_all('span')[1]
        date_str = ','.join(date_str.text.split(',')[1:]).strip()
        return to_en_datetime(date_str)

    @does_not_exist_check('source')
    def get_source(self):
        return "ইত্তেফাক"

    def get_base_url(self):
        return self.__url

    @does_not_exist_check('image url')
    def get_img_url(self):
        return "https://www.ittefaq.com.bd" + self.__soup.find(id="dtl_img_block").img['src'].strip()


class Ittefaq(Provider):
    def __init__(self) -> None:
        super().__init__(
            url='https://www.ittefaq.com.bd/',
            story_class=IttefaqStory,
            name="ইত্তেফাক"
        )

    def get_story_soups(self) -> Story:
        # get soup of main page
        soup = BeautifulSoup(requests.get(self.url).text,
                             'lxml').find(class_='latest-news')

        # get urls recent stories
        a_tags = soup.find_all('a')
        urls = [a_tag['href'] for a_tag in a_tags]

        soups = []
        for url in urls:
            soup = BeautifulSoup(requests.get(url).text,
                                 'lxml').find(class_='body-content')
            soup.base_url = url
            soups.append(soup)

        return soups
