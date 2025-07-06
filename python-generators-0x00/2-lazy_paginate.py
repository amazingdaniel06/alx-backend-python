import mysql.connector

def paginate_users(page_size, offset):
    """
    Fetch a page of users from the user_data table
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='aswise?Ben10',   # change as needed
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    query = f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results


def lazy_paginate(page_size):
    """
    Generator to lazily paginate through user_data
    """
    offset = 0
    while True:   # one loop only
        page = paginate_users(page_size, offset)
        if not page:
            break
        for user in page:
            yield user
        offset += page_size


# test code
if __name__ == "__main__":
    for user in lazy_paginate(3):
        print(user)

