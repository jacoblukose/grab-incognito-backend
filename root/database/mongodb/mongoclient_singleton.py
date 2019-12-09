import time
from pymongo import MongoClient

USERS_MONGO_COLLECTION = 'user_test'
REFFERAL_MONGO_COLLECTION = 'referral_test'
MONGO_CONNECTION_URL = 'localhost:27017'

# Singleton/SingletonDecorator.py
class SingletonDecorator:
    def __init__(self,klass):
        self.klass = klass
        self.instance = None
    def __call__(self,*args,**kwds):
        if self.instance == None:
            self.instance = self.klass(*args,**kwds)
        return self.instance

class MongoClientWrapper():
    def __init__(self,host='',port=''):

            #create mongoclient
            client = MongoClient(MONGO_CONNECTION_URL)
            # select default database
            self.db = client['my']

            if USERS_MONGO_COLLECTION not in self.db.list_collection_names():
                print("User collection not found. Creating...")
                self.users = self.db[USERS_MONGO_COLLECTION]

            if REFFERAL_MONGO_COLLECTION not in self.db.list_collection_names():
                print("Referral collection not found. Creating...")        
                self.users = self.db[REFFERAL_MONGO_COLLECTION]

    
    def read(self, query, collection_name):
        """
        Read documents from mongo
        """
        collection = self.db[collection_name]
        result = collection.find(query)
        return result


    def write(self, data, collection_name):
        """
        Insertion of new data
        """
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return result.inserted_id, result.acknowledged
    
    def update(self, query, data, collection_name ):
        """
        Updates existing records
        """
        collection = self.db[collection_name]
        result = collection.update_one(query, data)
        return result

m = SingletonDecorator(MongoClientWrapper)

# m = MongoClientWrapper()

# write query sample...
# print(m.write({"name" : "Joe Drumgoole"}, 'user_test'))

#update query sample...
#BY DEFAULT ONLY ONE RECORD OUT OF MANY WILL BE UPDATED. For multiple need to use update_many()
#https://www.w3schools.com/python/python_mongodb_update.asp
# query = {'name':"Joe Drumgoole"}
# newvalues = { "$set": { "address": "Canyon 123" } }
# data = m.update(query, newvalues, 'user_test' ) #result is not iterable.. use a read query to check..

# read query sample...
# query = {'name':"Joe Drumgoole"}
# data = m.read(query, 'user_test' )
# for r in data:
#     print(r)
