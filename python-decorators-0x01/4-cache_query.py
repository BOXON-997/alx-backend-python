import time
import sqlite3
import functools

# Global cache dictionary
query_cache = {}

# Reuse with_db_connection from previous tasks
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


# Cache decorator
def cache_query(func):
    """Decorator that caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query string (either from kwargs or first positional arg)
        query = kwargs.get("query") if "query" in kwargs else args[1] if len(args) > 1 else None

        if query in query_cache:
            print(f"[CACHE HIT] Returning cached result for query: {query}")
            return query_cache[query]

        print(f"[CACHE MISS] Executing and caching result for query: {query}")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#  First call will cache the result
if __name__ == "__main__":
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)
