#!/usr/bin/python3
""" create a flask application """


from flask import Flask, request

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """ display Hello HBNB! """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnh():
    """ display HBNB """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def cisfun(text):
    """Displays /c/<text>"""
    text = text.replace('_', ' ')
    return f"C {text}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
