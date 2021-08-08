from datetime import datetime  # This will be needed later
import os

from pprint import pprint
from dotenv import load_dotenv
from pymongo import MongoClient


def createUser(email):
    try:
        load_dotenv()  # Load config from a .env file:
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections

        document = {
            "email": email,
            "date-joined": datetime.now(),
            "saved-links": []
            }

        result = users.insert_one(document)

        client.close() #close connection
    #in case an error is thrown for whatever reason, the connection should be closed.
    except: 
        client.close()

def addLink(email, link):
    try:
        load_dotenv() # Load config from a .env file
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections
        result = users.update_one({'email': email}, {'$push': {'saved-links': link}})

        client.close() #close connection
    except:
        client.close()

def getAll(email):
    try:
        load_dotenv() # Load config from a .env file
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections
        # doc = users.find_one({'email': email})
        # links = doc['saved-links']
        if users.count_documents({'email': email}, limit = 1) > 0:
            doc = users.find_one({'email': email})
            links = doc['saved-links']
            client.close()
            return links

        else:
            client.close() #close connection
            return False

        return links
    except:
        client.close()


if __name__ == "__main__":
    getAll('new_uer@gmail.com')
##
