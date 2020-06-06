from pymongo import MongoClient
import pymongo
import requests 
import json

client = MongoClient('mongodb+srv://admin:admin@cluster0-nwyig.mongodb.net/fitmeal?retryWrites=true&w=majority',27017)
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
while True:
    try:
        r = requests.post(url = 'https://api.nal.usda.gov/fdc/v1/foods/list?api_key=U7LnkKAa6qPCPRxI47P1lPA0tI7tBUEEiFH1Hc5q',data = json.dumps(data),
                        headers=headers)
        meals.insert_many(r.json())
        data["pageNumber"] = data["pageNumber"] + 1
        count+=1
        print('100 pages on page number = ' + str(count) + ' inserted successfully in mongodb')
        print('numbers of pages with size 100 are : ' + str(count))        

    except:
        print('100 pages on page number = ' + str(count) + ' inserted successfully in mongodb')
        print('numbers of pages with size 100 are : ' + str(count))
print('numbers of pages with size 100 are : ' + str(count))
