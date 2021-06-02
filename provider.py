import requests
import re
from urllib.parse import urlparse
from logger import log_error, log_info, log_warning
from bs4 import BeautifulSoup
from datetime import date, datetime
from outer_source import get_source_link
from utils import similarity_between, exception_handler
from fb import post_to_fb
from imgbb import upload_to_imgbb
from story_image import StoryImage


class Story:
    def __init__(self, title, url=None, details=None, src=None, datetime=None, img_url=None):
        self.title = self.__clean_title(title)
        self.src = self.__clean_src(src)
        self.url = self.__get_url_if_does_not_exist(url)
        self.datetime = datetime
        self.date = self.__format_datetime(datetime)
        self.details = self.__clean_details(details)
        self.img = self.__get_img_from_url(img_url)

    def __eq__(self, other):
        return (self.url != None and self.url == other.url) or \
            similarity_between(self.title, other.title) > 0.7

    def __repr__(self):
        return f"Story: <{self.title}>"

    @exception_handler()
    def __save_story_image(self):
        StoryImage(self).save('temp')

    # debug
    @exception_handler()
    def save_story_image(self):
        return StoryImage(self).save('temp')

    @exception_handler()
    def __upload_to_imgbb(self):
        self.__save_story_image()
        path = upload_to_imgbb('temp.PNG')
        return path

    @exception_handler('upload to fb')
    def upload_to_fb(self):
        post_to_fb(
            self.__upload_to_imgbb(),
            self.title,
            self.details,
            self.url
        )

    @exception_handler()
    def is_complete(self) -> bool:
        return bool(self.title and self.details and self.src and self.date and self.url)

    @exception_handler()
    def __get_img_from_url(self, url: str) -> requests.Response:
        if url != None:
            return requests.get(url, stream=True).raw

    @exception_handler()
    def __get_url_if_does_not_exist(self, url):
        return url or get_source_link(self.src, self.title)

    @exception_handler()
    def __clean_details(self, details):
        if details != None:
            return details.strip()

    @exception_handler()
    def __format_datetime(self, datetime: datetime):
        if datetime != None:
            return datetime.strftime("%A, %b %d, %Y")

    @exception_handler()
    def __clean_src(self, src):
        if src != None:
            src = re.sub(" {2,}", " ", src).strip(',')
            return src.strip().encode("ascii", "ignore").decode('utf-8')

    @exception_handler()
    def __clean_title(self, title):
        return title.strip()


class Provider:
    def __init__(self, url):
        print("="*20)
        self.name = urlparse(url).netloc
        log_info("init", self.name)
        self.soup = BeautifulSoup(requests.get(url).text, 'lxml')

    def __get_story_or_none(self, soup, url):
        """
        Returns:
            a story if a all the properties of a story except url and image
            is successfully extracted, else None
        """
        log_info("extracting", url or f"Story from {self.name}")
        try:
            # title
            title = self.get_story_title(soup)
            if title == None:
                raise Exception("Title not found")

            # details
            details = self.get_story_detials(soup)
            if details == None:
                raise Exception("Details not found")

            # src
            src = self.get_story_src(soup)
            if details == None:
                raise Exception("Src not found")

            # date
            date = self.get_story_date(soup)
            if date == None:
                raise Exception("Date not found")

            # url
            url = self.get_story_url(soup, src, url)

            # img url
            img_url = self.get_story_img_url(soup)

            return Story(title=title, url=url, details=details, src=src, datetime=date, img_url=img_url)
        except Exception as e:
            log_error("while extracting", e)
            return

    def get_stories(self) -> list[Story]:
        """
        Returns:
            all recent complete(except image) stories
        """
        stories: list[Story] = []
        for soup, url in self.get_soup_and_url_of_stories():
            story_or_none = self.__get_story_or_none(soup, url)
            if story_or_none is not None:
                stories.append(story_or_none)
        return [story for story in stories if story.is_complete()]


