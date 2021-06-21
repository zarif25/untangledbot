from providers.utils.constants import TOPIC_MAPPING
from urllib.parse import urlparse


__PUNCUATIONS = ["!", "\"", "#", "$", "%", "&", "'",
                 "(", ")", "*", "+", ",", "-", "_", ".", "/", "\\", ":", ";", "<", "=", ">", "?", "[", "{", "}", "]", "।", ","]


def truncate(text: str, max_char: int) -> str:
    """
    Returns a truncated string
    >>> trancate("You can't actually truncate a Python string", 10)
    >>> "You can'..."
    """
    return (text[:max_char-2]+'..') if len(text) > max_char else text


def to_pascal(text: str) -> str:
    """
    Return a string in Pascal case
    >>> to_pascal("akash bhora tara")
    >>> "AkashBhoraTara"
    """
    return text.title().replace(' ', '')


def remove_symbols(text: str) -> str:
    """
    Return a string removing the symbols
    """
    return ''.join(char for char in text if char not in __PUNCUATIONS)


def remove_stop_words(text: str) -> str:
    """
    Args:
        text: a string with all lowercase characters
    Return the input string removing the stop words
    """
    __STOP_WORDS = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off',
                    'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
    __STOP_WORDS += ["অতএব", "অথচ", "অথবা", "অনুযায়ী", "অনেক", "অনেকে", "অনেকেই", "অন্তত", "অন্য", "অবধি", "অবশ্য", "অর্থাত", "আই", "আগামী", "আগে", "আগেই", "আছে", "আজ", "আদ্যভাগে", "আপনার", "আপনি", "আবার", "আমরা", "আমাকে", "আমাদের", "আমার", "আমি", "আর", "আরও", "ই", "ইত্যাদি", "ইহা", "উচিত", "উত্তর", "উনি", "উপর", "উপরে", "এ", "এঁদের", "এঁরা", "এই", "একই", "একটি", "একবার", "একে", "এক্", "এখন", "এখনও", "এখানে", "এখানেই", "এটা", "এটাই", "এটি", "এত", "এতটাই", "এতে", "এদের", "এব", "এবং", "এবার", "এমন", "এমনকী", "এমনি", "এর", "এরা", "এল", "এস", "এসে", "ঐ", "ও", "ওঁদের", "ওঁর", "ওঁরা", "ওই", "ওকে", "ওখানে", "ওদের", "ওর", "ওরা", "কখনও", "কত", "কবে", "কমনে", "কয়েক", "কয়েকটি", "করছে", "করছেন", "করতে", "করবে", "করবেন", "করলে", "করলেন", "করা", "করাই", "করায়", "করার", "করি", "করিতে", "করিয়া", "করিয়ে", "করে", "করেই", "করেছিলেন", "করেছে", "করেছেন", "করেন", "কাউকে", "কাছ", "কাছে", "কাজ", "কাজে", "কারও", "কারণ", "কি", "কিংবা", "কিছু", "কিছুই", "কিন্তু", "কী", "কে", "কেউ", "কেউই", "কেখা", "কেন", "কোটি", "কোন", "কোনও", "কোনো", "ক্ষেত্রে", "কয়েক", "খুব", "গিয়ে", "গিয়েছে", "গিয়ে", "গুলি", "গেছে", "গেল", "গেলে", "গোটা", "চলে", "চান", "চায়", "চার", "চালু", "চেয়ে", "চেষ্টা", "ছাড়া", "ছাড়াও", "ছিল", "ছিলেন", "জন", "জনকে", "জনের", "জন্য", "জন্যওজে", "জানতে", "জানা", "জানানো", "জানায়", "জানিয়ে", "জানিয়েছে", "জে", "জ্নজন", "টি", "ঠিক", "তখন", "তত", "তথা", "তবু", "তবে", "তা", "তাঁকে", "তাঁদের", "তাঁর", "তাঁরা", "তাঁাহারা", "তাই", "তাও", "তাকে", "তাতে", "তাদের", "তার", "তারপর", "তারা", "তারৈ", "তাহলে", "তাহা", "তাহাতে", "তাহার", "তিনঐ", "তিনি", "তিনিও", "তুমি", "তুলে", "তেমন", "তো", "তোমার", "থাকবে", "থাকবেন", "থাকা", "থাকায়", "থাকে",
                     "থাকেন", "থেকে", "থেকেই", "থেকেও", "দিকে", "দিতে", "দিন", "দিয়ে", "দিয়েছে", "দিয়েছেন", "দিলেন", "দু", "দুই", "দুটি", "দুটো", "দেওয়া", "দেওয়ার", "দেওয়া", "দেখতে", "দেখা", "দেখে", "দেন", "দেয়", "দ্বারা", "ধরা", "ধরে", "ধামার", "নতুন", "নয়", "না", "নাই", "নাকি", "নাগাদ", "নানা", "নিজে", "নিজেই", "নিজেদের", "নিজের", "নিতে", "নিয়ে", "নিয়ে", "নেই", "নেওয়া", "নেওয়ার", "নেওয়া", "নয়", "পক্ষে", "পর", "পরে", "পরেই", "পরেও", "পর্যন্ত", "পাওয়া", "পাচ", "পারি", "পারে", "পারেন", "পি", "পেয়ে", "পেয়্র্", "প্রতি", "প্রথম", "প্রভৃতি", "প্রযন্ত", "প্রাথমিক", "প্রায়", "প্রায়", "ফলে", "ফিরে", "ফের", "বক্তব্য", "বদলে", "বন", "বরং", "বলতে", "বলল", "বললেন", "বলা", "বলে", "বলেছেন", "বলেন", "বসে", "বহু", "বা", "বাদে", "বার", "বি", "বিনা", "বিভিন্ন", "বিশেষ", "বিষয়টি", "বেশ", "বেশি", "ব্যবহার", "ব্যাপারে", "ভাবে", "ভাবেই", "মতো", "মতোই", "মধ্যভাগে", "মধ্যে", "মধ্যেই", "মধ্যেও", "মনে", "মাত্র", "মাধ্যমে", "মোট", "মোটেই", "যখন", "যত", "যতটা", "যথেষ্ট", "যদি", "যদিও", "যা", "যাঁর", "যাঁরা", "যাওয়া", "যাওয়ার", "যাওয়া", "যাকে", "যাচ্ছে", "যাতে", "যাদের", "যান", "যাবে", "যায়", "যার", "যারা", "যিনি", "যে", "যেখানে", "যেতে", "যেন", "যেমন", "র", "রকম", "রয়েছে", "রাখা", "রেখে", "লক্ষ", "শুধু", "শুরু", "সঙ্গে", "সঙ্গেও", "সব", "সবার", "সমস্ত", "সম্প্রতি", "সহ", "সহিত", "সাধারণ", "সামনে", "সি", "সুতরাং", "সে", "সেই", "সেখান", "সেখানে", "সেটা", "সেটাই", "সেটাও", "সেটি", "স্পষ্ট", "স্বয়ং", "হইতে", "হইবে", "হইয়া", "হওয়া", "হওয়ায়", "হওয়ার", "হচ্ছে", "হত", "হতে", "হতেই", "হন", "হবে", "হবেন", "হয়", "হয়তো", "হয়নি", "হয়ে", "হয়েই", "হয়েছিল", "হয়েছে", "হয়েছেন", "হল", "হলে", "হলেই", "হলেও", "হলো", "হাজার", "হিসাবে", "হৈলে", "হোক", "হয়"]
    return ' '.join(word for word in text.split() if not word in __STOP_WORDS)


def to_topic_or_none(url: str):
    """
    Returns:
        The topic extracted from url or none
    """
    parsed_url = urlparse(url)
    if 'opinion' in parsed_url.netloc:
        return 'opinion'
    elif 'sport' in parsed_url.netloc:
        return 'sports'
    potential_topics = urlparse(url).path.strip('/').split('/')[:-1]
    for potential_topic in potential_topics:
        if not (potential_topic.isnumeric() or ('article' in potential_topic) or ('en' in potential_topic and 'environment' not in potential_topic and 'entertainment' not in potential_topic)):
            return potential_topic


def to_untangled_topic_or_none(extracted_topic: str) -> str:
    for key, value in TOPIC_MAPPING.items():
        if key in extracted_topic:
            return value
