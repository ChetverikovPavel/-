from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
mongo_base = client.Insta1609
collection = mongo_base['instagram']

for el in collection.find({'$and': [{'parse_username': 'shtanudachi'}, {'status': 'followers'}]}):
    pprint(el)
print()
for el in collection.find({'$and': [{'parse_username': 'avznamensky'}, {'status': 'following'}]}):
    pprint(el)