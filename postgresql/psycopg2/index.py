import psycopg2
import sys, os
from flask import Flask, jsonify

app = Flask(__name__)

cnx  = None
cursor = None

messages = []
host = os.environ.get('HOST')
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')

def Connect():
    messages.clear()
    global cnx 
    conn_string="host='{}' dbname='{}' user='{}' password='{}'".format(host,database,user,password)
    cnx  = psycopg2.connect(conn_string)
    global cursor
    cursor = cnx.cursor()
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

    cnx.commit()
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
    cnx.commit()
    messages.append("Inserting row")

def DeleteRow():
    cursor.execute("""
    DELETE FROM Users where id=1""")  
    cnx.commit()
    messages.append("Deleting row")

def DeleteTable():
    cursor.execute("""
    DROP TABLE IF EXISTS Users 
    """)
    cnx.commit()
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
        cnx.close()
        messages.append("Closing connection to Database")

    return jsonify(messages)

if __name__ == '__main__':
    app.run()



