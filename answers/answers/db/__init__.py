import os

import certifi
from pymongo import MongoClient

from answers.models.settings import MongoSettings

settings = MongoSettings()


def get_client():
    mongo_url = f"mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@cluster0.ys89g.mongodb.net/{settings.MONGO_DB_NAME}?retryWrites=true&w=majority"
    if os.getpid() == 0:
        return MongoClient(
            mongo_url,
            tlsCAFile=certifi.where(),
        )
    else:
        return MongoClient(mongo_url, tlsCAFile=certifi.where(), connect=False)


client = get_client()
