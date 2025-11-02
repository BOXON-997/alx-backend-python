#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator that connects to the ALX_prodev database and streams
    rows from the user_data table one by one.
    Uses a single loop and yields each row as a dictionary.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',         # change if your MySQL username differs
            password='root',     # change if your password differs
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            for row in cursor:   # only one loop
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error streaming data: {e}")
        return
