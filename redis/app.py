from flask import Flask, jsonify
import os, uuid
import redis

app = Flask(__name__)

messages = []
HOST = os.environ.get('HOST')
PASSWORD = os.environ.get('PASSWORD')


def ping(conn):
    result = conn.ping()
    messages.append(f"Ping to Redis - {str(result)}")

def addKey(conn, key, value):
    conn.set(key, value)
    messages.append(f"Adding random value '{value}' to key '{key}'")

def getKey(conn, key):
    value = conn.get(key)
    messages.append(f"Getting Key '{key}' with value '{value}'")

def getKeys(conn):
    messages.append("Printing Keys")

    for key in conn.keys('*'):
        messages.append(f"---> Printing key '{key}'")
    
def deleteKeys(conn):
    cursor = '0'

    while cursor != 0:
        cursor, keys = conn.scan(cursor=cursor, match='*',)
        if keys:
            conn.delete(*keys)

    messages.append("Deleting all keys")


@app.route('/')
def home():
    id = uuid.uuid4()
    key = f"key-{id}"
    value = f"value-{id}"

    try:
        messages.clear()
        conn = redis.StrictRedis(host=HOST, port=6379, password=PASSWORD, charset='utf-8', decode_responses=True)    
        messages.append("Connecting to Redis")

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



