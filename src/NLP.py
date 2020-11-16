"""@package NLP
Natural language processing

More details....
"""
import re

import demoji
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.tokenize.casual import _replace_html_entities, HANG_RE, WORD_RE
from spellchecker import SpellChecker

"""
Natural language processing

Main entry for natural language processing (text preprocessing).
"""


def text_precessing(text):
    text = demoji.replace_with_desc(text, sep="")
    """Tokenize the string"""
    tokens = tokenize(text)
    """ remove , . ! ?"""
    reg = re.compile(r'(.)\1{2,}')
    tokens = (remove_repeats(token, reg) for token in tokens if token not in ['.', ',', '?', '!'])
    """Spelling check"""
    checker = SpellChecker()
    """Use list now, wait for generator"""
    tokens = [spell_checker(token, checker) for token in tokens]
    """ Lemmanize text, ALWAYS LAST to avoid inconsistencies with incorrectly spelled words"""
    # remove_handles(text)
    tokens = lemmanize_text(tokens)
    return list(tokens)


def remove_repeats(word, reg):
    return reg.sub(r'\1\1', word)


def spell_checker(word, checker):
    return checker.correction(word)


class CustomTweetTokenizer(TweetTokenizer):
    def tokenize(self, text):
        # Fix HTML character entities:
        text = _replace_html_entities(text)
        # Shorten problematic sequences of characters
        safe_text = HANG_RE.sub(r"\1\1\1", text)
        # Tokenize:
        words = WORD_RE.findall(safe_text)
        return words


def tokenize(text):
    tokenizer = CustomTweetTokenizer()
    return tokenizer.tokenize(text)


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
