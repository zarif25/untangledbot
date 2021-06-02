from difflib import SequenceMatcher
from logger import log_error


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
                log_error(f"problem in {info_name or func.__name__.strip('_')}", e)
            return info
        return inner
    return outer
