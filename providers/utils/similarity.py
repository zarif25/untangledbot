from difflib import SequenceMatcher
from . import remove_symbols, remove_stop_words


def text_similarity(text1, text2):
    """
    Returns:
        Ratio of the number of important common words
        in both of the texts and the average number
        of words in both of the texts.
    """
    class Word:
        def __init__(self, word) -> None:
            self.word = word

        def __eq__(self, other) -> bool:
            return SequenceMatcher(None, self.word, other.word).ratio() > 0.8

        def __repr__(self) -> str:
            return self.word

    text1 = remove_stop_words(remove_symbols(text1).lower()).split()
    text2 = remove_stop_words(remove_symbols(text2).lower()).split()
    text1 = [Word(word) for word in text1 if word]
    text2 = [Word(word) for word in text2 if word]
    avg_text_words = (len(text1) + len(text2)) / 2
    common_words = len([word for word in text1 if word in text2])
    try:
        return common_words/avg_text_words
    except ZeroDivisionError:
        return 0



if __name__ == '__main__':
    print(text_similarity("বিশ্ব শান্তি সূচকে ছয় ধাপ এগিয়েছে বাংলাদেশ",
                          "বিশ্ব শান্তি সূচকে বাংলাদেশ ছয় ধাপ এগিয়েছে"))

    print(text_similarity("Bangladesh has advanced six steps in the world peace index.",
                          "Bangladesh is six steps, ahead in the world peace index."))
