"""@package NLP
Natural language processing

More details....
"""
import re

import nltk
from nltk.stem import SnowballStemmer
from nltk.classify import TextCat
import pycountry

nltk.download('punkt')
nltk.download('crubadan')

"""
Natural language processing

Main entry for natural language processing (text preprocessing).
"""


def text_precessing(text):
    language = detect_language(text)
    print(language)
    stemmer = SnowballStemmer(language)
    """Tokenize the string"""
    #text = remove_punctuation(text)
    tokens = tokenize(text)
    """remove punctuation, but keep 'Mr.' intact"""
    tokens = stem_text(tokens, stemmer)
    return tokens


def detect_language(text):
    tc = TextCat()
    lan = tc.guess_language(text)
    return str(pycountry.languages.get(alpha_3=lan).name).lower()


def tokenize(tex):
    return nltk.wordpunct_tokenize(tex)


"""
removal of punctuation

Main entry for natural language processing (text preprocessing).
"""


def remove_punctuation(text):
    print(text)
    text = re.split("[^a-zA-Z.,!?]*", text.lower())
    print(text)
    return text


"""
Term frequency - invers document frequency 

will run tf-idf on a given text input. for more information on this technique see the report.
"""


def tf_idf(text):
    processed = text
    return processed


def stem_text(tokens, stemmer):
    map(stemmer.stem, tokens)
    return tokens
