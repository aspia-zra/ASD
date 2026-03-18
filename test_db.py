from models.db import Database

db = Database()
cursor = db.get_cursor()
if cursor:
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Tables found:", [t[0] for t in tables])
else:
    print("Connection failed")