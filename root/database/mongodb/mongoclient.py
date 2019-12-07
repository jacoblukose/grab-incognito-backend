
from pymongo import MongoClient

USERS_MONGO_COLLECTION = 'user_test'
REFFERAL_MONGO_COLLECTION = 'referral_test'

class MongoClientWrapper():
    def __init__(self,host='',port=''):
            # mongo_configs = parse_yaml('root/configs/database-configs.yaml')
            #create mongoclient
            client = MongoClient('localhost:27017')
            # select default database
            self.db = client['my']
            if USERS_MONGO_COLLECTION not in self.db.list_collection_names():
                print("User collection not found. Creating...")
                self.users = self.db[USERS_MONGO_COLLECTION]

            if REFFERAL_MONGO_COLLECTION not in self.db.list_collection_names():
                print("Referral collection not found. Creating...")        
                self.users = self.db[REFFERAL_MONGO_COLLECTION]

    
    def read():
        pass

    def write(self, data, collection_name):
        collection = self.db[collection_name]
        result=collection.insert_one(data)
        return result.inserted_id, result.acknowledged
    
    def update():
        pass


m = MongoClientWrapper()
print(m.write({"name" : "Joe Drumgoole"}, 'user_test'))