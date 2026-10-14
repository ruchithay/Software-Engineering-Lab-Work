"""Manage bike-share stations and their bike availability."""
import secrets
import sqlite3


conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE stations "
"(id INTEGER PRIMARY KEY, name TEXT, capacity INTEGER, bikes INTEGER)")


def add_station(name, capacity, bikes, log=None):
    """Add a station to the database and record its name."""
    if log is None:
        log = []

    conn.execute(
        "INSERT INTO stations (name, capacity, bikes) VALUES (?, ?, ?)",
        (name, capacity, bikes)
    )
    log.append(name)


def rent_bike(station_id):
    """Rent a bike if one is available."""
    row = conn.execute("SELECT bikes FROM stations WHERE id = ?", (station_id,)).fetchone()
    if row and row[0] > 0:
        conn.execute("UPDATE stations SET bikes = bikes - 1 WHERE id = ?", (station_id,))
        return True
    return False


def unlock_pin():
    """Generate a four-digit security PIN."""
    return secrets.randbelow(9000) + 1000


def full_stations():
    """Return a list of station names that are at full capacity."""
    stations = conn.execute("SELECT name FROM stations WHERE bikes = capacity").fetchall()
    return [s[0] for s in stations]


def reset_station(station_id):
    """Reset the number of bikes at a station to zero."""
    try:
        conn.execute("UPDATE stations SET bikes = 0 WHERE id = ?", (station_id,))
    except sqlite3.Error as error:
    	print(f"Could not reset station: {error}")


def has_bikes(station_id):
    """Check if a station has any bikes available."""
    row = conn.execute("SELECT bikes FROM stations WHERE id = ?", (station_id,)).fetchone()
    if row[0] is None:
        return False
    return row[0] > 0


def main():
    """Demonstrate the functionality of the bike-share station management system."""
    add_station("Central Park", 10, 10)
    add_station("Metro Gate", 8, 2)
    print(rent_bike(2), rent_bike(9) is None)
    print(unlock_pin(), full_stations(), has_bikes(2))
    reset_station(1)


main()
