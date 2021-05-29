from utils import similarity_between
from bs4 import BeautifulSoup
import requests
from xml.sax import saxutils as su
from logger import log_info


def get_source_link(src, title):
    src = src.split(',')[-1].strip()
    res = requests.get(f"https://news.google.com/rss/search?q={title} {src}")
    soup = BeautifulSoup(su.unescape(res.text), 'lxml')
    try:
        first_a_tag = soup.item.a
    except Exception as e:
        raise Exception("Problem parsing rss feed", e)
    rss_title = first_a_tag.text
    log_info("RSS TITLE", rss_title)
    log_info("TITLE", title)
    log_info("match accuracy", similarity_between(title, rss_title))
    rss_url = first_a_tag['href']
    if similarity_between(title, rss_title) > 0.70:
        return rss_url
