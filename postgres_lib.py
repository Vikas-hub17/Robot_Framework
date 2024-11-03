import psycopg2
import json

def insert_data_to_db(data):
    connection = psycopg2.connect(
        dbname='Actuals',
        user='vikas',
        password='admin',
        host='localhost',
        port='5432'
    )
    cursor = connection.cursor()

    # Assume data contains rows in format [["Name", "Age", "City"], [...]]
    for row in data:
        cursor.execute(
            "INSERT INTO sample (Name, Salesman, Item, Units) VALUES (%s, %s, %s)",
            (row[0], row[1], row[2])
        )
    connection.commit()
    cursor.close()
    connection.close()
