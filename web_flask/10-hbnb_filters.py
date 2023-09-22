#!/usr/bin/python3
"""
starts a Flask web app.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.route("/hbnb_filters", strict_slashes=False)
def route1():
    """Displays an HTML with a list of all States.
    """
    url = "10-hbnb_filters.html"
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template(url, states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
