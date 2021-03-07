# Created by dinar at 01.03.2021
import re

from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import string
import pymorphy2


class TextAnalyzerUtil:

    @staticmethod
    def get_unique_words_from_posts_as_dict(text,
                                            clean_text: bool = False,
                                            language=None,
                                            stemming=False,
                                            lemmatization=False):
        if language is None:
            language = list("english")

        list_of_words = []
        if clean_text:
            text = TextAnalyzerUtil.clean_text(text, language)
            if stemming:
                list_of_words = TextAnalyzerUtil.stem(text.split(' '), language)
            elif lemmatization:
                list_of_words = TextAnalyzerUtil.lemmatizate(text.split(' '))
        else:
            list_of_words = str(text).split(' ')
        return TextAnalyzerUtil.get_unique_words_dict(list_of_words)

    @staticmethod
    def clean_text(text, language):
        """
        :param text: input text
        :param language: languages of stop words
        :var stop_words - symbols like but, are, is ...
        :return: clear text
        """
        stop_words = []
        for lang in language:
            stop_words.extend(stopwords.words(lang))
        # To lowercase
        text = text.lower()
        # Remove - " - symbols
        text = re.sub("[«»”“]", "", text)

        # Remove no utf-8 symbols
        text = text.encode('utf-8', 'ignore').decode()
        # Remove stop words
        text = ' '.join([word for word in text.split(' ') if word not in stop_words])
        # Remove mentions
        text = re.sub("@\S+", " ", text)
        # Remove URL
        text = re.sub("https*\S+", " ", text)
        # Remove Hashtags
        text = re.sub("#\S+", " ", text)
        # Remove new lines
        text = re.sub("^\s+|\n|\r|\s+$", '', text)
        # Remove emojis
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        # Remove ticks and the next character
        text = re.sub("\'\w+", '', text)
        # Remove punctuations
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
        # Remove numbers
        text = re.sub(r'\w*\d+\w*', '', text)
        # Replace the over spaces
        text = re.sub('\s{2,}', " ", text)
        return text

    @staticmethod
    def get_unique_words_dict(list_of_words: [str]):
        dict_of_unique_words = {}
        for word in list_of_words:
            if dict_of_unique_words.get(word):
                dict_of_unique_words[word] = dict_of_unique_words.get(word) + 1
            else:
                dict_of_unique_words[word] = 1
        return dict_of_unique_words

    @staticmethod
    def stem(list_of_words, language):
        for lang in language:
            snow_ball = SnowballStemmer(lang)
            list_of_words = map(lambda word: snow_ball.stem(word), list_of_words)
        return list_of_words

    @staticmethod
    def lemmatizate(list_of_words):
        morph = pymorphy2.MorphAnalyzer()
        return list(map(lambda word: morph.parse(word)[0].normal_form, list_of_words))
