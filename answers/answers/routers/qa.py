from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, File, Header
from answers.tasks import add
from answers.models.qa import SearchResult, SearchResultEl
from answers.db.qa import search, get
from answers.dependencies import get_payload, max_content_length, get_user
from answers.db import fs
from answers.models.user import User
from answers.models.upload import Upload
from answers.db.upload import create

router = APIRouter()

@router.get("/search/{q}", response_model=list[SearchResult])
def search_qa(q: str):
    return search(q)

@router.get("/{id}", response_model=SearchResultEl)
def get_qa(id: str):
    _id = ObjectId(id)
    return get(_id)

@router.post("/upload", dependencies=[Depends(max_content_length)], response_model=Upload)
def upload(user: User=Depends(get_user), file: bytes = File(...)):
    file_id = fs.put(file)
    return create(by=user.id, file_id=file_id)