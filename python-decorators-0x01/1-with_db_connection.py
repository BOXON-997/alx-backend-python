import sqlite3
import functools 

def with_db_connection(func):
    """Decorator thta handles opening and closing a database connection. """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open a database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection aas the first argument to the function
            result = func(conn, *args, **kwargs)
        finally:
            # Always close the connection, even if an error occurs 
            conn.close()
        return result
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email ? WHERE id = ?", (new_email, user_id))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print(user)