import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator to yield batches of rows from the user_data table
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='aswise?Ben10',  # change your password
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:   # loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes batches to yield users over age 25
    """
    for batch in stream_users_in_batches(batch_size):   # loop 2
        for user in batch:  # loop 3
            if user[3] > 25:
                yield user


# test
if __name__ == "__main__":
    for user in batch_processing(5):
        print(user)




def get_all_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='your_password',
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


