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

    def add_task(self, task):
        self.cursor.execute("""
            INSERT INTO tasks(
                title,
                subject,
                estimated_minutes,
                priority,
                deadline,
                completed
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            task.title,
            task.subject,
            task.estimated_minutes,
            task.priority,
            task.deadline,
            int(task.is_completed)
        ))

        self.connection.commit()

    def delete_task_by_title(self, title):
        self.cursor.execute(
            "DELETE FROM tasks WHERE title = ?",
            (title,)
        )

        self.connection.commit()
    
    def get_tasks(self):
        self.cursor.execute("SELECT * FROM tasks")

        return self.cursor.fetchall()
    
    def clear_tasks(self): #for now
        self.cursor.execute("DELETE FROM tasks")
        self.connection.commit()

    