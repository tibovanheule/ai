"""@package NLP
Natural language processing

More details....
"""
import re
from functools import lru_cache

import demoji
import nltk
import wordsegment as ws
from nltk.corpus import wordnet, stopwords, words
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer
from nltk.tokenize.casual import _replace_html_entities, HANG_RE, WORD_RE
from spellchecker import SpellChecker
from math import pow

from db import DB

"""
Natural language processing

Main entry for natural language processing (text preprocessing).
"""

"GLOBAL module variabeles"
reg = re.compile(r'(.)\1{2,}')
mention_hashtag_regex = re.compile(r'([^\w]|^)@[\w\-]+|^[\s]#([^\s])+')
url_remove = re.compile(
    r'(h(\s)*t(\s)*t(\s)*p(\s)*s?://)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+/)*([\w\-]+)((\?)?[\w\s]*=\s*['
    r'\w%&]*)*')
contarction_not = re.compile(r'n\'t')
contarction_am = re.compile(r'\'m')
contarction_have = re.compile(r'\'ve')
contarction_will = re.compile(r'\'ll')

# NOTE: zal niet perfect alles aanpassen doordat chars verschillende letters kunnen voorstellen
# maar spellchecker zal dit opmerken

# @Tibo waarschijnlijk moeten 'gee' voor g en 'oh' voor o er niet bij, maar atm heb ik ze er in gestoken
# T is makkelijker om ze gwn weg te doen
a = re.compile(r'(?:(?:\b(?:@|/-\\|\^|/\\))|(?:([a-zA-Z])3))')
b = re.compile(r'(?:(?:\b(?:\|:|P>|ß))|(?:([a-zA-Z])3))')
c = re.compile(r'(?:(?:\b[©¢<\[({])|(?:([a-zA-Z])3))')
d = re.compile(r'(?:(?:\b(?:\)|\|\)|\[\)|\?|\|>\|o))|(?:([a-zA-Z])3))')
e = re.compile(r'(?:(?:\b(?:&|€|\[-|ë))|(?:([a-zA-Z])3))')
f = re.compile(r'(?:(?:\b(?:\|=|/=|ph|ƒ|\|#))|(?:([a-zA-Z])3))')
g = re.compile(r'(?:(?:\b(?:&|C-|\(_\+|gee))|(?:([a-zA-Z])3))')
h = re.compile(r'(?:(?:\b(?:#|}{|\|-\||\]-\[\|\[-\]|\(-\)|\)-\(|/-/))|(?:([a-zA-Z])3))')
i = re.compile(r'(?:(?:\b(?:!|\||\]|eye|¡))|(?:([a-zA-Z])3))')
j = re.compile(r'(?:(?:\b(?:¿|_\||_/|</|\(/))|(?:([a-zA-Z])3))')
k = re.compile(r'(?:(?:\b(?:\|<|\|\{|\|\())|(?:([a-zA-Z])3))')
letter_l = re.compile(r'(?:(?:\b(?:\||£|\|_|1_|¬))|(?:([a-zA-Z])3))')
m = re.compile(r'(?:(?:\b(?:\|v\||\|\\/\||/\\/\\|\(v\)|/\|\\|//\.|\^\^|em))|(?:([a-zA-Z])3))')
n = re.compile(r'(?:(?:\b(?:\|\\\||/\\/|\[\\\]|<\\>|/V|\^/))|(?:([a-zA-Z])3))')
o = re.compile(r'(?:(?:\b(?:\(\)|\[\]|°|oh))|(?:([a-zA-Z])3))')
p = re.compile(r'(?:(?:\b(?:\|\*|¶|\|o|\|°|\|\"|\|>|\|\^\(o\)|\|\^\(\)))|(?:([a-zA-Z])3))')
q = re.compile(r'(?:(?:\b(?:\(\)_|\(_,\)|<\|))|(?:([a-zA-Z])3))')
r = re.compile(r'(?:(?:\b(?:\|\^|lz|\|\?|®))|(?:([a-zA-Z])3))')
s = re.compile(r'(?:(?:\b(?:\$|§|es))|(?:([a-zA-Z])3))')
t = re.compile(r'(?:(?:\b(?:\+|-\|-|†|\'\[\]\'))|(?:([a-zA-Z])3))')
u = re.compile(r'(?:(?:\b(?:µ|\|_\||\(_\)))|(?:([a-zA-Z])3))')
v = re.compile(r'(?:(?:\b(?:\\/|\^))|(?:([a-zA-Z])3))')
w = re.compile(r'(?:(?:\b(?:VV|\\/\\/|\\\\\'|\'//|\\\|/|\\\^/))|(?:([a-zA-Z])3))') # have fun checking these slashes...
x = re.compile(r'(?:(?:\b(?:><|\)\(|%|ecks))|(?:([a-zA-Z])3))')
y = re.compile(r'(?:(?:\b(?:¥|\'/))|(?:([a-zA-Z])3))')
z = re.compile(r'(?:(?:\b(?:~/_|-/_|>_))|(?:([a-zA-Z])3))')

