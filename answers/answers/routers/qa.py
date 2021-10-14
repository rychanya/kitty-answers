from fastapi import APIRouter
from answers.tasks import add
from answers.models.qa import SearchResult
from answers.db.qa import search

router = APIRouter()

@router.get("/search/{q}", response_model=list[SearchResult])
def search_qa(q: str):
    return search(q)
