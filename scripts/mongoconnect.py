from pymongo import MongoClient
from decouple import config
import pandas as pd


class MongoDriver:
    def __init__(self):
        self.client = MongoClient(config('MONGODB_URI'))

    def get_data(self, database='mf', collection='transactions'):
        db = self.client[database]
        collection = db[collection]
        df = pd.DataFrame(list(collection.find()))
        return df
