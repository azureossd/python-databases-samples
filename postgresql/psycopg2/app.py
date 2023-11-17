import os

from psycopg2 import pool
from flask import Flask, jsonify

app = Flask(__name__)

messages = []
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')

conn_string=f"host='{HOST}' dbname='{DATABASE}' user='{USER}' password='{PASSWORD}'"
# Create a connection pool with a min of 1 connection and max of 128
conn_pool = pool.SimpleConnectionPool(1, 128, conn_string)


def createTable(conn, cursor):
    # Check if table exists
    deleteTable(conn, cursor)

    messages.append("Dropping existing table")
    print("Dropping existing table")

    cursor.execute("""
        CREATE TABLE Users 
        (id serial PRIMARY KEY, 
        name VARCHAR(50) NOT NULL, 
        lastname VARCHAR(50) NOT NULL);
    """)

    conn.commit()
    messages.append("Creating Table Users")


def queryRow(cursor):
    cursor.execute("SELECT * FROM Users where id=1")

    row = cursor.fetchone()
    messages.append("Querying from Table and selecting 1")
    print("Querying from Table and selecting 1")

    while row:
        print(row[0])
        row = cursor.fetchone()


def queryAllRows(cursor):
    cursor.execute("SELECT * FROM Users")

    rows = cursor.fetchall()
    messages.append("Querying all rows from Table")
    print("Querying all rows from Table")

    for row in rows:
        print(row, end='\n')


def insertRow(conn, cursor):
    cursor.execute("""
        INSERT INTO Users (name, lastname)
        VALUES (%s, %s)""",
                   ('Name', 'LastName'))
    
    messages.append("Inserting row")
    print("Inserting row")

    conn.commit()


def deleteRow(conn, cursor):
    cursor.execute("""
        DELETE FROM Users where id=1
    """)

    messages.append("Deleting row")
    print("Deleting row")

    conn.commit()


def deleteTable(conn, cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS Users 
    """)

    conn.commit()
    messages.append("Dropping Table Users")


@app.route('/')
def home():
    try:
        # Get a connection from the pool
        conn = conn_pool.getconn()
        cursor = conn.cursor()

        messages.clear()
        messages.append("Connecting to Database")
        # Pass in connection values to functions
        createTable(conn, cursor)
        insertRow(conn, cursor)
        queryRow(cursor)
        queryAllRows(cursor)
        deleteRow(conn, cursor)
        deleteTable(conn, cursor)
    except Exception as e:
        print(e)
    finally:
        messages.append("Closing connection to Database")
        # Clean up connections
        cursor.close()
        conn_pool.putconn(conn)
        print("PostgreSQL connection is closed")

    return jsonify(messages)


if __name__ == '__main__':
    app.run()
