import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='aswise?Ben10',  # change this to your actual password
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()

if __name__ == "__main__":
    for user in stream_users():
        print(user)

