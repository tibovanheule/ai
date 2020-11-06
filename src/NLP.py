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
    """Remove Repeating characters like `oooooooooooooooooomygod """
    reg = re.compile(r'(.)\1{2,}')
    tokens = (remove_repeats(token, reg) for token in tokens if token not in ['.', ',', '?', '!'])
    """Spelling check"""
    checker = SpellChecker()
    """Use list now, wait for generator"""
    tokens = [spell_checker(token, checker) for token in tokens]
    """ Lemmanize text, ALWAYS LAST to avoid inconsistencies with incorrectly spelled words"""

    tokens = lemmanize_text(tokens)
    return list(tokens)


def remove_repeats(word, reg):
    return reg.sub(r'\1\1', word)


def spell_checker(word, checker):
    return checker.correction(word)


def tokenize(text):
    tokenizer = TweetTokenizer()
    return tokenizer.tokenize(text)


"""
removal of punctuation

Main entry for natural language processing (text preprocessing).
"""


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


def lemmanize_text(tokens):
    lem = WordNetLemmatizer()
    # Catogorize the tokens first
    tokens = nltk.pos_tag(tokens)
    tokens = (lem.lemmatize(token, pos=get_wordnet_pos(pos)) for (token, pos) in tokens)
    yield from tokens
