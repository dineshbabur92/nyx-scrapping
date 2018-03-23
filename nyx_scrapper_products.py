
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

db.nyx_products.delete_many({})
categories = list(db.nyx_categories.find({}))
print("fetching for " + str(len(categories)))

for category in categories:
    products = []
    driver.get(category["category_page"] + "?srule=best-sellers&viewall=1")
    product_elements = driver.find_elements_by_css_selector(".b-product_tile")
    for product_element in product_elements:
        href_element = product_element.find_element_by_css_selector(".b-product_img-link")
        products.append({
            "category_name": category["parent_category"] + "_" + category["category_name"],
            "listing_page": category["category_page"] + "?srule=best-sellers&viewall=1",
            "product_page": href_element.get_attribute("href"),
            "product_id_from_site": product_element.get_attribute("data-itemid"),
            "fetch_status": 0
        })
    products_inserts_result = db.nyx_products.insert_many(products)
    if(len(products_inserts_result.inserted_ids) == len(products)):
        print("inserted successfully!, " + str(len(products)) + ", for: " + category["parent_category"] + "_" + category["category_name"])
    else:
        print("some problem with insertion")
print("done!!!")

