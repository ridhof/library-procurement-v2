import inflect
import nltk
import re
import unicodedata

from nltk import word_tokenize, wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class NLP():
    text = ''
    language = ''

    def __init__(self, text):
        self.set_text(text)

    def set_text(self, text):
        self.text = text
        self.detect_language()

    def detect_language(self):
        language_ratios = {}

        tokens = wordpunct_tokenize(self.text)
        words = [word.lower() for word in tokens]

        for language in stopwords.fileids():
            if language == 'english' or language == 'indonesian':
                stopwords_set = set(stopwords.words(language))
                words_set = set(words)
                common_elements = words_set.intersection(stopwords_set)

                language_ratios[language] = len(common_elements)

        self.language = max(language_ratios, key=language_ratios.get)
