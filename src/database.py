import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("studyplanner.db")
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                subject TEXT,
                estimated_minutes INTEGER,
                priority INTEGER,
                deadline TEXT,
                completed INTEGER
            )
        """)

        self.connection.commit()