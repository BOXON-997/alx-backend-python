import sqlite3
import functools

#  Reuse the with_db_connection decorator from previous task
def with_db_connection(func):
    """Decorator that handles opening and closing a database connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


#  New transactional decorator
def transactional(func):
    """Decorator that manages database transactions (commit or rollback)."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit changes if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback if an error occurs
            print(f"[ERROR] Transaction failed: {e}")
            raise  # Re-raise the exception for visibility
    return wrapper


@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))


#  Test example
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print(" User email updated successfully (if user exists).")
