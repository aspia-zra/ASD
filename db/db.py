# Contains connection, Contains execute_query()
# azra made this, idk if this is correct, check with imaan

import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="db"
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, values=None):
        self.cursor.execute(query, values)
        self.conn.commit()

    def fetch_one(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def fetch_all(self, query, values=None):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()