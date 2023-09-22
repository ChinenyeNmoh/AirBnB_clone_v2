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


@app.route("/states", strict_slashes=False)
def route1():
    """Displays an HTML with a list of all States.
    """
    dictionary = storage.all("State")
    return render_template("9-states.html", state=dictionary)


# it works whithout specify uuid:id type in the route.
@app.route("/states/<id>", strict_slashes=False)
def route2(id):
    """Displays an HTML with info about <id> (only if exists)"""
    for dictionary in storage.all("State").values():
        if dictionary.id == id:
            return render_template("9-states.html", state=dictionary)

    # if the given id was not found, then:
    return render_template("9-states.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
