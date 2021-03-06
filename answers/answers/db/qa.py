import re
from typing import Optional

from bson import ObjectId

from answers.db import client, get_client
from answers.db.upload import COL_EL_NAME
from answers.models.qa import QATypeEnum
from answers.models.upload import UploadQAinDB

COL_NAME = "QA"


def search(s: str, user_id: Optional[ObjectId]):
    pipeline = [
        {
            "$match": {
                # "correct": {"$exists": True},
                "question": {"$regex": f".*{re.escape(s)}.*", "$options": "i"},
            }
        },
        {
            "$lookup": {
                "from": "Rating",
                "localField": "_id",
                "foreignField": "_id",
                "as": "rating",
            }
        },
        {"$unwind": {"path": "$rating", "preserveNullAndEmptyArrays": True}},
        {
            "$addFields": {
                "rating": {
                    "$ifNull": ["$rating", {"_id": "$_id", "likes": [], "dislikes": []}]
                }
            }
        },
        {
            "$addFields": {
                "rating.likes_count": {"$size": "$rating.likes"},
                "rating.dislikes_count": {"$size": "$rating.dislikes"},
                "rating.is_liked": {"$in": [user_id, "$rating.likes"]},
                "rating.is_disliked": {"$in": [user_id, "$rating.dislikes"]},
            }
        },
        # {"$project": {"rating._id": 0}},
        {
            "$group": {
                "_id": {"question": "$question", "type": "$type"},
                "data": {"$push": "$$ROOT"},
            }
        },
    ]
    return list(
        client.get_database().get_collection(COL_NAME).aggregate(pipeline=pipeline)
    )


def get(_id: ObjectId, user_id: Optional[ObjectId]):
    return list(
        client.get_database()
        .get_collection(COL_NAME)
        .aggregate(
            [
                {"$match": {"_id": _id}},
                {
                    "$lookup": {
                        "from": "Rating",
                        "localField": "_id",
                        "foreignField": "_id",
                        "as": "rating",
                    }
                },
                {"$unwind": {"path": "$rating", "preserveNullAndEmptyArrays": True}},
                {
                    "$addFields": {
                        "rating": {
                            "$ifNull": [
                                "$rating",
                                {"_id": "$_id", "likes": [], "dislikes": []},
                            ]
                        }
                    }
                },
                {
                    "$addFields": {
                        "rating.likes_count": {"$size": "$rating.likes"},
                        "rating.dislikes_count": {"$size": "$rating.dislikes"},
                        "rating.is_liked": {"$in": [user_id, "$rating.likes"]},
                        "rating.is_disliked": {"$in": [user_id, "$rating.dislikes"]},
                    }
                },
            ]
        )
    )[0]


def get_or_create(qa: UploadQAinDB, by: ObjectId):
    def get_answer_match(qa: UploadQAinDB):
        if qa.is_corect:
            if qa.type in (
                QATypeEnum.MatchingChoice,
                QATypeEnum.RangingChoice,
                QATypeEnum.OnlyChoice,
            ):
                return {"$match": {"correct": qa.answer}}
            elif qa.type == QATypeEnum.MultipleChoice:
                return {"$match": {"$expr": {"$setEquals": ["$correct", qa.answer]}}}
            else:
                raise ValueError
        else:
            if qa.type in (
                QATypeEnum.MatchingChoice,
                QATypeEnum.RangingChoice,
                QATypeEnum.OnlyChoice,
            ):
                return {
                    "$match": {
                        "$expr": {
                            "$anyElementTrue": [
                                {
                                    "$map": {
                                        "input": "$incorrect",
                                        "as": "el",
                                        "in": {"$eq": ["$$el", qa.answer]},
                                    }
                                }
                            ]
                        }
                    }
                }
            elif qa.type == QATypeEnum.MultipleChoice:
                return {
                    "$match": {
                        "$expr": {
                            "$anyElementTrue": [
                                {
                                    "$map": {
                                        "input": "$incorrect",
                                        "as": "el",
                                        "in": {"$setEquals": ["$$el", qa.answer]},
                                    }
                                }
                            ]
                        }
                    }
                }
            else:
                raise ValueError

    client = get_client()
    pipeline = [
        {
            "$match": {
                "question": qa.question,
                "type": qa.type,
                "$expr": {"$setIsSubset": [qa.answers, "$answers"]},
            }
        },
        get_answer_match(qa),
        {"$project": {"_id": True}},
    ]
    with client.start_session() as session:
        with session.start_transaction():
            ids = [
                el["_id"]
                for el in session.client.get_database()
                .get_collection(COL_NAME)
                .aggregate(pipeline=pipeline, session=session)
            ]
            is_new = not bool(ids)
            if not ids:
                new_qa = qa.to_qa(by)
                id = (
                    client.get_database()
                    .get_collection(COL_NAME)
                    .insert_one(new_qa.dict(exclude={"id"}), session=session)
                    .inserted_id
                )
                ids = [id]
            client.get_database().get_collection(COL_EL_NAME).update_one(
                {"_id": qa.id}, {"$set": {"ids": ids, "isNew": is_new}}, session=session
            )
    client.close()
