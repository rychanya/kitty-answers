from answers.db import client
from bson import ObjectId
from pymongo import ReturnDocument
from answers.models.user import User

COL_NAME = "Users"

collection = client.get_database().get_collection(COL_NAME)


def get_or_create(sub):
    doc = collection.find_one_and_update(
        filter={"sub": sub},
        update={"$setOnInsert": {"_id": ObjectId()}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return User.parse_obj(doc)
