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
a = re.compile(r'(?:\b(?:@|/-\\|\^|/\\))')
b = re.compile(r'(?:\b(?:\|:|P>|ß))')
c = re.compile(r'(?:\b[©¢<\[({])')
d = re.compile(r'(?:\b(?:\)|\|\)|\[\)|\?|\|>\|o))')
e = re.compile(r'(?:\b(?:&|€|\[-))')
f = re.compile(r'(?:\b(?:\|=|/=|ph|ƒ|\|#))')
g = re.compile(r'(?:\b(?:&|C-|\(_\+))')
h = re.compile(r'(?:\b(?:#|}{|\|-\||\]-\[\|\[-\]|\(-\)|\)-\(|/-/))')
i = re.compile(r'(?:\b(?:!|\||\]|¡))')
j = re.compile(r'(?:\b(?:¿|_\||_/|</|\(/))')
k = re.compile(r'(?:\b(?:\|<|\|\{|\|\())')
letter_l = re.compile(r'(?:\b(?:\||£|\|_|¬))')
m = re.compile(r'(?:\b(?:\|v\||\|\\/\||/\\/\\|\(v\)|/\|\\|//\.|\^\^))')
n = re.compile(r'(?:\b(?:\|\\\||/\\/|\[\\\]|<\\>|/V|\^/))')
o = re.compile(r'(?:\b(?:\(\)|\[\]|°))')
p = re.compile(r'(?:\b(?:\|\*|¶|\|o|\|°|\|\"|\|>|\|\^\(o\)|\|\^\(\)))')
q = re.compile(r'(?:\b(?:\(\)_|\(_,\)|<\|))')
r = re.compile(r'(?:\b(?:\|\^|\|\?|®))')
s = re.compile(r'(?:\b(?:\$|§))')
t = re.compile(r'(?:\b(?:\+|-\|-|†|\'\[\]\'))')
u = re.compile(r'(?:\b(?:\|_\||\(_\)))')
v = re.compile(r'(?:\b(?:\\/|\^))')
w = re.compile(r'(?:\b(?:VV|\\/\\/|\\\\\'|\'//|\\\|/|\\\^/))') # have fun checking these slashes...
x = re.compile(r'(?:\b(?:><|\)\(|%))')
y = re.compile(r'(?:\b(?:¥|\'/))')
z = re.compile(r'(?:\b(?:~/_|-/_|>_))')

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
hate = {i[0] for i in database.db_load_lexicon()}


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
    text = a.sub("a", text)
    text = b.sub("b", text)
    text = c.sub("c", text)
    text = d.sub("d", text)
    text = e.sub("e", text)
    text = f.sub("f", text)
    text = g.sub("g", text)
    text = h.sub("h", text)
    text = i.sub("i", text)
    text = j.sub("j", text)
    text = k.sub("k", text)
    text = letter_l.sub("l", text)
    text = m.sub("m", text)
    text = n.sub("n", text)
    text = o.sub("o", text)
    text = p.sub("p", text)
    text = q.sub("q", text)
    text = r.sub("r", text)
    text = s.sub("s", text)
    text = t.sub("t", text)
    text = u.sub("u", text)
    text = v.sub("v", text)
    text = w.sub("w", text)
    text = x.sub("x", text)
    text = y.sub("y", text)
    text = z.sub("z", text)

    """Tokenize the string"""
    tokens = tokenize(text)
    tokens = char_boundary(tokens)
    """ remove , . ! ? AND remove repeats"""
    """Spelling check"""
    tokens = [spell_checker(remove_repeats(token)) for token in tokens if token not in stopwords_set]
    """ Lemmanize text, ALWAYS LAST to avoid inconsistencies with incorrectly spelled words"""
    worden = (lemmanize_text(wordsegment(word)) for word in tokens)
    tokens = [token for sublist in worden for token in sublist if token not in stopwords_set]
    return tokens


def text_precessing_char(text):
    return ' '.join(text_precessing(text))


def remove_repeats(word):
    return reg.sub(r'\1\1', word)


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    if treebank_tag.startswith('V'):
        return wordnet.VERB
    if treebank_tag.startswith('N'):
        return wordnet.NOUN
    if treebank_tag.startswith('R'):
        return wordnet.ADV
    return wordnet.NOUN


def char_boundary(tokens):
    dict = {}
    for token in tokens:
        if token not in known_words and token not in hate and len(token) > 3:
            has_word(token, dict)
    return [k if k not in dict else max(dict[k], key=len) for k in tokens]


"""
Checks if some giberrisch word conceals a hatefull word, character bounding 
"""
def has_word(word, dict):
    fragments = {word[i:j] for i in range(len(word)) for j in range(i + 3, len(word) + 1)}
    sub_words = fragments.intersection(hate)
    if len(sub_words) > 0:
        dict[word] = sub_words
        return dict
    sub_words = fragments.intersection(known_words)
    if len(sub_words) > 0:
        dict[word] = sub_words
    return dict


def lemmanize_text(tokens):
    # Catogorize the tokens first
    tokens = tag(tokens)
    tokens = (lemmatize(token, pos=get_wordnet_pos(pos)) for (token, pos) in tokens)
    yield from tokens
