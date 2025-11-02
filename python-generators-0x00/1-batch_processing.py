#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from the user_data table in batches.
    Uses only one loop and yields lists of user dicts per batch.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',         # change if different
            password='root',     # change if different
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                yield rows  # yield one batch at a time

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error streaming batches: {e}")
        return


def batch_processing(batch_size):
    """
    Processes batches from stream_users_in_batches and prints
    users whose age > 25. Must use no more than 3 loops total.
    """
    for batch in stream_users_in_batches(batch_size):        # 1️ loop over batches
        for user in batch:                                   # 2️ loop over users in each batch
            if user['age'] > 25:
                yield user                                   #  generator yield instead of returning


# Optional: allow running directly for quick testing
if __name__ == "__main__":
    for user in batch_processing(50):
        print(user)
