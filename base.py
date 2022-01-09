import pymongo

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

mydb = client['Store']

information = mydb.beautiful_store_1 

rec = [{
    "Flowers": "Roses",
    "Price"  : 100,
    "Flowers": "Lily",
    "Price"  : 50,
    "Flowers": "Camomile",
    "Price"  : 30
      }]
information.insert_many(rec) 

import pymongo

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

mydb = client['Store']

information = mydb.beautiful_store_2

rec = [{
    "Books": "Adventude",
    "Price": 100,
    "Books": "Fantastic",
    "Price": 50
      }]
information.insert_many(rec) 

