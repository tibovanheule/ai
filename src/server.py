"""@package server
Provides the api routes and calls ai functions. With this we can implement an webinterface.

More details.
"""

from threading import Thread

from demoji import download_codes
from flask import Flask, jsonify, request
from nltk import download

from ai import construct_model, process_text, analyse_text, validate_ai
from db import DB

app = Flask(__name__)
database = DB()
tweets = [i[0] for i in database.db_load_tweet()]
hate = [i[0] for i in database.db_load_hate()]


@app.route('/api/analyse', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        return analyse_text(request.json["message"])
    return jsonify("Hello, this is the ai speaking. the ai hate you already and you are going to hate it :) ")


@app.route('/api/validate', methods=['POST'])
def validate():
    return validate_ai()


@app.route('/api/preprocess', methods=['POST'])
def process():
    return process_text(request.json["message"])


@app.route('/api/init', methods=['GET'])
def init():
    download('wordnet')
    download('words')
    download('stopwords')
    download('averaged_perceptron_tagger')
    download_codes()
    return str("inited")


@app.route('/api/data/tweets', methods=['GET'])
def showdata():
    return str(tweets)


@app.route('/api/data/hate', methods=['GET'])
def showhate():
    return str(hate)


@app.route('/api/model/init/', methods=['GET'])
def initmodel():
    thread = Thread(target=construct_model, kwargs={'data': tweets, 'hate': hate,
                                                    'modelname': request.args.get('modelname', "logistic_regression")})
    thread.start()
    return "Thread started, initing model"


@app.route('/api/model/init/small', methods=['GET'])
def initmodelsmall():
    thread = Thread(target=construct_model, kwargs={'data': tweets[:100], 'hate': hate[:100],
                                                    'modelname': request.args.get('modelname', "logistic_regression")})
    thread.start()
    return "Thread started, initing model"


@app.route('/api/model/init/medium', methods=['GET'])
def initmodelmedium():
    thread = Thread(target=construct_model, kwargs={'data': tweets[:1000], 'hate': hate[:1000],
                                                    'modelname': request.args.get('modelname', "logistic_regression")})
    thread.start()
    return "Thread started, initing model"


@app.route('/api/model/ready/', methods=['GET'])
def statusmodel():
    return str(DB().model_in_db(request.args.get('modelname', "logistic_regression")))
