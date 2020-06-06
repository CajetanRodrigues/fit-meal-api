import schedule
import time
from pymongo import MongoClient
import pymongo
import requests 
import json

client = MongoClient('mongodb+srv://admin:admin@cluster0-nwyig.mongodb.net/fitmeal?retryWrites=true&w=majority',27017)
# client=MongoClient('localhost',27017)
db=client.fitmeal
meals=db.meals
count=db.count

# meals.update({ "_id": 1 },{ "$unset": {"image": ""}});
# meals.update({}, {"$unset": {"image": 1}}, multi=True)
res = meals.find().sort("_id",1).skip(1500).limit(1)
for i in res:
    print(i)
