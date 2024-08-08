import mysql.connector
from config import db_host, db_name, db_user, db_pass

def connect():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            database=db_name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
