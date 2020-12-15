"""@package AI
The Ai module implements the core ai functions

More details....
"""
import multiprocessing
import pickle

import numpy as np
import scipy.sparse as sp
from keras.callbacks import ModelCheckpoint
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline

import db
from NLP import text_precessing, text_precessing_char, basic_precessing, basic_precessing_char


def analyse_text(text, modelname="logistic_regression"):
    dbobj = db.DB()
    model = pickle.loads(dbobj.get_model_in_db(modelname)[0][0])
    name = modelname + "_vect"
    vectorizer = pickle.loads(dbobj.get_model_in_db(name)[0][0])
    return str(model.predict(vectorizer.transform([text])))


def analyse_ad():
    dbobj = db.DB()

    model = pickle.loads(dbobj.get_model_in_db("logistic_regression_char")[0][0])
    name = "logistic_regression_char_vect"
    vectorizer = pickle.loads(dbobj.get_model_in_db(name)[0][0])

    print("normal data with logistic char")
    tweet = [i[0] for i in dbobj.db_load_extra_tweet()]
    print("got here")
    predictions = model.predict(vectorizer.transform(tweet))
    hate = [i[0] for i in dbobj.db_load_extra_hate()]
    print("confusion matrix")
    matrix = confusion_matrix(predictions, hate)
    name = "extra_logistic_regression_char_confusion_matrix"
    print(accuracy_score(predictions, hate, normalize=True))
    with open(name, 'w') as f:
        f.write(str(matrix))

    print("ad data with logistic char")
    tweet = [i[0] for i in dbobj.db_load_ad_tweet()]
    predictions = model.predict(vectorizer.transform(tweet))
    hate = [i[0] for i in dbobj.db_load_ad_hate()]
    print("confusion matrix")
    matrix = confusion_matrix(predictions, hate)
    name = "ad_logistic_regression_char_confusion_matrix"
    print(accuracy_score(predictions, hate, normalize=True))
    with open(name, 'w') as f:
        f.write(str(matrix))



    model = pickle.loads(dbobj.get_model_in_db("logistic_regression")[0][0])
    name = "logistic_regression_vect"
    vectorizer = pickle.loads(dbobj.get_model_in_db(name)[0][0])

    print("normal data with logistic word")
    tweet = [i[0] for i in dbobj.db_load_extra_tweet()]
    print("got here")
    predictions = model.predict(vectorizer.transform(tweet))
    hate = [i[0] for i in dbobj.db_load_extra_hate()]
    print("confusion matrix")
    matrix = confusion_matrix(predictions, hate)
    name = "extra_logistic_regression_confusion_matrix"
    print(accuracy_score(predictions, hate, normalize=True))
    with open(name, 'w') as f:
        f.write(str(matrix))

    print("ad data with logistic word")
    tweet = [i[0] for i in dbobj.db_load_ad_tweet()]
    predictions = model.predict(vectorizer.transform(tweet))
    hate = [i[0] for i in dbobj.db_load_ad_hate()]
    print("confusion matrix")
    matrix = confusion_matrix(predictions, hate)
    name = "ad_logistic_regression_confusion_matrix"
    print(accuracy_score(predictions, hate, normalize=True))
    with open(name, 'w') as f:
        f.write(str(matrix))


def process_text(text):
    return str(text_precessing(text.lower()))


def return_token(text):
    return text


def validate_ai():
    return "Hello, the ai thanks you for the lesson!"


def construct_model(data, hate, modelname="logistic_regression"):
    print(modelname)
    if modelname == "logistic_regression":
        vectorizer = TfidfVectorizer(preprocessor=text_precessing, tokenizer=return_token,
                                     max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3),
                                     norm=None, decode_error="replace")
        logistic(vectorizer, data, hate, modelname)
    elif modelname == "logistic_regression_char":
        vectorizer = TfidfVectorizer(preprocessor=text_precessing_char, max_df=0.75, min_df=5, use_idf=True,
                                     smooth_idf=False, ngram_range=(1, 3), norm=None, decode_error="replace",
                                     analyzer="char")
        logistic(vectorizer, data, hate, modelname)
    elif modelname == "lstm":
        tokenizer = Tokenizer(num_words=10000, lower=True, filters=None, char_level=False)
        construct_lstm(data, hate, tokenizer, modelname)
    elif modelname == "lstm_char":
        tokenizer = Tokenizer(num_words=10000, lower=True, filters=None, char_level=True)
        construct_lstm(data, hate, tokenizer, modelname)
    elif modelname == "lstm_les":
        tokenizer = Tokenizer(num_words=10000, lower=True, filters=None, char_level=False)
        construct_lstm_les(data, hate, tokenizer, modelname)
    elif modelname == "log_basic":
        vectorizer = TfidfVectorizer(preprocessor=basic_precessing, tokenizer=return_token,
                                     max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3),
                                     norm=None, decode_error="replace")
        logistic(vectorizer, data, hate, modelname)

    elif modelname == "log_basic_char":
        vectorizer = TfidfVectorizer(preprocessor=basic_precessing_char,
                                     max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3),
                                     norm=None, decode_error="replace")
        logistic(vectorizer, data, hate, modelname)


