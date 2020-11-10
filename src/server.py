"""@package server
Provides the api routes and calls ai functions. With this we can implement an webinterface.

More details.
"""

from demoji import download_codes
from flask import Flask, jsonify, request
from nltk import download

import ai
from db import DB

app = Flask(__name__)
database = DB()
data = database.db_load()


@app.route('/api/analyse', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        return ai.analyse_text(request.json["message"],data)
    else:
        return jsonify("Hello, this is the ai speaking. the ai hate you already and you are going to hate it :) ")


@app.route('/api/validate', methods=['GET', 'POST'])
def validate():
    if request.method == 'POST':
        # request.form['username']
        return ai.validate()
    else:
        return jsonify("Hello, the ai thanks you for the lesson!")


@app.route('/api/preprocess', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        return ai.process_text(request.json["message"])
    else:
        return jsonify("Hello, the ai thanks you for the lesson!")


@app.route('/api/init', methods=['GET'])
def init():
    download('wordnet')
    download('stopwords')
    download('averaged_perceptron_tagger')
    download_codes()
    return str("inited")


@app.route('/api/data', methods=['GET'])
def showdata():
    return str(data)