ws.load()
checker = SpellChecker()
wnl = WordNetLemmatizer()
tag = nltk.pos_tag
try:
    nltk.data.find('corpora/stopwords')
    stopwords_set = stopwords.words("english")
    stopwords_set.extend(['.', ',', '?', '!', '\'', '$', '&', '"', ':', '-', '/', '<', '>'])
    stopwords_set = set(stopwords_set)
except LookupError:
    stopwords_set = set()
    print("PLEASE INIT, AND RESTART SERVER")


try:
    nltk.data.find('corpora/words')
    known_words = set(words.words())
except LookupError:
    known_words = set()
    print("PLEASE INIT, AND RESTART SERVER")

database = DB()
hate = set(i[0] for i in database.db_load_lexicon())



@lru_cache(maxsize=5000)
def lemmatize(token, pos):
    return wnl.lemmatize(token, pos=pos)


@lru_cache(maxsize=5000)
def wordsegment(token):
    return ws.segment(token)


@lru_cache(maxsize=5000)
def spell_checker(token):
    return checker.correction(token)


class CustomTweetTokenizer(TweetTokenizer):
    def tokenize(self, text):
        # Fix HTML character entities:
        text = _replace_html_entities(text)
        # Shorten problematic sequences of characters
        safe_text = HANG_RE.sub(r"\1\1\1", text)
        # Tokenize:
        return WORD_RE.findall(safe_text)


tokenize = CustomTweetTokenizer().tokenize


def text_precessing(text):
    text = demoji.replace_with_desc(text, sep="")

    text = contarction_not.sub(" not", text)
    text = contarction_am.sub(" am", text)
    text = contarction_have.sub(" have", text)
    text = contarction_will.sub(" will", text)

    text = url_remove.sub(" site", text)

    text = mention_hashtag_regex.sub(" entity", text)
    text = a.sub("\1a", text)

    """Tokenize the string"""
    tokens = tokenize(text)
    """ remove , . ! ? AND remove repeats"""
    """Spelling check"""
    tokens = [spell_checker(remove_repeats(token)) for token in tokens if token not in stopwords_set]
    """ Lemmanize text, ALWAYS LAST to avoid inconsistencies with incorrectly spelled words"""
    worden = (lemmanize_text(wordsegment(word)) for word in tokens)
    tokens = [token for sublist in worden for token in sublist if token not in stopwords_set]
    not_known = (token for token in tokens if token not in known_words and token not in hate)
    tokenkl = [has_word(token) for token in not_known if len(token) > 3]
    print(tokenkl)
    #map(lambda x: x if x tokenkl else 'sss', a)
    permute_spaces([token for token in tokens if token not in known_words])
    return tokens

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


def has_word(word):
    fragments = set(word[i:j] for i in range(len(word)) for j in range(i + 3, len(word) + 1))
    sub_words = fragments.intersection(hate)
    if len(sub_words) > 0:
        return word, sub_words
    sub_words = fragments.intersection(known_words)
    return None if len(sub_words) == 0 else (word, sub_words)


def permute_spaces(str):
    n = len(str)
    opsize = int(pow(2, n - 1))
    pos = list()
    for counter in range(opsize):
        new_pos_elem = list()
        string = ""
        for j in range(n):
            if j != 0 and not (counter & (1 << j)):
                new_pos_elem.append(string)
                string = ""
            string = string + str[j]
            if counter & (1 << j):
                string = string + " "

        pos.append(new_pos_elem)
    print(pos)


def lemmanize_text(tokens):
    # Catogorize the tokens first
    tokens = tag(tokens)
    tokens = (lemmatize(token, pos=get_wordnet_pos(pos)) for (token, pos) in tokens)
    yield from tokens
