"""@package NLP
Natural language processing

More details....
"""
import re

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.classify import TextCat
from nltk.tokenize import TweetTokenizer
from spellchecker import SpellChecker

nltk.download('wordnet')

"""
Natural language processing

Main entry for natural language processing (text preprocessing).
"""


def text_precessing(text):
    text = text.lower()
    lem = WordNetLemmatizer()
    """Tokenize the string"""
    tokens = tokenize(text)

    """Remove Repeating characters like `oooooooooooooooooomygod """
    tokens = [remove_repeats(token) for token in tokens]

    tokens = [spell_checker(token) for token in tokens]


    """ Lemmanize text, ALWAYS LAST to avoid inconsistencies with incorrectly spelled words"""
    tokens = lemmanize_text(tokens, lem)
    return tokens


def remove_repeats(word):
    return re.sub(r'(.)\1{2,}', r'\1\1', word)


def spell_checker(word):
    checker = SpellChecker()
    return checker.correction(word)


def tokenize(text):
    tokenizer = TweetTokenizer()
    return tokenizer.tokenize(text)


"""
removal of punctuation

Main entry for natural language processing (text preprocessing).
"""


def remove_punctuation(text):
    print(text)
    text = re.sub(".,!?", "", text.lower())
    print(text)
    return text


"""
Term frequency - invers document frequency 

will run tf-idf on a given text input. for more information on this technique see the report.
"""


def tf_idf(text):
    processed = text
    return processed


def lemmanize_text(tokens, lem):
    tokens = [lem.lemmatize(token, pos='n') for token in tokens]
    tokens = [lem.lemmatize(token, pos='v') for token in tokens]
    return tokens