class RSSProvider(Provider):
    def __init__(self, url):
        super().__init__(url)

    def get_soup_and_url_of_stories(self):
        return [(item, None) for item in self.soup.find_all('item')]

    @staticmethod
    def get_story_title(soup):
        return soup.title.text

    @staticmethod
    def get_story_detials(soup):
        return soup.description.text

    @staticmethod
    def get_story_src(soup):
        return soup.source.text

    @staticmethod
    def get_story_date(soup):
        date_str = soup.pubdate.text
        if date_str == None:
            return
        date_str = date_str.split(',')[1].strip()[:11]
        return datetime.strptime(date_str, '%d %b %Y')

    @staticmethod
    def get_story_url(soup, src=None, url=None):
        return soup.guid.text

    @staticmethod
    def get_story_img_url(soup):
        try:
            return soup.find('media:content')['url']
        except TypeError:
            return


class DStar(RSSProvider):
    def __init__(self):
        super().__init__('https://www.thedailystar.net/top-news/rss.xml')


class TBSNews(RSSProvider):
    def __init__(self):
        super().__init__('https://www.tbsnews.net/top-news/rss.xml')


class Bdnews24(Provider):
    def __init__(self):
        super().__init__('http://bdnews24.com/')

    def get_soup_and_url_of_stories(self):
        a_tags = self.soup.find(id='homepagetabs-tabs-2-2').find_all('a')
        urls = [a_tag['href'] for a_tag in a_tags]
        return [(BeautifulSoup(requests.get(url).text, 'lxml'), url) for url in urls]

    @staticmethod
    def get_story_title(soup):
        return soup.find(id='news-details-page').h1.text

    @staticmethod
    def get_story_detials(soup):
        return soup.find(class_='article_lead_text').h5.text

    @staticmethod
    def get_story_src(soup):
        src = soup.find(class_='byline').text
        if src == None:
            return
        src = (
            src
            .replace(">", "")
            .replace(",\n", ", ")
            .replace("\n", "")
            .strip()
        ) or 'bdnews24.com'
        return src

    @staticmethod
    def get_story_date(soup):
        date_str = soup.find(class_='dateline').find_all('span')[1]
        if date_str == None:
            return
        date_str = date_str.text.split(':')[0][:-2].strip()
        return datetime.strptime(date_str, '%d %b %Y')

    @staticmethod
    def get_story_url(soup, src, url):
        if src.endswith('bdnews24.com'):
            return url

    @staticmethod
    def get_story_img_url(soup):
        try:
            return soup.find(class_='gallery-image-box print-only').div.img['src']
        except TypeError:
            return


class DHKTribune(Provider):
    def __init__(self):
        super().__init__('https://www.dhakatribune.com/')

    def get_soup_and_url_of_stories(self):
        h2_tags = self.soup.find(class_='just_in_news').find_all("h2")
        urls = ["https://www.dhakatribune.com"+h2_tag.a['href']
                for h2_tag in h2_tags]
        return [(BeautifulSoup(requests.get(url).text, 'lxml').find(class_="report-mainhead"), url) for url in urls]

    @staticmethod
    def get_story_title(soup):
        return soup.h1.text

    @staticmethod
    def get_story_detials(soup):
        return soup.find(class_="highlighted-content").p.text

    @staticmethod
    def get_story_src(soup):
        src = soup.a.text.strip()
        if src == None:
            return
        src = src.strip(" \n,")
        outside_src = ['afp', 'bss', 'reuters', 'Scroll.in',
                       'unb', 'new york times', 'washington']
        if src in ["Tribune Desk", "Showtime Desk", "Tribune Report", "Tribune Editorial"]:
            src = "Dhaka Tribune"
        elif not any([o_s in src.lower() for o_s in outside_src]):
            src += ", Dhaka Tribune"
        return src

    @staticmethod
    def get_story_date(soup):
        date_str = soup.ul.li.text
        if date_str == None:
            return
        date_str = date_str.strip('\n')[23:].split(',')
        date_str[0] = date_str[0][:-2]
        date_str = ''.join(date_str)
        return datetime.strptime(date_str, '%B %d %Y')

    @staticmethod
    def get_story_url(soup, src, url):
        if src.endswith('Dhaka Tribune'):
            return url

    @staticmethod
    def get_story_img_url(soup):
        try:
            img_url = soup.find(class_="reports-big-img").img['src']
            if img_url.endswith(".gif"):
                img_url = soup.find(id="gallery-grid").img['src']
            return img_url
        except TypeError:
            return
