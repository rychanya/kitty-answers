from bson.objectid import ObjectId
from fastapi import APIRouter

from answers.db.qa import get
from answers.models.qa import SearchResultEl

router = APIRouter(prefix="/qa", tags=["QA"])


@router.get("/{id}", response_model=SearchResultEl)
def get_qa(id: str):
    _id = ObjectId(id)
    return get(_id, ObjectId())
