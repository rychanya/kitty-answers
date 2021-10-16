from answers.db import client
from bson import ObjectId

COL_NAME = "QA"

collection = client.get_database().get_collection(COL_NAME)

def search(s: str):
    pipeline = [
        {
            "$match": {
                # "correct": {"$exists": True},
                "question": {"$regex": f".*{s}.*", "$options": "i"},
            }
        },
        {
            "$group": {
                "_id": {"question": "$question", "type": "$type"},
                "data": {"$push": "$$ROOT"},
            }
        },
    ]
    return list(collection.aggregate(pipeline=pipeline))

def get(_id: ObjectId):
    return collection.find_one({"_id": _id})