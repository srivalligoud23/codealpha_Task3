import sqlite3

DATABASE = "bus_pass.db"


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_passes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            passenger_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            pass_type TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()