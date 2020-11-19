"""@package AI
The Ai module implements the core ai functions

More details....
"""
import multiprocessing
import pickle

import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import db
from NLP import text_precessing


def analyse_text(text, modelname="logistic_regression"):
    with open('mini_model.pk', 'rb') as file:
        model = pickle.load(file)
    with open('mini_vectorizer.pk', 'rb') as file:
        vectorizer = pickle.load(file)
    test = vectorizer.transform([text])
    return str(model.predict(test))


def process_text(text):
    return str(text_precessing(text.lower()))


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
        print("Splitting data into train & test")
        x_train, x_test, y_train, y_test = train_test_split(data[:100], hate[:100], train_size=0.7, random_state=4262)
        print("fitting training")
        vect = vectorizer.fit(x_train)
        with open('para_mini_vect.pk', 'wb') as fin:
            pickle.dump(vect, fin)
        with open('para_mini_vectorizer.pk', 'wb') as fin:
            pickle.dump(vectorizer, fin)

        print("transforming training")
        # x_train_vectorized = vect.transform(x_train)
        x_train_vectorized = parallel_construct(x_train, vect.transform)
        with open('para_mini_x-train-vectorizer.pk', 'wb') as fin:
            pickle.dump(x_train_vectorized, fin)
        print("initing model")
        model = LogisticRegression(verbose=True, n_jobs=-1)
        model.fit(x_train_vectorized, y_train)
        dbobj.insert_model_in_db(modelname, pickle.dumps(model))
        predictions = model.predict(vect.transform(x_test))
        print(f"Model made, predictions on the test are {predictions}")
        with open('para_mini_model.pk', 'wb') as fin:
            pickle.dump(model, fin)
        dbobj.insert_model_in_db("para_f_tfidfvectorizer", pickle.dumps(model))
        with open('score.txt', 'w') as file:
            score = accuracy_score(y_test, predictions, normalize=True)
            file.write(str(score))
        print("safed files")


def parallel_construct(data, func):
    core_count = multiprocessing.cpu_count() - 1
    print(f"working on {core_count} threads")

    data_split = np.array_split(data, core_count)
    pool = multiprocessing.Pool(core_count)

    df = sp.vstack(pool.map(func, data_split), format='csr')
    pool.close()
    pool.join()
    return df
