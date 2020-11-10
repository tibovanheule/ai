"""@package AI
The Ai module implements the core ai functions

More details....
"""
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

from NLP import text_precessing


def analyse_text(text,data):
    # print(str(NLP.text_precessing(text)))
    stopwords_set = stopwords.words("english")
    vectorizer = TfidfVectorizer(preprocessor=text_precessing, tokenizer=return_token, stop_words=stopwords_set,
                                 max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3), norm=None,
                                 decode_error="replace")

    # res = model.predict(vectorizer.transform())
    return str(vectorizer)


def process_text(text):
    return str(text_precessing(text))


def return_token(text):
    return text


def validate():
    return "Hello, the ai thanks you for the lesson!"


def construct_matrix(text, vecto):
    # ? tf is this even used for???
    tfidf = vecto.fit_transform(text).toarray()
    vocab = {v: i for i, v in enumerate(vecto.get_feature_names())}
    idf_vals = vecto.idf_
    return text
