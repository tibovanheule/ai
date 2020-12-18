"""@package server
Provides the api routes and calls ai functions. With this we can implement an webinterface.

More details.
"""

from threading import Thread

from demoji import download_codes
from flask import Flask, request
from nltk import download

from ai import construct_model, process_text, analyse_text
from db import DB

app = Flask(__name__)
database = DB()
tweets = [i[0] for i in database.db_load_tweet()]
hate = [i[0] for i in database.db_load_hate()]


@app.route('/api/analyse', methods=['POST'])
def analyze():
    """  analyse a tweet using logistic word model
    """
    return analyse_text(request.json["message"])


@app.route('/api/preprocess', methods=['POST'])
def process():
    """  Get a preprocesing of a tweet

    for debugging
    """
    return process_text(request.json["message"])


@app.route('/api/init', methods=['GET'])
def init():
    """  init the server and program

    download nesseary files for nlp
    """
    download('wordnet')
    download('words')
    download('stopwords')
    download('averaged_perceptron_tagger')
    download_codes()
    return str("inited")


@app.route('/api/data/tweets', methods=['GET'])
def showdata():
    """  give tweets present in the tweets database
    """
    return str(tweets)


@app.route('/api/data/hate', methods=['GET'])
def showhate():
    """  give tweets present in the tweets database
    """
    return str(hate)


@app.route('/api/model/init/', methods=['GET'])
def initmodel():
    """  init a model

    modelname is given by the url parameter "modelname"
    """
    thread = Thread(target=construct_model, kwargs={'data': tweets, 'hate': hate,
                                                    'modelname': request.args.get('modelname', "logistic_regression")})
    thread.start()
    return "Thread started, initing model"


@app.route('/api/model/init/small', methods=['GET'])
def initmodelsmall():
    """  init a model but with only a 100 tweets

    modelname is given by the url parameter "modelname"
    for debugging
    """
    thread = Thread(target=construct_model, kwargs={'data': tweets[:100], 'hate': hate[:100],
                                                    'modelname': request.args.get('modelname', "logistic_regression")})
    thread.start()
    return "Thread started, initing model"


@app.route('/api/model/init/medium', methods=['GET'])
def initmodelmedium():
    """  init a model but with only a 1000 tweets

    modelname is given by the url parameter "modelname"
    for debugging
    """
    thread = Thread(target=construct_model, kwargs={'data': tweets[:1000], 'hate': hate[:1000],
                                                    'modelname': request.args.get('modelname', "logistic_regression")})
    thread.start()
    return "Thread started, initing model"


@app.route('/api/model/ready/', methods=['GET'])
def statusmodel():
    """  give back if model is done building.
    """
    return str(DB().model_in_db(request.args.get('modelname', "logistic_regression")))
