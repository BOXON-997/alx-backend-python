import sqlite3
import functools
from datetime import datetime  # Required for timestamp logging


# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract SQL query from args or kwargs
        query = kwargs.get("query") if "query" in kwargs else args[0] if args else None

        # Log the query with timestamp
        if query:
            print(f"[{datetime.now()}] Executing SQL Query: {query}")
        else:
            print(f"[{datetime.now()}] No SQL query found.")

        # Execute the original function
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#  Fetch users while logging the queries
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
