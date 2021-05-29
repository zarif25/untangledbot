from time import localtime
from difflib import SequenceMatcher

def get_theme():
    t_hour = (localtime().tm_hour + 6) % 24
    return 'light' if 3 <= t_hour <= 18 else 'dark'

def similarity_between(hash, title):
    return round(SequenceMatcher(None, hash, title).ratio(), 2)