def logistic(vectorizer, data, hate, modelname):
    dbobj = db.DB()
    """Construct a db entry. Avoid using old model for requests made before ending of model construction"""
    dbobj.constructing_model_in_db(modelname)
    print("Splitting data into train & test")
    x_train, x_test, y_train, y_test = train_test_split(data, hate, train_size=0.7, random_state=42)
    print(f"training on a size of {len(x_train)}")
    print("fitting training")
    vect = vectorizer.fit(x_train)
    print("transforming training")
    # x_train_vectorized = vect.transform(x_train)
    x_train_vectorized = parallel_construct(x_train, vect.transform)

    dbobj.insert_vect_in_db(modelname, pickle.dumps(vect))
    params = [{}]
    pipe = Pipeline([('select', SelectFromModel(LogisticRegression(n_jobs=-1, max_iter=1e5))),
                     ('model', LogisticRegression(n_jobs=-1, max_iter=1e5))])
    model = GridSearchCV(pipe, params, cv=StratifiedKFold(n_splits=5).split(x_train, y_train))
    print("initing model")
    model = model.fit(x_train_vectorized, y_train)
    print("Model made")
    predictions = model.predict(vect.transform(x_test))
    name_one = modelname + "_predictions"
    with open(name_one, 'w') as f:
        for i in predictions:
            f.write(str(i))
    dbobj.insert_model_in_db(modelname, pickle.dumps(model.best_estimator_))
    matrix = confusion_matrix(predictions, y_test)
    name = modelname + "_confusion_matrix"
    print(accuracy_score(predictions, y_test, normalize=True))
    with open(name, 'w') as f:
        f.write(str(matrix))


def parallel_construct(data, func):
    core_count = multiprocessing.cpu_count() - 1
    print(f"working on {core_count} threads")

    data_split = np.array_split(data, core_count)
    pool = multiprocessing.Pool(core_count)

    df = sp.vstack(pool.map(func, data_split), format='csr')
    pool.close()
    pool.join()
    return df


def construct_lstm(data, hate, tokenizer, modelname, maxlen=500):
    dbobj = db.DB()
    # Preprocess text (& join on space again :§
    # max features: top most frequently used words.
    # maxlen, how long can an inputtext be (will be truncated if longer)
    dbobj.constructing_model_in_db("lstm")
    hate = np.asarray(hate)
    # KERAS tokenizer (SETS INTO INTEGERS/ VECTORS INSTEAD OF WORDS)
    preprocessedData = np.asarray([text_precessing_char(text) for text in data])

    print("tokenize + word embeddings")

    tokenizer.fit_on_texts(preprocessedData)
    word_index = tokenizer.word_index  # len(word_index) == aantal tokens als we dat willen zien
    print('Found %s unique tokens.' % len(word_index))
    x = tokenizer.texts_to_sequences(preprocessedData)
    x = pad_sequences(x, maxlen=maxlen)
    print(f"Shape of tensor is: {x.shape}")
    # Y = ? pd.get_dummies(data) #(getten labels -> numbers (dus bij ons 0 en 1?))
    # shape van Y zou dan (X.shape[0], (1 of 2) moeten zijn

    # train test split
    model = make_lstm_model(x.shape[1])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    epochs = 20  # Zal waarschijnlijk hoger moeten, is het aantal keren dat het traint kinda
    batch_size = 64
    x_train, x_test, y_train, y_test = train_test_split(x, hate, train_size=0.7, random_state=42)
    mcp = ModelCheckpoint(modelname + ".hdf5", monitor="val_accuracy", save_best_only=True, save_weights_only=False)
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
              callbacks=[mcp])
    # callbacks=[        EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)]

    accuracy = model.evaluate(x_test, y_test)
    print(accuracy)


def construct_lstm_les(data, hate, tokenizer, modelname, maxlen=500):
    dbobj = db.DB()
    # Preprocess text (& join on space again :§
    # max features: top most frequently used words.
    # maxlen, how long can an inputtext be (will be truncated if longer)
    dbobj.constructing_model_in_db("lstm")
    hate = np.asarray(hate)
    # KERAS tokenizer (SETS INTO INTEGERS/ VECTORS INSTEAD OF WORDS)
    preprocessedData = np.asarray([text_precessing_char(text) for text in data])

    print("tokenize + word embeddings")

    tokenizer.fit_on_texts(preprocessedData)
    word_index = tokenizer.word_index  # len(word_index) == aantal tokens als we dat willen zien
    print('Found %s unique tokens.' % len(word_index))
    x = tokenizer.texts_to_sequences(preprocessedData)
    x = pad_sequences(x, maxlen=maxlen)
    print(f"Shape of tensor is: {x.shape}")
    # Y = ? pd.get_dummies(data) #(getten labels -> numbers (dus bij ons 0 en 1?))
    # shape van Y zou dan (X.shape[0], (1 of 2) moeten zijn

    # train test split
    model = make_lstm_les_model(len(tokenizer.word_index) + 1)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.summary()

    epochs = 20  # Zal waarschijnlijk hoger moeten, is het aantal keren dat het traint kinda
    batch_size = 64
    x_train, x_test, y_train, y_test = train_test_split(x, hate, train_size=0.7, random_state=42)
    mcp = ModelCheckpoint(modelname + ".hdf5", monitor="val_accuracy", save_best_only=True, save_weights_only=False)
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
              callbacks=[mcp])
    # callbacks=[        EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)]

    accuracy = model.evaluate(x_test, y_test)
    print(accuracy)


def make_lstm_model(x):
    model = Sequential()
    embed_layer = Embedding(50000, 100, input_length=x)
    model.add(embed_layer)
    # add other layers
    model.add(SpatialDropout1D(0.2))  # (not sure if needed)
    model.add(LSTM(250, dropout=0.2, recurrent_dropout=0.2))
    model.add(Dense(2, activation='softmax'))  # Dit zorgt voor output in het juiste format van ons NN
    return model


def make_lstm_les_model(x):
    model = Sequential()
    embed_layer = Embedding(x, 64, input_length=300)
    model.add(embed_layer)
    model.add(LSTM(32))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Dit zorgt voor output in het juiste format van ons NN
    return model

