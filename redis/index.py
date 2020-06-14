from flask import Flask, jsonify
import sys, os, random, string
import redis

app = Flask(__name__)

con = None
messages = []
host = os.environ.get('HOST')
password = os.environ.get('PASSWORD')


def Connect():
    messages.clear()
    global con
    con = redis.StrictRedis(host=host,port=6379, password=password, charset='utf-8', decode_responses=True)    
    messages.append("Connecting to Redis")

def Ping():
    result = con.ping()
    messages.append("Ping to Redis " + str(result))

def AddKey(key, value):
    con.set(key, value)
    messages.append("Adding random value '{}' to key '{}'".format(value, key))

def GetKey(key):
    value = con.get(key)
    messages.append("Getting Key '{}' with value '{}'".format(key, value))

def GetKeys():
    messages.append("Printing Keys")
    for key in con.keys('*'):
        messages.append("---> Printing key '{}' ".format(key))
    
def DeleteKeys():
    cursor = '0'
    while cursor != 0:
        cursor, keys = con.scan(cursor=cursor, match='*',)
        if keys:
            con.delete(*keys)
    messages.append("Deleting all keys")

def randomString(stringLength=4):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@app.route('/')
def home():
    try:
        Connect()
        Ping()
        name = "Name-"+ randomString()
        value = randomString()
        AddKey(name,value)
        GetKey(name)
        name = "Name-"+ randomString()
        value = randomString()
        AddKey(name,value)
        GetKeys()
        DeleteKeys()
    except Exception as ex:
        print("Raised exception caught: ", ex.args)

    return jsonify(messages)

if __name__ == '__main__':
    app.run()



