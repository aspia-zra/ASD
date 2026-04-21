# import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Dragonfruit23**",
        database="secondverparagonapartment"
    )

def getconnection():
    return get_connection()
