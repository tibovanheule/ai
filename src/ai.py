"""@package AI
The Ai module implements the core ai functions

More details....
"""
import multiprocessing
import pickle

import numpy as np
import scipy.sparse as sp
from gensim.models import Word2Vec
from keras.layers import Embedding, LSTM
from keras.models import Sequential
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline

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
    if modelname == "logistic_regression":
        vectorizer = TfidfVectorizer(preprocessor=text_precessing, tokenizer=return_token,
                                     max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3),
                                     norm=None,
                                     decode_error="replace")
        logistic(vectorizer, data, hate, modelname)
    elif modelname == "logistic_regression_char":

        vectorizer = TfidfVectorizer(preprocessor=text_precessing, tokenizer=return_token,
                                     max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3),
                                     norm=None,
                                     decode_error="replace")
        logistic(vectorizer, data, hate, modelname)
    else:
        construct_lstm(data, hate)


def logistic(vectorizer, data, hate, modelname):
    dbobj = db.DB()

    """Construct a db entry. Avoid using old model for requests made before ending of model construction"""
    dbobj.constructing_model_in_db(modelname)
    print("Splitting data into train & test")
    x_train, x_test, y_train, y_test = train_test_split(data, hate, train_size=0.7, random_state=4262)
    print("fitting training")
    vect = vectorizer.fit(x_train)
    print("transforming training")
    # x_train_vectorized = vect.transform(x_train)
    x_train_vectorized = parallel_construct(x_train, vect.transform)
    params = [{}]
    pipe = Pipeline(
        [('select', SelectFromModel(LogisticRegression(n_jobs=-1))), ('model', LogisticRegression(n_jobs=-1))])
    model = GridSearchCV(pipe, params, cv=StratifiedKFold(n_splits=5, random_state=42).split(x_train, y_train))
    print("initing model")
    model.fit(x_train_vectorized, y_train)
    dbobj.insert_model_in_db(modelname, pickle.dumps(model))
    predictions = model.predict(vect.transform(x_test))
    print(f"Model made, predictions on the test are {predictions}")
    dbobj.insert_model_in_db(modelname, pickle.dumps(model))


def parallel_construct(data, func):
    core_count = multiprocessing.cpu_count() - 1
    print(f"working on {core_count} threads")

    data_split = np.array_split(data, core_count)
    pool = multiprocessing.Pool(core_count)

    df = sp.vstack(pool.map(func, data_split), format='csr')
    pool.close()
    pool.join()
    return df


def construct_lstm(data, hate, max_features=100000, maxlen=500):
    return 0


def make_lstm_model(sequence_length, embedding_dim):
    model_variaton = "LSTM"
    model = Sequential()
    embed_layer = Embedding(input_dimm=weights.shape[0],
                            output_dim=weights.shape[1],
                            weights=[weights])
    model.add(embed_layer)
    # add other layers
    model.add(Dropout(0.25))  # (not sure if needed)
    model.add(LSTM(50))

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    print(model.summary())
    return model


def create_embeddings(data, embeddings_path, vocab_path):
    model = Word2Vec(data, min_count=5,
                     window=5, sg=1, iter=25)
    weights = model.syn0
    # Save weights into embeddings_path
    vocab = dict([(k, v.index) for k, v in model.vocav.items()])
    # Save vocab into vocab_path
