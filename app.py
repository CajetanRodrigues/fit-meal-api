from flask import Flask, request 
import json
import requests
import json
from flask_cors import CORS
from pymongo import MongoClient
import pymongo
import re

client = MongoClient('mongodb+srv://admin:admin@cluster0-qbkxj.mongodb.net/test?retryWrites=true&w=majority',27017)
# client=MongoClient('localhost',27017)
db=client.fitmeal
meals=db.meals
userMeals=db.userMeals
users=db.users
routines = db.routines
app = Flask(__name__)
CORS(app)

@app.route('/signup', methods = ["POST"]) 
def signup():
    data=request.json
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    name=str(data['name'])
    email=str(data['email'])
    password=str(data['password'])
    #Name Validation
    if(len(name)>25):
        return json.dumps(False)
    #Email Validation
    if(re.search(regex,email)==False):
        return json.dumps(False)
    #Password Validation
    flag = 0
    while True:   
        if (len(password)<8): 
            flag = -1
            break
        else: 
            flag = 0
            print("Valid Password") 
        break
  
    if flag ==-1: 
        return json.dumps(False)
    try:
        users.insert({ "name": name, "email":email, "password":password},check_keys=False)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return json.dumps(False)
    return json.dumps(True)

@app.route('/login', methods = ["POST"]) 
def login():
    data=request.json
    email=str(data['email'])
    password=str(data['password'])
    response = []
    documents=users.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    flag=0
    for i in range(0,len(response)):
        emailreg=response[i]["email"]
        passwordreg=response[i]["password"]
        if(password==passwordreg and email==emailreg):
            flag=1
            break
    if(flag==1):
        return json.dumps(True)
    else:
        return json.dumps(False)

@app.route('/read-profile', methods = ["GET"]) 
def readProfile():
    response = []
    user =users.find_one({"email": "cajetanrodrigues88@gmail.com"})
    user["_id"] = str(user["_id"])
    return json.dumps(user)

    
@app.route('/add-bmi', methods = ["POST"]) 
def addBMI():
    data=request.json
    email = "cajetanrodrigues88@gmail.com"
    print(data)
    gender=data['gender']
    age=data['age']
    height=data['height']
    weight=data['weight']
    try:
            myquery = { "email": "cajetanrodrigues88@gmail.com" }
            newvalues = { "$set": { "gender": gender} }
            users.update_one(myquery, newvalues)
            newvalues = { "$set": { "age": age} }
            users.update_one(myquery, newvalues)
            newvalues = { "$set": { "height": height} }
            users.update_one(myquery, newvalues)
            newvalues = { "$set": { "weight": weight} }
            users.update_one(myquery, newvalues)
    except pymongo.errors.DuplicateKeyError as e:
            print(e)
            return json.dumps(False)
    
    return json.dumps(True)

@app.route('/add-info', methods = ["POST"]) 
def addInfo():
    data=request.json
    email = "cajetanrodrigues88@gmail.com"
    print(data)
    goal=data['goal']
    activityLevel=data['activityLevel']
    bodyType=data['bodyType']
    mealsNumber=data['mealsNumber']
    try:
            myquery = { "email": "cajetanrodrigues88@gmail.com" }
            newvalues = { "$set": { "goal": goal} }
            users.update_one(myquery, newvalues)
            newvalues = { "$set": { "activityLevel": activityLevel} }
            users.update_one(myquery, newvalues)
            newvalues = { "$set": { "bodyType": bodyType} }
            users.update_one(myquery, newvalues)
            newvalues = { "$set": { "mealsNumber": mealsNumber} }
            users.update_one(myquery, newvalues)
    except pymongo.errors.DuplicateKeyError as e:
            print(e)
            return json.dumps(False)
    
    return json.dumps(True)

@app.route('/read-meals', methods = ["GET"]) 
def readMeals():
    response = []
    documents=meals.find()
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)

@app.route('/add-meals', methods = ["POST"]) 
def addMeals():
    dataArray=request.json
    for data in dataArray:
        print(data)
        item=data['Item']
        benefits=data['Benefits']
        protein=data['Protein']
        carbohydrates=data['Carbohydrates']
        calories=data['Calories']
        fats=data['Fats']
        image=data['Image']
        quantity=data['Quantity']
        try:
            meals.insert_one({ "item": item, "benefits":benefits, "protein":protein,"carbohydrates":carbohydrates,"calories": calories,"fats":fats, "image":image, "quantity":quantity})
        except pymongo.errors.DuplicateKeyError as e:
            print(e)
            return json.dumps(False)
    
    return json.dumps(True)

@app.route('/add-meal', methods = ["POST"]) 
def addMeal():
    data = request.json
    print(data)
    item=data['Item']
    benefits= 'NaN'
    protein=data['Protein']
    carbohydrates=data['Carbohydrates']
    calories=data['Calories']
    fats= 'NaN'
    image=data['Image']
    quantity=0
    try:
        userMeals.insert_one({ "item": item, "benefits":benefits, "protein":protein,"carbohydrates":carbohydrates,"calories": calories,"fats":fats, "image":image, "quantity":quantity})
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return json.dumps(False)
    return json.dumps(True)

@app.route('/read-routines', methods = ["POST"]) 
def readRoutines():
    response = []
    data = request.json
    userId = data['userId']
    print(userId)
    documents =routines.find_one({"userId": userId})
    response = []
    for document in documents:
        print(document)
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.dumps(response)


@app.route('/add-routine', methods = ["POST"]) 
def addRoutine():
    data = request.json
    print(data)
    routineName=data['routineName']
    routineFramed=data['routineFramed']
    try:
        routines.insert_one({"userId": "5ebe8f37357b2831267e60fc", "routineName": routineName, "routineFramed":routineFramed})
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        return json.dumps(False)
    return json.dumps(True)


@app.route('/frame-routine', methods = ["POST"]) 
def frameRoutine():
    data=request.json
    totalProtein = data["totalProtein"]
    totalCarbs = data["totalCarbs"]
    totalCalories = data["totalCalories"]
    
    basketArray = []
    for meal in data["basket"]:
        basketArray.append(meal)
        if meal["quantity"]>1 :
            mealObjCopy = meal.copy()
            mealObjCopy["quantity"] = 1
            for _ in range(meal["quantity"]):
                basketArray.append(mealObjCopy)
            basketArray.remove(meal)
        else:
            basketArray.append(meal)
    print(basketArray)
    # basketArray = sorted(basketArray, key=lambda k: k['calories'], reverse=True)
    oneCycle = {
        "time" : "8 AM"
    }
    oneCycleMeals = basketArray[0:int(len(basketArray)/4)]
    secondCycle = {
        "time" : "11 AM"
    }
    secondCycleMeals = basketArray[int(len(basketArray)/4): int(len(basketArray)/2)]
    routine = []
    routine.append(oneCycle)
    routine = routine + oneCycleMeals
    routine.append(secondCycle)
    routine = routine + secondCycleMeals
    
    return json.dumps(routine)

if __name__ == '__main__':  
    app.run(host='127.0.0.1',port=80,debug = True)
