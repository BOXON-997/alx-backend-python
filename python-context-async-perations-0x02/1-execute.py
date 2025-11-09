import sqlite3


class ExecuteQuery:
    """Custom reusable context manager to handle DB connection and query execution."""

    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open DB connection and execute the query."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection safely."""
        if self.conn:
            self.conn.close()


# Use the reusable context manager
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        print(results)

# Objective: create a reusable context manager that takes a query as input and executes it, managing both connection and the query execution

# Instructions:

#     Implement a class based custom context manager ExecuteQuery that takes the query: ”SELECT * FROM users WHERE age > ?” and the parameter 25 and returns the result of the query

#     Ensure to use the__enter__() and the __exit__() methods
