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
headers = {
    'Content-Type' : 'application/json'
}



from selenium import webdriver
import os 
import time
import requests
import io
from PIL import Image
import hashlib
# This is the path I use
# DRIVER_PATH = '.../Desktop/Scraping/chromedriver 2'
# Put the path for your ChromeDriver here
DRIVER_PATH = 'C:/chromedriver'
wd = webdriver.Chrome(executable_path=DRIVER_PATH)
def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls

arr = meals.find().sort("_id", pymongo.ASCENDING)
arrMaxLength = meals.count()
print(arrMaxLength)
pageSize = 100
pageNumber = 0
countValue = 0
temp = 0
while True:
        arr1 = arr.skip(505).limit(1000)
        for i in arr1:
            try:
                # if i["img"]!=None:
                #     temp+=1
                #     print(temp)
                #     print("Already present, so skipping!!")
                #     continue
                print(i["description"].split(",")[0])
                fdcId =  i["fdcId"]
                imageName = i["description"].split(",")[0]
                res= []
                with webdriver.Chrome(executable_path=DRIVER_PATH) as wd:
                        res = fetch_image_urls(i["description"].split(",")[0], 1, wd=wd, sleep_between_interactions=0.5)
                image = ''
                for item in res:
                    image = item

                print('-------------------------')
                print(fdcId)
                print(image)
                query = { "fdcId": fdcId }
                imageQuery = { "$set": { "img": image } }
                # unsplashPhotographerQuery = { "$set": { "unsplash": obj } }

                meals.update_one(query, imageQuery)
                print('Inserted in database successfully')
                
                x = count.find_one()
                cquery = { "key": "abc" }
                countQuery = { "$set": { "count": x["count"]+1 } }
                count.update_one(cquery, countQuery)
                # meals.update_one(query, unsplashPhotographerQuery)

                # print(obj)
                # print(data["results"][0]["urls"])
                countValue+=1
                print(str(countValue) + ' documents updated')
                print('-------------------------------')
            except ValueError:
                print('Json decoding failed hence countinuing to next item')
                continue
        if(countValue>arrMaxLength):
            print("Completed Task Successfully, Yipee")
            
        pageNumber+=1
    