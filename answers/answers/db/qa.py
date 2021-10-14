from answers.db import client

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