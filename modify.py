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
# print(meals.count())

for i in meals.find().limit(10):
    print(i["description"].split(",")[0])
    imageName = i["description"].split(",")[0]
    r = requests.get(url = 'http://127.0.0.1:8083/image/'+imageName,
                        headers=headers)
    data = r.json()
    image = data["results"][0]["urls"]
    obj = {
      "name": data["results"][0]["user"]["name"],
      "profile": data["results"][0]["user"]["links"]["html"]
    }

    query = { "description": i["description"] }

    imageQuery = { "$set": { "image": image } }
    unsplashPhotographerQuery = { "$set": { "unsplash": obj } }

    meals.update_one(query, imageQuery)
    meals.update_one(query, unsplashPhotographerQuery)

    print(obj)
    print(data["results"][0]["urls"])