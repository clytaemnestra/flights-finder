from flights import get_db


def get_all_airlines():
    """Returns all airlines from the database."""
    db = get_db()
    result = db.run(
        "MATCH (a:Airline)-[:IS_INCORPORATED_IN]->(c:Country)"
        "RETURN a.name as Airline, a.iata as IATA,"
        " a.icao as ICAO, c.name as Country"
    )
    data = []
    for record in result:
        data.append(
            {
                "Name": record["Airline"],
                "IATA": record["IATA"],
                "ICAO": record["ICAO"],
                "Country": record["Country"],
            }
        )
    return data


def find_shortest_path(origin, destination):
    """Returns shortest flights from given origin to given destination."""
    db = get_db()
    query = (
        "MATCH p=shortestpath((src:Airport{{city: '{origin}'}})-[*..15]"
        "-(dest:Airport{{city: '{destination}'}})) "
        "WHERE ALL (i in range(0, size(relationships(p))-2) "
        "WHERE (relationships(p)[i]).date < (relationships(p)[i+1]).date) "
        "RETURN p".format(origin=origin, destination=destination)
    )

    result = db.run(query)
    path = ""
    for item in result:
        path = item["p"]
    relationships = path.relationships
    nodes = path.nodes
    path = ""
    for i in range(len(relationships)):
        if i % 2 == 0:
            path += f'{nodes[i]["name"]}, Departure time: {relationships[i]["date"]}, '
        else:
            path += f'Flight: {nodes[i]["number"]}, Arrival time: {relationships[i]["date"]} -> '
    path += destination
    if path.endswith("-> "):
        path = path[:-3]
    return path


def get_busiest_airports():
    "Returns list of busiest airports by number of flights."
    db = get_db()
    query = (
        "MATCH (airport:Airport)<-[:DEPARTS_AT]-(f:Flight) "
        "WITH airport, count(f) as departures "
        "MATCH (f2:Flight)-[:ARRIVES_AT]->(airport)"
        "RETURN airport.name as airport_name, departures, "
        "count(f2) as arrivals "
        "ORDER BY departures DESC"
    )
    result = db.run(query)
    airports = []
    for record in result:
        airports.append(
            {
                "Name": record["airport_name"],
                "Departures": record["departures"],
                "Arrivals": record["arrivals"],
            }
        )
    return airports
