from flask import Flask, jsonify
import ai

app = Flask(__name__)

@app.route('/api/analyze')
def analyze():
    return ai.analyze_text()

@app.route('/api/validate')
def validate():
    return ai.validate()

@app.errorhandler(404)
def page_not_found(e):
    return '404.html'
