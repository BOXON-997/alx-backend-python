import sqlite3 

class DatabaseConnection:
    """Custom class-based context manager for handling database connections. """

    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None 

    def __enter__(self):
        """Open the database connection when entering the context. """
        self.conn = sqlite3.connect(self.db_name)
        return self.conn 
    
    def __exit__(self, exc_type, exc_valueq, traceback):
        """Close tyhe database connection when exiting the context."""
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    with DatabaseConnection("users.db") as conmn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetrchall()
        print(results)


# Objective: create a class based context manager to handle opening and closing database connections automatically

# Instructions:

#     Write a class custom context manager DatabaseConnection using the __enter__ and the __exit__ methods

#     Use the context manager with the with statement to be able to perform the query SELECT * FROM users. Print the results from the query.
