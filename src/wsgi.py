"""@package wsgi
entry for Gunicorn to run the flask server as a service on the server.
"""

from server import app


if __name__ == "__main__":
    app.run()
