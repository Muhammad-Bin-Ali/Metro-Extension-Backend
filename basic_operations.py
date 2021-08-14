from datetime import datetime  # This will be needed later
import os

from pprint import pprint
from dotenv import load_dotenv
from pymongo import MongoClient


def createUser(id, email):
    try:
        load_dotenv()  # Load config from a .env file:
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections

        #if the user doesn't already exist in database. If a document with their ID cannot be found, then create new document
        if not users.count_documents({"id": id}, limit = 1) > 0:
            document = {
                "id": id,
                "email": email,
                "date-joined": datetime.now(),
                "saved-links": []
                }

            result = users.insert_one(document)

        client.close() #close connection
    #in case an error is thrown for whatever reason, the connection should be closed.
    except: 
        client.close()

def addLink(id, link, title, summary):
    try:
        load_dotenv() # Load config from a .env file
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections
        saved_links = (users.find_one({'id': id}))['saved-links']
        
        if saved_links:
            #if the url of the last link is not equal to the link that is currently being passed in
            if saved_links[-1][3] != link: 
                result = users.update_one({'id': id}, {'$push': {'saved-links': [title, datetime.now(), summary, link]}})
        else:
            result = users.update_one({'id': id}, {'$push': {'saved-links': [title, datetime.now(), summary, link]}})

        client.close() #close connection
        return True
    except:
        client.close()
        return False

#function to remove a saved link
def delLink(id, link, title, summary):
    try:
        load_dotenv() # Load config from a .env file
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections
        saved_links = (users.find_one({'id': id}))['saved-links']
        
        if saved_links:
            #finding index of saved link
            for i in range(len(saved_links)):
                if saved_links[i][3] == link:
                    date = saved_links[i][1]
                    break
            else:
                client.close();
                return True
        
            result = users.update_one({'id': id}, {'$pull': {'saved-links': [title, date, summary, link]}})

        client.close() #close connection
        return True
    except:
        client.close()
        return False

def getAll(id):
    try:
        load_dotenv() # Load config from a .env file
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections
      
        if users.count_documents({'id': id}, limit = 1) > 0:
            doc = users.find_one({'id': id})
            links = doc['saved-links']
            #cleaning the query so it only returns the title and date to front end
            cleaned_links = []
            for link in links:
                date = link[1].strftime("%d.%m.%Y")
                title = link[0]
                cleaned_links.append([title, date])

            client.close()
            return cleaned_links

        else:
            client.close() #close connection
            return False

        return links
    except:
        client.close()


if __name__ == "__main__":
    # addLink("104845424937636392509", "https://www.instagram.com/direct/t/340282366841710300949128190617270476779?hl=en",
    #  "Random title", "Test Summmary 1q2341241")
    getAll("104845424937636392509")
