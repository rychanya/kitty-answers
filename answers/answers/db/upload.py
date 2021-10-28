from answers.db import client
from bson import ObjectId
from answers.models.upload import Upload

COL_NAME = "Upload"

collection = client.get_database().get_collection(COL_NAME)

def create(by: ObjectId, file_id: ObjectId):
    _id = collection.insert_one({'by': by, 'file_id': file_id}).inserted_id
    return Upload(by=by, file_id=file_id, _id=_id)