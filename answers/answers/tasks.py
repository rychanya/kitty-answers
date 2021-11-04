import os

import celery
from bson.objectid import ObjectId

from answers.db.qa import get_or_create
from answers.db.upload import get_el
from answers.models.upload import UploadQAinDB

app = celery.Celery("tasker")
app.conf.broker_url = os.environ["REDIS_URL"]  # type: ignore


@app.task
def parse_upload(oid_str: str, by_str: str):
    oid = ObjectId(oid_str)
    by = ObjectId(by_str)
    qa = UploadQAinDB.parse_obj(get_el(oid))
    get_or_create(qa, by)
