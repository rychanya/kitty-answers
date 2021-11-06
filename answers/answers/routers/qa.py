from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, File

from answers.db.qa import get, search
from answers.db.upload import create
from answers.dependencies import get_user, max_content_length
from answers.models.qa import SearchResult, SearchResultEl
from answers.models.upload import Upload
from answers.models.user import User
from answers.tasks import parse_upload, test_task
from answers.xl import file_iter

router = APIRouter()


@router.post("/search", response_model=list[SearchResult])
def search_qa(q: str):
    return search(q)


@router.get("/{id}", response_model=SearchResultEl)
def get_qa(id: str):
    _id = ObjectId(id)
    return get(_id)


@router.post(
    "/upload", dependencies=[Depends(max_content_length)], response_model=Upload
)
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

@router.post("/test")
def test():
    test_task.delay()