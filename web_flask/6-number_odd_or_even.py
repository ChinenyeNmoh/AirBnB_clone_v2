#!/usr/bin/python3
""" create a flask application """


from flask import Flask, request, render_template

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
    """ display C followed by a text given in a text variable"""
    return 'C ' + text.replace('_', ' ')


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """ display Python followed by a text given in a text variable"""
    text = text.replace('_', ' ')
    return f"Python {text}"


@app.route('/number/<int:n>', strict_slashes=False)
def integer(n):
    """displays number only if integer"""
    if isinstance(n, int):
        return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def integer_template(n):
    """displays number only if integer"""
    if isinstance(n, int):
        return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_even(n):
    """display odd or even number"""
    if isinstance(n, int):
        if n % 2 == 0:
            res = "even"
        else:
            res = "odd"
    return render_template('6-number_odd_or_even.html', n=n, res=res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
