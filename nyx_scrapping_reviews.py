
# coding: utf-8

# In[37]:

import urllib, json, pandas
from bson import ObjectId
import datetime
from IPython.display import clear_output
import traceback

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# In[38]:

import pymongo
client = pymongo.MongoClient("localhost", 27017)
db = client.revlon
print("inserting into db, " + db.name)

products = list(db.nyx_products.find({}))
# products = products[0:2]
print("fetching " + str(len(products)) + " products")

DATA_PATH = "D:\\Data\\Dinesh\\Work\\revlon\\nyx_data_final"

MASTER_URL = '''
https://api.bazaarvoice.com/data/batch.json?
passkey=e7e8c07apoamt76yz4sc85yjz
&apiversion=5.5
&displaycode=17556-en_us
&resource.q0=reviews
&filter.q0=isratingsonly%3Aeq%3Afalse
&filter.q0=productid%3Aeq%3A{0}
&filter.q0=contentlocale%3Aeq%3Aen_US
&sort.q0=submissiontime%3Adesc
&stats.q0=reviews
&filteredstats.q0=reviews
&include.q0=authors%2Cproducts%2Ccomments
&filter_reviews.q0=contentlocale%3Aeq%3Aen_US
&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_US
&filter_comments.q0=contentlocale%3Aeq%3Aen_US
&limit.q0=100
&offset.q0=0
&limit_comments.q0=3
&callback=bv_1111_20310
'''
MASTER_URL = MASTER_URL.replace("\n", "")


fetched_products = 0
for product in products:
    try:
        print("fetching product id: " + str(product["product_id_from_site"]))
        response = urllib.request.urlopen(MASTER_URL.format(product["product_id_from_site"])).read()
        reviews = json.loads(response.decode("utf-8")[14:-1])["BatchedResults"]["q0"]["Results"]
        try: 
            reviews_insert = db.nyx_reviews.insert_many(reviews)
            if(len(reviews_insert.inserted_ids) == len(reviews)):
                print("reviews inserted successfully")
                product_update_result = db.nyx_products.update_one(
                    { "_id": product["_id"] }, 
                    { 
                        "$set": { "fetch_status": 1 }, 
                        "$currentDate": {"lastModified": True } 
                    }
                )
                if(product_update_result.modified_count == 1):
                    print("product status updated successfully")
                else:
                    print("cannot update product status")
            else:
                print("reviews could not be inserted into db")
        except:
            print("database insert exception")
            pass
#         print(DATA_PATH
#             + "\\"
#             + product["product_id_from_site"] + "___" + datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
#             + ".json")
        with open(
            DATA_PATH
            + "\\"
            + product["product_id_from_site"] + "___" + datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S') 
            + ".json", "w", encoding="utf-8"
        ) as output_file: 
            json.dump(json.loads(JSONEncoder().encode(reviews)), output_file)
        fetched_products += 1
        print("fetched " + str(len(reviews)) 
              + " reviews for product id, " + str(product["product_id_from_site"]) 
              + ". Total products fetched = " + str(fetched_products))
        clear_output()
    except:
        traceback.print_exc()
        pass
        


# In[18]:



