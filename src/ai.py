"""@package AI
The Ai module implements the core ai functions

More details....
"""
import multiprocessing
import pickle
from collections import Counter

import numpy as np
import scipy.sparse as sp
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D, BatchNormalization
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

import db
from NLP import text_precessing, text_precessing_char, basic_precessing, basic_precessing_char


def analyse_text(text, modelname="logistic_regression"):
    dbobj = db.DB()
    model = pickle.loads(dbobj.get_model_in_db(modelname)[0][0])
    name = modelname + "_vect"
    vectorizer = pickle.loads(dbobj.get_model_in_db(name)[0][0])
    return str(model.predict(vectorizer.transform([text])))


def analyse_ad_lstm(modelname):
    """
    model = load_model("beste_gewichten.hdf5",compile=False)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    name = "lstm_word"
    print(name)
    print("normal data with lstm word")

    print("tokenize + word embeddings")

    tokenizer.fit_on_texts(preprocessedData)
    x = tokenizer.texts_to_sequences(preprocessedData)
    x = pad_sequences(x, maxlen=500)
    print("predicting")
    predictions = model.predict(x)
    print(predictions)
    rounded_predictions = np.argmax(predictions, axis=-1)
    cm = confusion_matrix(y_true=hate, y_pred=rounded_predictions)
    print(cm)
    with open(name, 'w') as f:
        f.write(str(cm))
        """
    if (modelname == "lstm_les"):
        dbobj = db.DB()

        tokenizer = Tokenizer(num_words=10000, lower=True, filters=None, char_level=True)
        tweet = [i[0] for i in dbobj.db_load_extra_tweet()]
        hate = [i[0] for i in dbobj.db_load_extra_hate()]
        hate = np.asarray(hate)
        preprocessedData = [text_precessing_char(text) for text in tweet]
        print("done")
        x = tokenizer.texts_to_sequences(preprocessedData)
        x = pad_sequences(x, maxlen=300)
        model = load_model("lstm_les.hdf5")
        predictions = model.predict_classes(x)
        print(predictions)
        accuracy = model.evaluate(x, hate)
        print(accuracy)
        cm = confusion_matrix(y_true=hate, y_pred=predictions)
        print(cm)
        with open(modelname + "_matrix.txt", 'w') as f:
            f.write(str(cm))


def analyse_ad():
    dbobj = db.DB()

    model = pickle.loads(dbobj.get_model_in_db("logistic_regression_char")[0][0])
    name = "logistic_regression_char_vect"
    vectorizer = pickle.loads(dbobj.get_model_in_db(name)[0][0])

    print("normal data with logistic char")
    tweet = [i[0] for i in dbobj.db_load_extra_tweet()]
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

    # naive_bayes

    model = pickle.loads(dbobj.get_model_in_db("naive_bayes")[0][0])
    name = "naive_bayes_vect"
    vectorizer = pickle.loads(dbobj.get_model_in_db(name)[0][0])

    print("normal data with naive bayes")
    tweet = [i[0] for i in dbobj.db_load_extra_tweet()]
    predictions = model.predict(vectorizer.transform(tweet))
    hate = [i[0] for i in dbobj.db_load_extra_hate()]
    print("confusion matrix")
    matrix = confusion_matrix(predictions, hate)
    name = "extra_naive_bayes_confusion_matrix"
    print(accuracy_score(predictions, hate, normalize=True))
    with open(name, 'w') as f:
        f.write(str(matrix))

    print("ad data with naive bayes")
    tweet = [i[0] for i in dbobj.db_load_ad_tweet()]
    predictions = model.predict(vectorizer.transform(tweet))
    hate = [i[0] for i in dbobj.db_load_ad_hate()]
    print("confusion matrix")
    matrix = confusion_matrix(predictions, hate)
    name = "ad_naive_bayes_confusion_matrix"
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
        tokenizer = Tokenizer(num_words=10000, lower=True, filters="", char_level=False)
        construct_lstm(data, hate, tokenizer, modelname)
    elif modelname == "lstm_char":
        tokenizer = Tokenizer(num_words=10000, lower=True, filters="", char_level=True)
        construct_lstm(data, hate, tokenizer, modelname)
    elif modelname == "lstm_les":
        tokenizer = Tokenizer(num_words=10000, lower=True, filters="", char_level=False)
        construct_lstm_les(data, hate, tokenizer, modelname)
    elif modelname == "lstm_tibo":
        construct_lstm_tibo(data, hate, modelname)
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
    elif modelname == "naive_bayes":
        vectorizer = TfidfVectorizer(preprocessor=text_precessing_char,
                                     max_df=0.75, min_df=5, use_idf=True, smooth_idf=False, ngram_range=(1, 3),
                                     norm=None, decode_error="replace")
        naive_bayes(vectorizer, data, hate, modelname)


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


