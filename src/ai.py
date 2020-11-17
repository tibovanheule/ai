"""@package AI
The Ai module implements the core ai functions

More details....
"""
import pickle

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

import db
from NLP import text_precessing


def analyse_text(text, modelname="logistic_regression"):
    stopwords_set = stopwords.words("english")
    return str("prediction")


def process_text(text):
    return str(text_precessing(text))


def return_token(text):
    return text


def validate():
    return "Hello, the ai thanks you for the lesson!"


def construct_model(data, hate, modelname="logistic_regression"):
    vectorizer = TfidfVectorizer(preprocessor=text_precessing, tokenizer=return_token,
                                 max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3), norm=None,
                                 decode_error="replace")
    dbobj = db.DB()
    print(modelname)
    """Construct a db entry. Avoid using old model for requests made before ending of model construction"""
    dbobj.constructing_model_in_db(modelname)
    print(dbobj.get_model_in_db(modelname))
    if dbobj.model_in_db(modelname):
        print("lol")
    else:
        x_train, x_test, y_train, y_test = train_test_split(data, hate)
        vect = vectorizer.fit(x_train)
        with open('vect.pk', 'wb') as fin:
            pickle.dump(vect, fin)
        with open('vectorizer.pk', 'wb') as fin:
            pickle.dump(vectorizer, fin)
        dbobj.insert_vect_in_db("tfidfvectorizer", pickle.dumps(vect))
        x_train_vectorized = vect.transform(x_train)

        model = LogisticRegression(verbose=True, n_jobs=-1)
        model.fit(x_train_vectorized, y_train)
        dbobj.insert_model_in_db(modelname, pickle.dumps(model))
        predictions = model.predict(vect.transform(x_test))
        print(predictions)
