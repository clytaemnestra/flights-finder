from flask import Blueprint, render_template, request
from .queries import get_all_airlines, find_shortest_path, get_busiest_airports

app = Blueprint("app", __name__)


@app.route("/")
def homepage():
    """Shows homepage with input fields for queries."""
    return render_template("homepage.html")


@app.route("/results", methods=["GET", "POST"])
def results():
    """Shows the fastest flight connections for given queries."""
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    try:
        shortest_path = find_shortest_path(origin=origin, destination=destination)
        return render_template("flights.html", shortest_path=shortest_path)
    except:
        return render_template("no-connection.html")


@app.route("/all-airports")
def show_all_airports():
    """Shows list of all airlines."""
    airlines = get_all_airlines()
    return render_template("airlines.html", airlines=airlines)


@app.route("/busiest-airports")
def show_busiest_airports():
    "Shows list of busiest airports"
    busiest_airports = get_busiest_airports()
    return render_template("busiest-airports.html", busiest_airports=busiest_airports)
