"""@package NLP
Natural language processing

More details....
"""
import re
from functools import lru_cache

import demoji
import nltk
import wordsegment as ws
from nltk.corpus import wordnet, stopwords
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
mention_hashtag_regex = re.compile(r'([^\w]|^)@[\w\-]+|^[\s]#([^\s])+')
replacement_regex = re.compile(r'([^\s])@')  # this WILL have to be changed rn serves as boilerplate for later
url_remove = re.compile(
    r'(h(\s)*t(\s)*t(\s)*p(\s)*s?://)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+/)*([\w\-]+)((\?)?[\w\s]*=\s*['
    r'\w%&]*)*')
contarction_not = re.compile(r'n\'t')
contarction_am = re.compile(r'\'m')
contarction_have = re.compile(r'\'ve')
contarction_will = re.compile(r'\'ll')

checker = SpellChecker()
wnl = WordNetLemmatizer()
lemmatize = lru_cache(wnl.lemmatize)
wordsegment = lru_cache(ws.segment)
spell_checker = lru_cache(checker.correction)
tag = nltk.pos_tag
stopwords_set = stopwords.words("english")
stopwords_set.extend(['.', ',', '?', '!', '\'', '$', '&', '"', ':', '-', '/', '<', '>'])
stopwords_set = set(stopwords_set)


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


tokenize = CustomTweetTokenizer().tokenize


def text_precessing(text):
    text = demoji.replace_with_desc(text, sep="")
    text = url_remove.sub(" site", text)
    text = contarction_not.sub(" not", text)
    text = contarction_am.sub(" am", text)
    text = contarction_have.sub(" have", text)
    text = contarction_will.sub(" will", text)

    text = mention_hashtag_regex.sub(" entity", text)
    """Tokenize the string"""
    tokens = tokenize(text)
    """ remove , . ! ? AND remove repeats"""
    """Spelling check"""
    tokens = [spell_checker(remove_repeats(token)) for token in tokens if token not in stopwords_set]
    """ Lemmanize text, ALWAYS LAST to avoid inconsistencies with incorrectly spelled words"""
    words = (lemmanize_text(wordsegment(word)) for word in tokens)
    return [token for sublist in words for token in sublist if token not in stopwords_set]


def substitute_letters(word):
    word = replacement_regex.sub(r'\1a', word)
    return word


def remove_repeats(word):
    return reg.sub(r'\1\1', word)


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
