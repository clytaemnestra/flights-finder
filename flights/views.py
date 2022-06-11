from flask import Blueprint, render_template
from .queries import show_all_airports

app = Blueprint("app", __name__)


@app.route("/")
def homepage():
    """Shows homepage with input fields for queries."""
    return render_template("homepage.html")


@app.route("/results")
def results():
    """Shows all flight connections for given queries."""
    return render_template("results.html")


@app.route("/all-airports")
def homepage():
    """Shows homepage with input fields for queries."""
    all_airports = show_all_airports()
    return render_template("airports.html", all_airports=all_airports)
