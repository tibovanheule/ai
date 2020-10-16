from flask import Flask, jsonify
import ai

app = Flask(__name__)

@app.route('/ai/analyze')
def analyze():
    return ai.analyze_text()

@app.route('/ai/validate')
def analyze():
    return ai.validate()

@app.errorhandler(404)
def page_not_found(e):
    return '404.html'
