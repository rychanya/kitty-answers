from bson import ObjectId
from pydantic.tools import parse_obj_as

from answers.db import client
from answers.models import OIDStr
from answers.models.upload import Upload, UploadQA

COL_NAME = "Upload"
COL_EL_NAME = "Upload_el"

collection = client.get_database().get_collection(COL_NAME)


def create(by: ObjectId, row_data: list):
    data = [el.dict() for el in parse_obj_as(list[UploadQA], row_data)]
    with client.start_session() as session:
        with session.start_transaction():
            ids = (
                client.get_database()
                .get_collection(COL_EL_NAME)
                .insert_many(data)
                .inserted_ids
            )
            upload = Upload(by=by, row_data=ids)
            id = (
                client.get_database()
                .get_collection(COL_NAME)
                .insert_one(upload.dict(exclude_none=True))
                .inserted_id
            )
            if isinstance(id, ObjectId):
                upload.id = OIDStr(id)
                return upload
    # upload = Upload(by=by, row_data=row_data)
    # _id = collection.insert_one(upload.dict(exclude_none=True)).inserted_id
    # return _id


def get_el(id: ObjectId):
    return client.get_database().get_collection(COL_EL_NAME).find_one({"_id": id})
