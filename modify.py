from pymongo import MongoClient
import pymongo
import requests 
import json

client = MongoClient('mongodb+srv://admin:admin@cluster0-qbkxj.mongodb.net/test?retryWrites=true&w=majority',27017)
# client=MongoClient('localhost',27017)
db=client.fitmeal
meals=db.meals

pageSize = 200
pageNumber = 1

data = {
  "dataType": [
    "Foundation",
    "SR Legacy"
  ],
  "pageSize": 100,
  "pageNumber": 1,
  "sortBy": "dataType.keyword",
  "sortOrder": "asc",
}
headers = {
    'Content-Type' : 'application/json'
}
count = 0
# print(meals.count())

for i in meals.find().limit(1):
    print(i["description"])
    break
print('numbers of pages with size 100 are : ' + str(count))
