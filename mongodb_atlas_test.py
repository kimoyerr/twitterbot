import pymongo
from os import environ

my_client = pymongo.MongoClient(environ['MONGODB_ATLAS_CONNECTION'])

# Test
my_db = my_client.tweets
print(my_db)
