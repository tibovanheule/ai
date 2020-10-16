from flask import Flask, jsonify, request 
import ai

app = Flask(__name__)

@app.route('/api/analyse', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        #request.form['username']
        return ai.analyse_text()
    else:
        return jsonify("Hello, this is the ai speaking. the ai hate you already and you are going to hate it :) ") 


@app.route('/api/validate', methods=['GET', 'POST'])
def validate():
    if request.method == 'POST':
        #request.form['username']
        return ai.validate()
    else:
        return jsonify("Hello, the ai thanks you for the lesson!") 
