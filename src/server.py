"""@package server
Provides the api routes and calls ai functions. With this we can implement an webinterface.

More details.
"""

from flask import Flask, jsonify, request
import ai
import nltk
import demoji

app = Flask(__name__)


@app.route('/api/analyse', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        return ai.analyse_text(request.json["message"])
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
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    demoji.download_codes()
    return str("inited")
