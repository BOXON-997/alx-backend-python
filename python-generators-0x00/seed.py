#!/usr/bin/python3
import mysql.connector
from mysql.connector import Error
import csv
import uuid

# -------------------------------
# 1️ Connect to MySQL server (no DB yet)
# -------------------------------
def connect_db():
    """Connects to MySQL server (without specifying a database)."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',         # ← use your MySQL username
            password='root'      # ← or your actual MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


# -------------------------------
# 2️ Create database ALX_prodev
# -------------------------------
def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


# -------------------------------
# 3️ Connect to ALX_prodev
# -------------------------------
def connect_to_prodev():
    """Connects directly to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='ALX_prodev'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


# -------------------------------
# 4️ Create table user_data
# -------------------------------
def create_table(connection):
    """Creates the user_data table if it doesn't exist."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,0) NOT NULL,
            INDEX idx_user_id (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


# -------------------------------
# 5️ Insert CSV data
# -------------------------------
def insert_data(connection, csv_file):
    """Inserts data into user_data table if not already present."""
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = int(row['age'])
                # Avoid duplicates by checking email
                cursor.execute("SELECT COUNT(*) FROM user_data WHERE email = %s;", (email,))
                exists = cursor.fetchone()[0]
                if exists == 0:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
                        (user_id, name, email, age)
                    )
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
