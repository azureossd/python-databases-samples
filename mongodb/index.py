from pymongo import MongoClient
from bson import ObjectId
import sys, os
from flask import Flask, jsonify

app = Flask(__name__)

client = None
db = None
messages = []

host = os.environ.get('HOST')
database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')

def Connect():
    messages.clear()
    global client 
    #If you are using Azure CosmosDb, default port is 10255 and add the following parameters ?ssl=true&retrywrites=false.
    #Example: conn_string="mongodb://{}:{}@{}:10255/{}?ssl=true&retrywrites=false".format(user,password,host,database)
    conn_string="mongodb://{}:{}@{}:27017/{}".format(user,password,host,database)
    client = MongoClient(conn_string)
    global db
    db = client[database]
    messages.append("Connecting to Database")

def CreateCollection():
    #Check if table exists
    collections = db.list_collection_names()
    if "users" in collections:
        print("The collection exists.")
        DeleteCollection()

    db.createCollection("Users")
    messages.append("Creating User Collection")

def GetUser(id):
    query = {'_id': ObjectId(id)}
    user_collection = db["users"]
    user = user_collection.find_one(query)
    messages.append("Querying from User Collection and selecting 1 user {}".format(user))

def GetUsers():
    user_collection = db["users"]
    records = user_collection.find()
    messages.append("Querying all users from collections")
    for user in user_collection.find():
      print(user)
    
def AddUser():
    user = { "name": "Name", "last_name": "Last Name" }
    user_collection = db["users"]
    id = user_collection.insert_one(user)
    messages.append("Add user in collection. User Id: {}".format(id.inserted_id))
    return id.inserted_id

def DeleteUser():
    user = { "name": "Name", "last_name": "Last Name" }
    user_collection = db["users"]
    user_collection.delete_one(user)
    messages.append("Deleting user from collection")

def DeleteCollection():
    user_collection = db["users"]
    user_collection.drop()
    messages.append("Dropping User Collection")

@app.route('/')
def home():
    try:
        Connect()
        CreateCollection
        id = AddUser()
        GetUser(id)
        GetUsers()
        DeleteUser()
        DeleteCollection()
    except Exception as ex:
        print("Raised exception caught: ", ex.args)
    finally:
        client.close()
        messages.append("Closing connection to Database")

    return jsonify(messages)

if __name__ == '__main__':
    app.run()



