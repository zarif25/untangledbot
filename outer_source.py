from utils import similarity_between
from bs4 import BeautifulSoup
import requests
from xml.sax import saxutils as su


def get_source_link(src, title):
    # FIXME: [ERROR] problem in get_url_if_does_not_exist ('Problem parsing rss feed', AttributeError("'NoneType' object has no attribute 'a'"))
    if src == None:
        return None
    src = src.split(',')[-1].strip()
    res = requests.get(f"https://news.google.com/rss/search?q={title} {src}")
    soup = BeautifulSoup(su.unescape(res.text), 'lxml')
    try:
        first_a_tag = soup.item.a
    except Exception as e:
        raise Exception("Problem parsing rss feed", e)
    rss_title = first_a_tag.text
    rss_url = first_a_tag['href']
    if similarity_between(title, rss_title) > 0.7:
        return rss_url
