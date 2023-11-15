import os

from flask import Flask, jsonify
from mysql.connector import pooling

app = Flask(__name__)

messages = []
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')

pooling.CNX_POOL_MAXSIZE = 128
# Create connection pool and set the max pool size to 128
# https://dev.mysql.com/doc/connector-python/en/connector-python-connection-pooling.html
connection_pool = pooling.MySQLConnectionPool(
    user=USER,
    host=HOST,
    database=DATABASE,
    password=PASSWORD,
    pool_name="mysql-connector-python-pool",
    pool_size=128)

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
    print("Connection Pool Name - ", connection_pool.pool_name)
    print("Connection Pool Size - ", connection_pool.pool_size)

    try:
        # Get connection object from a pool
        conn = connection_pool.get_connection()
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
        conn.close()
        print("MySQL connection is closed")

    return jsonify(messages)


if __name__ == '__main__':
    app.run()
