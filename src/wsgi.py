"""@package wsgi
entry for Gunicorn to run the flask server as a service on the server.
"""

from server import app
import nltk
import demoji

if __name__ == "__main__":
    nltk.download('wordnet')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')
    demoji.download_codes()
    app.run()
