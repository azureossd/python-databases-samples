from flask import Flask, jsonify
import pymssql
import os

app = Flask(__name__)

# Environment variables
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')

messages = []


def createTable(conn, cursor):
    # Check if table exists
    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = 'Users'
    """)

    if cursor.fetchone()[0] == 1:
        deleteTable(conn, cursor)

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
        VALUES (%s, %s)""",
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
    # pymssql does not handle connection pooling on its own
    # Other APIs or ORMs can be used to do this - like sqlachlemy
    conn = pymssql.connect(HOST, USER, PASSWORD, DATABASE)
    cursor = conn.cursor()

    try:
        messages.clear()
        messages.append("Connecting to Database")

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

    return jsonify(messages)


if __name__ == '__main__':
    app.run()
