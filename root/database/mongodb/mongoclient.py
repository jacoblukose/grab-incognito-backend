
from pymongo import MongoClient

USERS_MONGO_COLLECTION = 'user_test'
REFFERAL_MONGO_COLLECTION = 'referral_test'
MONGO_CONNECTION_URL = 'localhost:27017'

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
        collection = self.db[collection_name]
        result=collection.find(query)
        return result


    def write(self, data, collection_name):
        collection = self.db[collection_name]
        result=collection.insert_one(data)
        return result.inserted_id, result.acknowledged
    
    def update():
        pass


m = MongoClientWrapper()

# write query sample...
# print(m.write({"name" : "Joe Drumgoole"}, 'user_test'))

# read query sample...
# query = {'name':"Joe Drumgoole"}
# data = m.read(query, 'user_test' )
# for r in data:
#     print(r)
