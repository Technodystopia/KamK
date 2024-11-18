import json
import duckdb
import os
from pymongo import MongoClient
import pandas as pd

with open("data/json/mongo.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    MONGO_URI = data["mongo_uri"]
    DB_NAME = data["database_name"]
    COLLECTION = data["collection_name"]
    tables = data["tables"]

client = MongoClient(MONGO_URI)
mongo_db = client[DB_NAME]
mongo_collection = mongo_db[COLLECTION]

path = "src/bi/workspace/sources/warehouse/warehouse.duckdb"
try: 
    if not os.path.exists(path):
        print(f"Creating new DuckDB-file in {path}")
        conn = duckdb.connect(path)
        conn.close()
    
    conn = duckdb.connect(path)
    for t in tables:
        mongo_collection = mongo_db[t]
        data = list(mongo_collection.find())
        df = pd.DataFrame(data)
        df = df.drop("_id", axis=1)
        conn.execute(f"CREATE TABLE IF NOT EXISTS {t} AS SELECT * FROM df")
except Exception as e:
    print(f"Oh no: {e}")

#result = conn.execute("SELECT * FROM hopp_kooste_gold").df()
#print(result)

conn.close()
client.close()
