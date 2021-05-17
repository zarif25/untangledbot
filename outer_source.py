from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import requests
from xml.sax import saxutils as su
# from urllib.parse import quote
from logger import log_info


def match_accuracy(hash, title):
    return SequenceMatcher(None, hash, title).ratio()


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
    log_info("TITLE", {title})
    log_info("match accuracy", match_accuracy(title, rss_title))
    rss_url = first_a_tag['href']
    if match_accuracy(title, rss_title) > 0.70:
        return rss_url
