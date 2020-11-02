"""@package NLP
Natural language processing

More details....
"""
import re

import nltk
from nltk.stem import WordNetLemmatizer
import demoji
from nltk.tokenize import TweetTokenizer
from spellchecker import SpellChecker
from nltk.corpus import wordnet

"""
Natural language processing

Main entry for natural language processing (text preprocessing).
"""


def text_precessing(text):
    text = text.lower()
    text = demoji.replace_with_desc(text, sep="")
    """Tokenize the string"""
    tokens = tokenize(text)
    """ remove , . ! ?"""
    tokens = filter(remove_punctuation,tokens)
    """Remove Repeating characters like `oooooooooooooooooomygod """
    tokens = [remove_repeats(token) for token in tokens]
    """Spelling check"""
    tokens = [spell_checker(token) for token in tokens]
    """ Lemmanize text, ALWAYS LAST to avoid inconsistencies with incorrectly spelled words"""

    tokens = lemmanize_text(tokens)
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
    return text not in ['.', ',', '?', '!']


def get_wordnet_pos(word):
    treebank_tag = nltk.pos_tag(word)
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def lemmanize_text(tokens):
    lem = WordNetLemmatizer()
    tokens = [lem.lemmatize(token, pos=get_wordnet_pos(token)) for token in tokens]
    return tokens
