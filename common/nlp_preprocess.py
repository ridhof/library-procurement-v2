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
    preprocessed_text = ''
    language = ''

    def __init__(self, text):
        self.set_text(text)

    def set_text(self, text):
        self.text = text
        self.detect_language()
        self.preprocess()

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

    def remove_non_ascii(words):
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode(
                'ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words

    def to_lowercase(words):
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words

    def remove_punctuation(words):
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words

    def replace_numbers(words):
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words

    def remove_stopwords(words, language='english'):
        new_words = []
        for word in words:
            if word not in stopwords.words(language):
                new_words.append(word)
        return new_words

    def lemmatize_verbs(words, language='english'):
        lemmatizer = WordNetLemmatizer()
        factory = StemmerFactory()
        if language == 'indonesian':
            stemmer = factory.create_stemmer()
        lemmas = []
        for word in words:
            if language == 'indonesian':
                lemmas.append(
                    stemmer.stem(word)
                )
            else:
                lemmas.append(
                    lemmatizer.lemmatize(word, pos='v')
                )
        return lemmas

    def preprocess(self):
        words = nltk.word_tokenize(self.text)

        words = NLP.remove_non_ascii(words)
        words = NLP.to_lowercase(words)
        words = NLP.remove_punctuation(words)
        if self.language == 'english':
            words = NLP.replace_numbers(words)
        words = NLP.remove_stopwords(words, language=self.language)
        words = NLP.lemmatize_verbs(words, language=self.language)

        self.preprocessed_text = ' '.join(words)
