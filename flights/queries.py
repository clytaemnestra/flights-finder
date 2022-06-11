from flights import get_db


def show_all_airports():
    """Returns all airports from the database."""
    db = get_db()
    result = db.run(
        "MATCH (a:Airline)-[:IS_INCORPORATED_IN]->(c:Country)"
        "RETURN a.name as Airline, a.iata as IATA,"
        " a.icao as ICAO, c.name as Country"
    )
    data = []
    for record in result:
        data.append(
            f"Name: {record['Airline']} - IATA: {record['IATA']} - ICAO: {record['ICAO']} - Country: {record['Country']}"
        )
    return data
