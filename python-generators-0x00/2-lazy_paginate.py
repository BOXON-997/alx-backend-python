#!/usr/bin/python3
import seed

def paginate_users(page_size, offset):
    """
    Fetch a page of users from user_data table based on limit and offset.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily loads paginated user data from the database.
    Fetches the next page only when needed (lazy loading).
    Uses only ONE loop.
    """
    offset = 0
    while True:  # only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
