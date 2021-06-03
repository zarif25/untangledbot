import logging
import re
import time
from difflib import SequenceMatcher

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.INFO)


def similarity_between(text1: str, text2: str):
    common_words = ["a", "all", "also", "an", "and", "any", "as", "at", "be", "but", "by", "can", "could", "do", "for", "from", "get", "have", "he", "her", "him", "his", "how", "if", "in", "into", "it", "its", "it's",
                    "my", "no", "not", "of", "on", "or", "she", "so", "than", "that", "the", "their", "them", "then", "there", "these", "they", "this", "to", "we",  "what", "when", "which", "who", "will", "with", "would", "you", "your"]
    text1 = text1.lower()
    text2 = text2.lower()
    for word in common_words:
        text1 = text1.replace(f" {word} ", " ")
        text2 = text2.replace(f" {word} ", " ")
    return round(SequenceMatcher(None, text1, text2).ratio(), 2)


def exception_handler(info_name=None):
    def outer(func):
        def inner(*args):
            info = None
            try:
                info = func(*args)
            except Exception as e:
                logging.error(
                    f"problem in {info_name or func.__name__.strip('_')} {e}")
            return info
        return inner
    return outer


def truncate(text: str, max_char: int) -> str:
    return (text[:max_char-2]+'..') if len(text) > max_char else text


def to_pascal(text: str) -> str:
    return text.title().replace(' ', '')


def remove_symbols(text: str) -> str:
    return re.sub(r'[^\w ]', '', text)


def sleep_with_reminder(secs_to_sleep: int, reminder_span: int):
    """
    Like the time.sleep(secs) function except it logs
    the remaining time after

    Args:
        secs_to_sleep: the time to sleep in seconds
        reminder_span: the time interval after which I will remind you how much time is left
    """
    secs_passed = 0
    while secs_passed < secs_to_sleep:
        secs_remaining = secs_to_sleep - secs_passed
        logging.info(
            f"I'll wake up after {secs_remaining//60} mins {secs_remaining%60} seconds")
        time.sleep(reminder_span)
        secs_passed += reminder_span
