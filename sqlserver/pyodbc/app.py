from flask import Flask, jsonify
import pyodbc
import os

app = Flask(__name__)

# Global variables
global conn
global cursor
conn = None
cursor = None
# Environment variables
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')

connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={HOST};DATABASE={DATABASE};UID={USER};PWD={PASSWORD}'
messages = []


def createTable(conn, cursor):
    # Check if table exists
    if cursor.tables(table='Users', tableType='TABLE').fetchone():
        deleteTable()

    cursor.execute("""
        CREATE TABLE Users
        (id int IDENTITY(1,1) PRIMARY KEY,
        name varchar(50) NOT NULL,
        lastname varchar(50) NULL)
    """)

    conn.commit()
    messages.append("Creating Table Users")


def queryRow(cursor):
    cursor.execute("SELECT * FROM Users where id=1")

    row = cursor.fetchone()
    messages.append("Querying from Table and selecting 1")

    while row:
        print(row[0])
        row = cursor.fetchone()


def queryAllRows(cursor):
    cursor.execute("SELECT * FROM Users")

    rows = cursor.fetchall()
    messages.append("Querying all rows from Table")

    for row in rows:
        print(row, end='\n')


def insertRow(conn, cursor):
    cursor.execute("""
        INSERT INTO Users (name, lastname)
        VALUES (?, ?)""",
                   ('Name', 'LastName')
                   )

    conn.commit()
    messages.append("Inserting row")


def deleteRow(conn, cursor):
    cursor.execute("""
        DELETE FROM Users where id=1
    """)

    conn.commit()
    messages.append("Deleting row")


def deleteTable(conn, cursor):
    cursor.execute("""
        DROP TABLE Users
    """)

    conn.commit()
    messages.append("Dropping Table Users")


@app.route('/')
def home():
    try:
        messages.clear()
        messages.append("Connecting to Database")
        # pyodbc automatically handles connection pooling
        conn = pyodbc.connect(connectionString)
        cursor = conn.cursor()
        # Pass in connection values to functions
        createTable(conn, cursor)
        insertRow(conn, cursor)
        queryRow(conn, cursor)
        queryAllRows(conn, cursor)
        deleteRow(conn, cursor)
        deleteTable(conn, cursor)
    except Exception as e:
        print(e)
    finally:
        messages.append("Closing connection to Database")
        # Clean up connections
        cursor.close()
        conn.close()

    return jsonify(messages)


if __name__ == '__main__':
    app.run()
