from flask import Flask, jsonify
import mariadb
import sys
import os

app = Flask(__name__)

mariadb_connection  = None
cursor = None

messages = []
host = os.environ.get('HOST')
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')

def Connect():
    messages.clear()
    global mariadb_connection 
    mariadb_connection  = mariadb.connect(user=user, password=password, database=database, host=host)
    global cursor
    cursor = mariadb_connection.cursor()
    messages.append("Connecting to Database")

def CreateTable():
    #Check if table exists
    DeleteTable()
    messages.append("Dropping existing table")

    cursor.execute("""
        CREATE TABLE Users 
        (id serial PRIMARY KEY, 
        name VARCHAR(50) NOT NULL, 
        lastname VARCHAR(50) NOT NULL);
        """)

    mariadb_connection.commit()
    messages.append("Creating Table Users")

def QueryRow():
    cursor.execute("SELECT * FROM Users where id=1") 
    row = cursor.fetchone() 
    messages.append("Querying from Table and selecting 1")
    while row: 
        print(row[0])
        row = cursor.fetchone()

def QueryAllRows():
    cursor.execute("SELECT * FROM Users") 
    rows = cursor.fetchall()
    messages.append("Querying all rows from Table")
    for row in rows:
        print(row, end='\n')
    
def InsertRow():
    cursor.execute("""
    INSERT INTO Users (name, lastname)
    VALUES (%s, %s)""", ('Name','LastName')) 
    mariadb_connection.commit()
    messages.append("Inserting row")

def DeleteRow():
    cursor.execute("""
    DELETE FROM Users where id=1""")  
    mariadb_connection.commit()
    messages.append("Deleting row")

def DeleteTable():
    cursor.execute("""
    DROP TABLE IF EXISTS Users 
    """)
    mariadb_connection.commit()
    messages.append("Dropping Table Users")

@app.route('/')
def home():
    try:
        Connect()
        CreateTable()
        InsertRow()
        QueryRow()
        QueryAllRows()
        DeleteRow()
        DeleteTable()
    except Exception as ex:
        print("Raised exception caught: ", ex.args)
    finally:
        cursor.close()
        mariadb_connection.close()
        messages.append("Closing connection to Database")

    return jsonify(messages)

if __name__ == '__main__':
    app.run()



