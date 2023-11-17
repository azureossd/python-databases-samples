from pymongo import MongoClient
from bson import ObjectId
import os
from flask import Flask, jsonify

app = Flask(__name__)


HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')

messages = []


def createCollection(db):
    # Check if table exists
    collections = db.list_collection_names()

    if "users" in collections:
        print("The collection exists.")
        deleteCollection(db)

    db.createCollection("Users")
    messages.append("Creating User Collection")

def getUser(id, db):
    query = {'_id': ObjectId(id)}
    user_collection = db["users"]
    user = user_collection.find_one(query)
    messages.append(f"Querying from User Collection and selecting 1 user {user}")

def getUsers(db):
    user_collection = db["users"]
    user_collection.find()

    messages.append("Querying all users from collections")

    for user in user_collection.find():
      print(user)
    
def addUser(db):
    user = { "name": "Name", "last_name": "Last Name" }
    user_collection = db["users"]

    id = user_collection.insert_one(user)
    messages.append(f"Add user in collection. User Id: {id.inserted_id}")

    return id.inserted_id

def deleteUser(db):
    user = { "name": "Name", "last_name": "Last Name" }

    user_collection = db["users"]
    user_collection.delete_one(user)

    messages.append("Deleting user from collection")

def deleteCollection(db):
    user_collection = db["users"]
    user_collection.drop()

    messages.append("Dropping User Collection")

@app.route('/')
def home():
    try:
        messages.clear()
        messages.append("Connecting to Database")
        # If you are using Azure CosmosDb, default port is 10255 and add the following parameters ?ssl=true&retrywrites=false.
        # Example: conn_string = f"mongodb://{user}:{password}@{host}:10255/{database}?ssl=true&retrywrites=false"
        # Otherwise: conn_string = f"mongodb://{user}:{password}@{host}:27017/{database}"
        conn_string = f"mongodb://{USER}:{PASSWORD}@{HOST}:10255/{DATABASE}?ssl=true&retrywrites=false"
        client = MongoClient(conn_string, maxPoolSize=128)
        db = client[DATABASE]

        createCollection
        id = addUser(db)
        getUser(id, db)
        getUsers(db)
        deleteUser(db)
        deleteCollection(db)
    except Exception as e:
        print(e)
    finally:
        client.close()
        messages.append("Closing connection to Database")

    return jsonify(messages)

if __name__ == '__main__':
    app.run()



