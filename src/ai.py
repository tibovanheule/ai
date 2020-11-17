"""@package AI
The Ai module implements the core ai functions

More details....
"""
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
import db
from NLP import text_precessing


def analyse_text(text, data, hate, modelname="logistic_regression"):
    stopwords_set = stopwords.words("english")
    vectorizer = TfidfVectorizer(preprocessor=text_precessing, tokenizer=return_token,
                                 max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3), norm=None,
                                 decode_error="replace")
    dbobj = db.DB()
    if dbobj.model_in_db(modelname):
        return "lol"
    else:

        x_train, x_test, y_train, y_test = train_test_split(data, hate)
        vect = vectorizer.fit(x_train)
        with open('vectorizer.pk', 'wb') as fin:
            pickle.dump(vectorizer, fin)
        x_train_vectorized = vect.transform(x_train)

        model = LogisticRegression(verbose=True, n_jobs=-1)
        model.fit(x_train_vectorized, y_train)

        predictions = model.predict(vect.transform(x_test))
        print(predictions)
        return str(predictions)


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
