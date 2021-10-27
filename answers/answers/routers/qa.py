from bson.objectid import ObjectId
from fastapi import APIRouter, Depends, Header
from answers.tasks import add
from answers.models.qa import SearchResult, SearchResultEl
from answers.db.qa import search, get
from answers.dependencies import get_payload

router = APIRouter()

@router.get("/search/{q}", response_model=list[SearchResult])
def search_qa(q: str):
    return search(q)

@router.get("/{id}", response_model=SearchResultEl)
def get_qa(id: str):
    _id = ObjectId(id)
    return get(_id)

@router.put("/upload")
def upload(payload=Depends(get_payload)):
    return payload