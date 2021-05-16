from difflib import SequenceMatcher
from bs4 import BeautifulSoup
import requests
from xml.sax import saxutils as su
from urllib.parse import quote


def match_accuracy(hash, title):
    return SequenceMatcher(None, hash, title).ratio()


def get_source_link(src, title):
    src = src.split(',')[-1]
    query = quote(title + " " + src)
    res = requests.get(f"https://news.google.com/rss/search?q={query}+when:1d")
    soup = BeautifulSoup(su.unescape(res.text), 'lxml')
    try:
        first_a_tag = soup.item.a
    except Exception as e:
        raise Exception("Problem parsing rss feed", e)
    rss_title = first_a_tag.text
    print(
        f"\nRSS TITLE: {rss_title}\nTITLE: {title}\n{match_accuracy(title, rss_title)}\n")
    rss_url = first_a_tag['href']
    if match_accuracy(title, rss_title) > 0.70:
        return rss_url
