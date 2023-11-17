from flask import Flask, jsonify
import os, uuid
import redis

app = Flask(__name__)

messages = []
HOST = os.environ.get('HOST')
PASSWORD = os.environ.get('PASSWORD')

conn_pool = redis.ConnectionPool(host=HOST, port=6379, password=PASSWORD, decode_responses=True)

def ping(conn):
    result = conn.ping()
    print(f"Ping to Redis - {str(result)}")
    messages.append(f"Ping to Redis - {str(result)}")

def addKey(conn, key, value):
    conn.set(key, value)
    print(f"Adding random value '{value}' to key '{key}'")
    messages.append(f"Adding random value '{value}' to key '{key}'")

def getKey(conn, key):
    value = conn.get(key)
    print(f"Getting Key '{key}' with value '{value}'")
    messages.append(f"Getting Key '{key}' with value '{value}'")

def getKeys(conn):
    messages.append("Printing Keys")
    print("Printing Keys")
    for key in conn.keys('*'):
        print(f"---> Printing key '{key}'")
        messages.append(f"---> Printing key '{key}'")
    
def deleteKeys(conn):
    cursor = '0'

    while cursor != 0:
        cursor, keys = conn.scan(cursor=cursor, match='*',)
        if keys:
            conn.delete(*keys)

    print("Deleting all keys")
    messages.append("Deleting all keys")


@app.route('/')
def home():
    id = uuid.uuid4()
    key = f"key-{id}"
    value = f"value-{id}"

    try:
        messages.clear()
        conn = redis.StrictRedis(connection_pool=conn_pool, max_connections=128)    
        messages.append("Connecting to Redis")
        print("Connecting to Redis")
        
        ping(conn)
        addKey(conn, key, value)
        getKey(conn, key)
        addKey(conn, key, value)
        getKeys(conn)
        deleteKeys(conn)
    except Exception as ex:
        print("Raised exception caught: ", ex.args)        

    return jsonify(messages)

if __name__ == '__main__':
    app.run()



