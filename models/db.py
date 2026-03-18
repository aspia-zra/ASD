import mysql.connector
from mysql.connector import Error

class Database:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try:
                cls._connection = mysql.connector.connect(
                    host='127.0.0.1',
                    port=3306,
                    user='root',
                    password='root1234',           
                    database='asd_paragon'
                )
                print("✅ Connected to MySQL")
            except Error as e:
                print(f"❌ Connection error: {e}")
                cls._connection = None
        return cls._instance

    def get_cursor(self):
        if self._connection and self._connection.is_connected():
            return self._connection.cursor()
        return None

    def commit(self):
        if self._connection:
            self._connection.commit()

    def close(self):
        if self._connection:
            self._connection.close()