from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, File

from answers.db.upload import create, get_upload_report
from answers.dependencies import get_user, max_content_length
from answers.models.upload import Upload
from answers.models.user import User
from answers.tasks import parse_upload
from answers.xl import file_iter

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/", dependencies=[Depends(max_content_length)], response_model=Upload)
def upload(
    user: User = Depends(get_user),
    file: bytes = File(...),
):
    row_data = file_iter(file)
    upload = create(
        by=user.id,
        row_data=row_data,
    )
    if upload is None:
        return
    for qa_id in upload.row_data:
        parse_upload.delay(str(qa_id), str(user.id))
    return upload


@router.get("/{str_id}", name="Get upload by id")
def get_upload(str_id: str, user: User = Depends(get_user)):
    oid = ObjectId(str_id)
    print(get_upload_report(oid, user.id))
