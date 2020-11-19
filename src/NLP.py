"""@package NLP
Natural language processing

More details....
"""
import re
from functools import lru_cache

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

"GLOBAL module variabeles"
reg = re.compile(r'(.)\1{2,}')
mention_hashtag_regex = re.compile(r'^@[\w\-]+|^[\s]#([^\s])+')
replacement_regex = re.compile(r'([^\s])@')  # this WILL have to be changed rn serves as boilerplate for later
url_remove = re.compile(
    r'(h(\s)*t(\s)*t(\s)*p(\s)*s?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*')
contarction_not = re.compile(r'n\'t')
contarction_am = re.compile(r'\'m')
contarction_have = re.compile(r'\'ve')
contarction_will = re.compile(r'\'ll')

checker = SpellChecker()
wnl = WordNetLemmatizer()
lemmatize = lru_cache(wnl.lemmatize)
tag = nltk.pos_tag


class CustomTweetTokenizer(TweetTokenizer):
    def tokenize(self, text):
        # Fix HTML character entities:
        text = _replace_html_entities(text)
        # Substitute non-alpha characters in the middle of a word
        text = substitute_letters(text)
        # Shorten problematic sequences of characters
        safe_text = HANG_RE.sub(r"\1\1\1", text)
        # Tokenize:
        return WORD_RE.findall(safe_text)


tokenizer = CustomTweetTokenizer()


def text_precessing(text):
    text = demoji.replace_with_desc(text, sep="")
    text = url_remove.sub("site", text)
    text = contarction_not.sub(" not", text)
    text = contarction_am.sub(" am", text)
    text = contarction_have.sub(" have", text)
    text = contarction_will.sub(" will", text)
    """Tokenize the string"""
    tokens = tokenizer.tokenize(text)
    """ remove , . ! ? AND remove repeats"""
    """Spelling check"""
    tokens = [spell_checker(remove_repeats(token)) for token in tokens if
              token not in ['.', ',', '?', '!']]
    """ Lemmanize text, ALWAYS LAST to avoid inconsistencies with incorrectly spelled words"""
    return list(lemmanize_text(tokens))


def substitute_letters(word):
    word = replacement_regex.sub(r'\1a', word)
    return word


def remove_repeats(word):
    unMention = mention_hashtag_regex.sub("entity", word)
    return reg.sub(r'\1\1', unMention)


def spell_checker(word):
    return checker.correction(word)


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
    # Catogorize the tokens first
    tokens = tag(tokens)
    tokens = (lemmatize(token, pos=get_wordnet_pos(pos)) for (token, pos) in tokens)
    yield from tokens
