from datetime import datetime
from discord_webhook import log_error_to_discord
from providers.utils.similarity import text_similarity
from providers.utils.outer_source import get_source_link

import requests
from bs4 import BeautifulSoup

from providers.utils.exception_handler import StoryExtractionError, does_not_exist_check

from .utils import remove_symbols, to_pascal, to_untangled_topic_or_none, truncate, to_topic_or_none


class Story:

    def __init__(self, provider_name: str, lang: str = 'en'
    ):
        self.provider_name = provider_name
        self.title = self.get_title()
        self.summary = self.get_summary()
        self.dtime = self.get_dtime()
        self.topic = self.get_topic()
        self.source = self.get_source()
        self.base_url = self.get_base_url()
        self.display_url = self.get_display_url()
        self.img_url = self.get_img_url()
        self.lang = lang

    def is_complete(self):
        return (
            self.title and
            self.source and
            self.base_url and
            self.display_url and
            self.dtime and
            self.summary and
            self.img_url and
            self.topic
        )

    def get_title(self) -> str:
        """
        Returns:
            The title of the story
        """
        raise NotImplementedError

    def get_summary(self) -> str:
        """
        Returns:
            The summary of the story
        """
        raise NotImplementedError

    def get_dtime(self) -> datetime:
        """
        Returns:
            The datetime of the story
        """
        raise NotImplementedError

    def get_topic(self, *args) -> str:
        """
        Returns:
            The topic of the story or None
        """
        if args:
            extracted_topic = args[0]
            topic = to_untangled_topic_or_none(extracted_topic)
            # <testing>
            if topic == None:
                log_error_to_discord(f"Unknown topic extracted: {extracted_topic}. Url: banglatribune.com")
            # </testing>
            return topic
        base_url = self.get_base_url()
        extracted_topic = to_topic_or_none(base_url)
        topic = to_untangled_topic_or_none(extracted_topic)
        # <testing>
        if topic == None:
            log_error_to_discord(f"Unknown topic extracted: {extracted_topic}. Url: {base_url}")
        # </testing>

        if topic == 'ignore':
            display_url = self.get_display_url()
            if base_url == display_url:
                return None
            extracted_topic = to_topic_or_none(display_url)
            topic = to_untangled_topic_or_none(extracted_topic)
            # <testing>
            if topic == None:
                log_error_to_discord(f"Unknown topic extracted: {extracted_topic}. Url: {display_url}")
            # </testing>
        return topic

    def get_source(self) -> str:
        """
        Returns:
            The source of the story
        """
        raise NotImplementedError

    def get_base_url(self) -> str:
        """
        Returns:
            The url of the story from scraped provider
        """
        raise NotImplementedError

    def get_display_url(self) -> str:
        """
        Returns:
            The url of the story from original provider
        """
        source = self.get_source()
        if self.provider_name == source:
            return self.get_base_url()
        else:
            title = self.get_title()
            return get_source_link(source, title)

    def get_img_url(self) -> str:
        """
        Returns:
            The url of the image of the story
        """
        raise NotImplementedError

    def is_exactly_same(self, other) -> bool:
        return self.base_url == other.base_url

    def __eq__(self, other):
        # FIXME Sakib
        if self.provider_name == other.provider_name:
            return False
        if self.display_url in [other.display_url, other.base_url] or self.base_url in [other.display_url, other.base_url]:
            return True
        title_similarity = text_similarity(self.title, other.title)
        if title_similarity > 0.3:
            return True
        summary_similarity = text_similarity(self.summary, other.summary)
        if summary_similarity > 0.3:
            return True
        return False

    def __repr__(self):
        short_title = truncate(to_pascal(remove_symbols(self.title)), 20)
        return f"<Story: {short_title}>"


class Provider:
    def __init__(self, url: str, story_class: Story, name: str):
        self.url = url
        self.name = name
        self.story_class = story_class

    def __repr__(self):
        return f"<Provider: {self.name}>"

    def get_story_soups(self) -> list[BeautifulSoup]:
        raise NotImplementedError

    def get_stories(self) -> list[Story]:
        """
        Returns:
            A list of latest stories
        """
        soups = self.get_story_soups()

        stories: list[Story] = []
        for soup in soups:
            try:
                story = self.story_class(soup, self.name)
                stories.append(story)
            except StoryExtractionError as e:
                print(e)
        return stories


class RssStory(Story):
    def __init__(self, soup, provider_name, lang='en'):
        self.__soup = soup
        self.name = self.get_base_url()
        super().__init__(provider_name, lang=lang)

    @does_not_exist_check('title')
    def get_title(self):
        return self.__soup.title.text.strip()

    @does_not_exist_check('summary')
    def get_summary(self):
        return self.__soup.description.text.strip()

    @does_not_exist_check('date')
    def get_dtime(self):
        date_str = self.__soup.pubdate.text.strip()
        if date_str == None:
            return
        date_str = date_str.split(',')[1].strip()[:11]
        return datetime.strptime(date_str, '%d %b %Y')

    @does_not_exist_check('source')
    def get_source(self):
        return self.__soup.source.text.strip()

    @does_not_exist_check('base url')
    def get_base_url(self):
        return self.__soup.guid.text.strip()

    @does_not_exist_check('image url')
    def get_img_url(self):
        return self.__soup.find('media:content')['url']


class RssProvider(Provider):
    def __init__(self, url, name) -> None:
        super().__init__(url, RssStory, name)

    def get_story_soups(self):
        soup = BeautifulSoup(requests.get(self.url).text, 'lxml')
        return soup.find_all('item')