def naive_bayes(vectorizer, data, hate, modelname):
    dbobj = db.DB()
    """Construct a db entry. Avoid using old model for requests made before ending of model construction"""
    dbobj.constructing_model_in_db(modelname)
    print("Splitting data into train & test")
    x_train, x_test, y_train, y_test = train_test_split(data, hate, train_size=0.7, random_state=42)
    print(f"training on a size of {len(x_train)}")
    print("fitting training")
    vect = vectorizer.fit(x_train)
    print("transforming training")
    params = [{}]
    # x_train_vectorized = vect.transform(x_train)
    x_train_vectorized = parallel_construct(x_train, vect.transform)
    dbobj.insert_vect_in_db(modelname, pickle.dumps(vect))
    model = MultinomialNB(alpha=1)
    print("initing model")
    model.fit(x_train_vectorized, y_train)
    print("Model made")
    predictions = model.predict(vect.transform(x_test))
    name_one = modelname + "_predictions"
    with open(name_one, 'w') as f:
        for i in predictions:
            f.write(str(i))
    dbobj.insert_model_in_db(modelname, pickle.dumps(model))
    matrix = confusion_matrix(predictions, y_test)
    name = modelname + "_confusion_matrix"
    print(accuracy_score(predictions, y_test, normalize=True))
    with open(name, 'w') as f:
        f.write(str(matrix))


def construct_lstm(data, hate, tokenizer, modelname, maxlen=500):
    dbobj = db.DB()
    # Preprocess text (& join on space again :§
    # max features: top most frequently used words.
    # maxlen, how long can an inputtext be (will be truncated if longer)
    dbobj.constructing_model_in_db("lstm")

    data = [i[0] for i in dbobj.db_load_extra_tweet()]
    hate = [i[0] for i in dbobj.db_load_extra_hate()]

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
    return model


def construct_lstm_tibo(data, hate, modelname):
    # code gebasseerd op https://www.youtube.com/watch?v=j7EB7yeySDw
    dbobj = db.DB()
    hate = np.asarray(hate)
    dbobj.constructing_model_in_db("lstm_tibo")
    print("constructing tibo lstm")
    data = [text_precessing_char(t) for t in data]
    print("Data done")
    print("split")
    x_train, x_test, y_train, y_test = train_test_split(data, hate, train_size=0.7, random_state=42)
    print("count")
    counter = Counter()
    for i in data:
        for word in i.split():
            counter[word] += 1
    num_words = len(counter)
    max_words = 25
    print("tokenizing")
    tokenizer = Tokenizer(num_words=num_words)
    tokenizer.fit_on_texts(x_train)
    seq_train = tokenizer.texts_to_sequences(x_train)
    seq_test = tokenizer.texts_to_sequences(x_test)
    print("padding")
    padded = pad_sequences(seq_train, maxlen=max_words, padding='post', truncating='post')
    test_padded = pad_sequences(seq_test, maxlen=max_words, padding='post', truncating='post')
    model = Sequential()
    model.add(Embedding(num_words, 32, input_length=max_words))
    model.add(LSTM(64, dropout=0.1))
    model.add(Dense(1, activation='sigmoid'))
    optimizer = Adam(learning_rate=3e-4)
    model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy"])
    mcp = ModelCheckpoint(modelname + ".hdf5", monitor="val_accuracy", save_best_only=True, save_weights_only=False)
    model.fit(padded, y_train, epochs=20, validation_data=(test_padded, y_test), callbacks=[mcp])

    model.load(modelname + ".hdf5")

    # testing, predicting
    print("loading new dataset")
    tweet = [i[0] for i in dbobj.db_load_extra_tweet()]
    hate = [i[0] for i in dbobj.db_load_extra_hate()]
    preprocessedData = [text_precessing_char(text) for text in tweet]
    print("done")
    x = tokenizer.texts_to_sequences(preprocessedData)
    x = pad_sequences(x, maxlen=max_words, padding='post', truncating='post')
    predictions = model.predict_classes(x)
    cm = confusion_matrix(y_true=hate, y_pred=predictions)
    print(cm)
    name = "extra_" + modelname + "_confusion_matrix"
    with open(name, 'w') as f:
        f.write(str(cm))

    # testing, predicting
    print("loading new dataset")
    tweet = [text_precessing_char(i[0]) for i in dbobj.db_load_ad_tweet()]
    hate = [i[0] for i in dbobj.db_load_ad_hate()]
    print("done")
    x = tokenizer.texts_to_sequences(tweet)
    x = pad_sequences(x, maxlen=max_words, padding='post', truncating='post')
    predictions = model.predict_classes(x)
    cm = confusion_matrix(y_true=hate, y_pred=predictions)
    print(cm)
    name = "ad_" + modelname + "_confusion_matrix"
    with open(name, 'w') as f:
        f.write(str(cm))


def construct_lstm_les(data, hate, tokenizer, modelname, maxlen=500):
    dbobj = db.DB()
    # Preprocess text (& join on space again :§
    # max features: top most frequently used words.
    # maxlen, how long can an inputtext be (will be truncated if longer)

    dbobj.constructing_model_in_db("lstm")
    # KERAS tokenizer (SETS INTO INTEGERS/ VECTORS INSTEAD OF WORDS)
    preprocessedData = [text_precessing_char(text) for text in data]

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
    # mcp = ModelCheckpoint(modelname + ".hdf5", monitor="val_accuracy", save_best_only=True, save_weights_only=False)
    model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test),
              callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)])

    accuracy = model.evaluate(x_test, y_test)
    model.save("lstm_les.hdf5")
    print(accuracy)
    return model


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
    model.add(BatchNormalization())
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # Dit zorgt voor output in het juiste format van ons NN
    return model
