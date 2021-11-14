from typing import Optional

from bson import ObjectId
from pymongo.client_session import ClientSession

from answers.db import client
from answers.models.rating import Rating

COL_NAME = "Rating"


def _get_or_create(id: ObjectId, session: ClientSession):
    client.get_database().get_collection(COL_NAME).find_one_and_update(
        filter={"_id": id},
        update={"$setOnInsert": {"likes": [], "dislikes": []}},
        upsert=True,
        session=session,
    )


def _get_formated_rating(
    id: ObjectId, user_id: Optional[ObjectId], session: ClientSession
) -> Rating:
    doc = list(
        client.get_database()
        .get_collection(COL_NAME)
        .aggregate(
            [
                {"$match": {"_id": id}},
                {
                    "$project": {
                        "likes_count": {"$size": "$likes"},
                        "dislikes_count": {"$size": "$dislikes"},
                        "is_liked": {"$in": [user_id, "$likes"]},
                        "is_disliked": {"$in": [user_id, "$dislikes"]},
                    }
                },
            ],
            session=session,
        )
    )
    if doc:
        return Rating.parse_obj(doc[0])
    else:
        return Rating.parse_obj(
            {
                "_id": id,
                "likes_count": 0,
                "dislikes_count": 0,
                "is_liked": False,
                "is_disliked": False,
            }
        )


def get(id: ObjectId, user_id: Optional[ObjectId]) -> Rating:
    with client.start_session() as session:
        with session.start_transaction():
            _get_or_create(id, session)
            return _get_formated_rating(id, user_id, session)


def like_qa(id: ObjectId, user_id: ObjectId) -> Rating:
    with client.start_session() as session:
        with session.start_transaction():
            _get_or_create(id, session)
            client.get_database().get_collection(COL_NAME).find_one_and_update(
                filter={"_id": id},
                update={
                    "$pull": {"dislikes": user_id},
                    "$addToSet": {"likes": user_id},
                },
                session=session,
            )
            return _get_formated_rating(id, user_id, session)


def dislike_qa(id: ObjectId, user_id: ObjectId) -> Rating:
    with client.start_session() as session:
        with session.start_transaction():
            _get_or_create(id, session)
            client.get_database().get_collection(COL_NAME).find_one_and_update(
                filter={"_id": id},
                update={
                    "$pull": {"likes": user_id},
                    "$addToSet": {"dislikes": user_id},
                },
                session=session,
            )
            return _get_formated_rating(id, user_id, session)
