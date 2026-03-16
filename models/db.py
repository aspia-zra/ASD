import sqlite3

class Database:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._connection = sqlite3.connect('pams.db')
            cls._connection.row_factory = sqlite3.Row
        return cls._instance

    def get_cursor(self):
        return self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def close(self):
        self._connection.close()