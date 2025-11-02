#!/usr/bin/python3
import seed
from mysql.connector import Error


def stream_user_ages():
    """
    Generator that streams user ages one by one from the user_data table.
    Uses yield to avoid loading all rows into memory.
    """
    try:
        connection = seed.connect_to_prodev()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data;")

        for row in cursor:  # Loop 1
            yield row["age"]

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming ages: {e}")
        return


def average_age():
    """
    Uses the stream_user_ages generator to compute the average user age
    in a memory-efficient way (no SQL AVG and no list storage).
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    if count > 0:
        avg = total_age / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No users found.")


# Allow direct execution for testing
if __name__ == "__main__":
    average_age()
