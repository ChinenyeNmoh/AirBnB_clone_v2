#!/usr/bin/python3
"""
starts a Flask web app.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Removes current SQLAlchemy session."""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def route1():
    """Display HTML page with a list of
    all objects inside a DBstorage."""
    url = '8-cities_by_states.html'
    dictionary = storage.all("State")
    return render_template(url, states=dictionary)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")
