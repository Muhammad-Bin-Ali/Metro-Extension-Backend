from datetime import datetime  # This will be needed later
import os
from dotenv import load_dotenv
from pymongo import MongoClient


def checkIfExist(id, link):
    try:
        load_dotenv()  # Load config from a .env file:
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections
        saved_links = (users.find_one({'id': id}))['saved-links']

        if saved_links:
            #if the url of the last link is not equal to the link that is currently being passed in
            for saved_link in saved_links:
                if saved_link[3] == link: #if the user has already saved that link
                    client.close()
                    return True

            return False #if no matching link is found, return false
        else:
            client.close() #close connection
            return False #user hasn't saved any links so return false
        #in case an error is thrown for whatever reason, the connection should be closed.
    except: 
        client.close()

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
            # if saved_links[-1][3] != link: 
            result = users.update_one({'id': id}, {'$push': {'saved-links': [title, datetime.now(), summary, link]}})
        else:
            result = users.update_one({'id': id}, {'$push': {'saved-links': [title, datetime.now(), summary, link]}})

        client.close() #close connection
        return True
    except:
        client.close()
        return False

#function to remove a saved link
def delLink(id, title, summary):
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
                if saved_links[i][0] == title:
                    date = saved_links[i][1]
                    link = saved_links[i][3]
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
            return 404

    except:
        client.close()

def getSaved(id, title):
    try:
        load_dotenv() # Load config from a .env file
        MONGODB_URI = os.environ['MONGODB_URI']

        # Connect to your MongoDB cluster:
        client = MongoClient(MONGODB_URI)
        db = client['main'] #retrieve main database
        users = db['Users'] #retrieve Users collections
      
        doc = users.find_one({'id': id})
        links = doc['saved-links']

        for link in links:
            if link[0] == title:
                body = link[2]
                client.close()
                return body
        
        client.close()
        return False

    except:
        client.close()


if __name__ == "__main__":
    addLink("104845424937636392509", "Test", "https://www.bbc.com/news/world-australia-59889522",
     "The U.S. attacked an Islamic State planner in Afghanistan in retaliation for a deadly bombing outside Kabul airport. There was a high risk of further blasts as it winds up its mission to evacuate civilians and withdraw troops. The attack killed scores of Afghans and 13 U.N. service members. Most of the more than 20 allied countries involved in airlifting their citizens and Afghans out of Kabul said they had completed evacuations by Friday. Britain was ending its operation on Saturday, its armed forces chief Nick Carter said, adding that the focus would then turn to withdrawing British troops. Britain said any recognition with the West should depend on how it acts with the Taliban and must be conditional on allowing safe passage for our site, you agree to our Terms of Service and Privacy Policy. We are happy to provide you with information about our products and services. We hope that you will use this information to help you in your daily life. Please share your photos and videos with us on our Facebook and Twitter accounts. We would like to hear from you about your experiences with our site. Please send them to: mail@dailymail.co.uk and we will feature them in a weekly Newsquiz. For more information, visit our News Quiz page or our Facebook page. For confidential support, call the Samaritans on 08457 90 90 90 or visit a local Samaritans branch, or see www.ge. For confidential support, call the Samaritans on 08457 90 90 90 or visit a local Samaritans ge. For confidential support, call the Samaritans on 08457 90 90 90 or visit a local Samaritans ge. For confidential support, call the Samaritans on 08457 90 90 90 or visit a local Samaritans ")
