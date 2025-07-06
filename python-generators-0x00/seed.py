import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',      # Your MySQL server is usually on localhost
            user='root',           # Change this if your MySQL username is different
            password='aswise?Ben10'  # Replace with your actual MySQL password
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None
import mysql.connector
from mysql.connector import Error

def connect_db():
    # your connection code here
    ...

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    print("Database ALX_prodev checked/created")
    cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='aswise?Ben10',  # replace with your actual password
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    )
    """
    cursor.execute(create_table_query)
    print("Table user_data created successfully")
    cursor.close()

import csv

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if the user_id already exists
            cursor.execute(
                "SELECT user_id FROM user_data WHERE user_id = %s",
                (row['user_id'],)
            )
            result = cursor.fetchone()
            if not result:
                insert_query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    row['user_id'],
                    row['name'],
                    row['email'],
                    row['age']
                ))
        connection.commit()
    print("Data inserted successfully")
    cursor.close()


def stream_rows(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    row = cursor.fetchone()
    while row:
        yield row
        row = cursor.fetchone()
    cursor.close()

