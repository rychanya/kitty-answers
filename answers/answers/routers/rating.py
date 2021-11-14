from bson import ObjectId
from fastapi import APIRouter, Depends

from answers.db.rating import dislike_qa, get, like_qa
from answers.dependencies import oid_from_path

router = APIRouter(prefix="/rating", tags=["Rating"])


@router.get("/{str_id}")
def get_rating(id: ObjectId = Depends(oid_from_path)):
    return get(id, ObjectId("61422e9a2f7a823e87957532"))


@router.post("/{str_id}/like")
def like(id: ObjectId = Depends(oid_from_path)):
    return like_qa(id, ObjectId("61422e9a2f7a823e87957532"))


@router.post("/{str_id}/dislike")
def dislike(id: ObjectId = Depends(oid_from_path)):
    return dislike_qa(id, ObjectId("61422e9a2f7a823e87957532"))
