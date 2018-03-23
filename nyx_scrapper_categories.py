
# coding: utf-8

# In[7]:

import time
import pymongo

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from pathlib import Path
import os
import datetime
import traceback

client = pymongo.MongoClient("localhost", 27017)
db = client.revlon
print("inserting into db, " + db.name)

driver = webdriver.Firefox("D:\\Data\\Dinesh\\Work\\revlon\\geckodriver-v0.19.1-win64");
driver.get("https://www.nyxcosmetics.com")
driver.implicitly_wait(10)

db.nyx_categories.delete_many({})
links = []
# links = {}
# links["face"] = []
# links["eyes"] = []
# links["lips"] = []
list_elements = driver.find_elements_by_css_selector(".cat_lips li a")
for e in list_elements:
    links.append({
        "parent_category": "lips",
        "category_name": e.get_attribute("innerText").strip(), 
        "category_page": e.get_attribute("href"),
        "fetch_status": 0
    })
list_elements = driver.find_elements_by_css_selector(".cat_face li a")
for e in list_elements:
    links.append({
        "parent_category": "face",
        "category_name": e.get_attribute("innerText").strip(), 
        "category_page": e.get_attribute("href"),
        "fetch_status": 0
    })
list_elements = driver.find_elements_by_css_selector(".cat_eyes li a")
for e in list_elements:
    links.append({
        "parent_category": "eyes",
        "category_name": e.get_attribute("innerText").strip(), 
        "category_page": e.get_attribute("href"),
        "fetch_status": 0
    })
category_inserts_result = db.nyx_categories.insert_many(links)
if(len(category_inserts_result.inserted_ids) == len(links)):
    print("inserted successfully!, " + str(len(links)))
else:
    print("some problem with insertion")
# links = {"face": [links["face"][0]]}

