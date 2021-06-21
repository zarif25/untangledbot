from bs4 import BeautifulSoup
import requests
from xml.sax import saxutils as su
from .similarity import text_similarity


def get_source_link(source: str, title: str):
    """
    Args:
        source: source of story
        title: title of story
    Finds the story in google news rss feed and return the link if the title and source matches.
    """
    res = requests.get(
        f"https://news.google.com/rss/search?q={title} {source}")
    soup = BeautifulSoup(su.unescape(res.text), 'lxml')
    try:
        first_item = soup.item
        link = first_item.a['href']
        rss_title = ''.join(first_item.title.text.split('-')[:-1]).strip()
        if text_similarity(title, rss_title) > 0.2:
            return link
        raise AttributeError("Source and title in rss feed didn't match")
    except AttributeError as e:
        print(f"{e}\n\tSource not found: {title} - {source}")
