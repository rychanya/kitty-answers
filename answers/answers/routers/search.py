from bson.objectid import ObjectId
from fastapi import APIRouter

from answers.db.qa import search
from answers.models.qa import SearchResult

router = APIRouter(prefix="/search", tags=["Search"])


@router.post("/", response_model=list[SearchResult])
def search_qa(q: str):
    user_id = ObjectId()
    res = search(q, user_id)
    return res
