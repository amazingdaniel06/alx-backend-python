import mysql.connector

def stream_user_ages():
    """
    Generator to yield user ages one by one
    """
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='aswiseBen10',  # change to your password
        database='ALX_prodev'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:   # loop 1
        yield row[0]

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculate the average age using the generator
    """
    total = 0
    count = 0
    for age in stream_user_ages():  # loop 2
        total += age
        count += 1
    if count == 0:
        print("No users found")
    else:
        average = total / count
        print(f"Average age of users: {average:.2f}")

# test
if __name__ == "__main__":
    calculate_average_age()

