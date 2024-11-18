# Use this script to load data from Duckdb to Mongodb.abs
# The script connects to Duckdb and Mongodb, loads data from Duckdb, and inserts it into Mongodb.

import json
import duckdb
from pymongo import MongoClient
import pandas as pd

# Load constants from json
with open("data/json/mongo.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
    MONGO_URI = data["mongo_uri"]
    DATABASE_NAME = data["database_name"]
    COLLECTION_NAME = data["collection_name"]
    tables = data["tables"]

# Moar constants
DB_PATH = "data/warehouse/warehouse.duckdb"

# duckdb connect
duckdb_conn = duckdb.connect(DB_PATH)

# mongoconnect
mongo_client = MongoClient(MONGO_URI)
# new db + new collection
mongo_db = mongo_client[DATABASE_NAME]
mongo_collection = mongo_db[COLLECTION_NAME]

# data to mongo
for t in tables:
    df = duckdb_conn.execute(f"SELECT * FROM {t}").fetchdf()
    data = df.to_dict(orient="records")
    mongo_collection = mongo_db[t]
    try:
        mongo_collection.insert_many(data)
        print(f"Great success! Inserted table with {len(data)} records.")
    except Exception as e:
        print(f"Oops: {e}")

# verify
#sample_data = mongo_collection.find().limit(1)
#for doc in sample_data:
#    print(doc)

duckdb_conn.close()
mongo_client.close()
