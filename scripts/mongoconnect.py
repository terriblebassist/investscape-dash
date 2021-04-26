from pymongo import MongoClient
from decouple import config
import pandas as pd


class MongoDriver:
    def __init__(self):
        self.client = MongoClient(config('MONGO_URI'))

    def fetch_collection_in_dataframe(
            self, database=config('MONGO_DB'),
            collection=config('MONGO_COLLECTION')):
        db = self.client[database]
        return pd.DataFrame(list(db[collection].find()))

    def insert_document_in_collection(
            self, obj, database=config('MONGO_DB'),
            collection=config('MONGO_COLLECTION')):
        db = self.client[database]
        return db[collection].insert_one(obj).inserted_id


# z = MongoDriver()
# print(z.fetch_collection_in_dataframe())
# z.insert_document_in_collection(obj={
#     "date": "07/08/2020",
#     "scheme_code": 119598,
#     "scheme_name": "ABCD Fund",
#     "value": 2000,
#     "units": 5678
# })
# print(z.fetch_collection_in_dataframe())
