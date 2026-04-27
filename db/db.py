#Imaan Mohamed - 23015907 
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root123456!",
        database="sdgpdump"
    )

def getconnection():
    return get_connection()
