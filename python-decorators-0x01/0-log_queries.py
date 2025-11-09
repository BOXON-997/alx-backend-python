import sqlite3
import functools 

#### decorator to log SQL queries 
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract SQL query from args and kwargs
        query = kwargs.get("query") if "query" in kwargs else [0] if args else None

        # Log the query
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print(f"[LOG] No SQL query found.")

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

# Fetch users while logging the quesries 
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)






