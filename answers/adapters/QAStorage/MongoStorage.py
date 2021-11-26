import os

import certifi
from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from pydantic import BaseSettings
from pymongo import MongoClient, ReturnDocument
from pymongo.collection import Collection

from adapters.QAStorage.BaseQAStorage import (
    BaseQAStorage,
    InvalidQAIdException,
    QANotExistException,
)
from models.qa import QA, QACreateResult, QAInputDTO, QATypeEnum

load_dotenv()


class MongoSettings(BaseSettings):
    MONGO_DB_NAME: str
    MONGO_PASSWORD: str
    MONGO_USER: str


settings = MongoSettings()


class MongoStorage(BaseQAStorage):
    _client = None
    QA_NAME = "QA"
    QA_BASE_NAME = "QA_BASE"
    QA_GROUP_NAME = "QA_GROUP"

    @classmethod
    def _get_client(cls) -> MongoClient:
        mongo_url = f"mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@cluster0.ys89g.mongodb.net/{settings.MONGO_DB_NAME}?retryWrites=true&w=majority"
        if os.getpid() == 0:
            client = MongoClient(
                mongo_url,
                tlsCAFile=certifi.where(),
            )
        else:
            client = MongoClient(mongo_url, tlsCAFile=certifi.where(), connect=False)
        cls._client = client
        return client

    @property
    def client(self):
        if self._client:
            return self._client
        else:
            return self._get_client()

    @property
    def qa_collection(self) -> Collection:
        return self.client.get_database().get_collection(self.QA_NAME)

    @property
    def qa_base_collection(self) -> Collection:
        return self.client.get_database().get_collection(self.QA_BASE_NAME)

    @property
    def qa_group_collection(self) -> Collection:
        return self.client.get_database().get_collection(self.QA_GROUP_NAME)

    @staticmethod
    def str_to_oid(str_id) -> ObjectId:
        try:
            return ObjectId(str_id)
        except (InvalidId, TypeError):
            raise InvalidQAIdException(str_id=str_id)

    def get_qa_by_id(self, str_id: str) -> QA:
        id = self.str_to_oid(str_id)
        qa = (
            self.client.get_database()
            .get_collection(self.QA_NAME)
            .find_one({"_id": id})
        )
        if qa is None:
            raise QANotExistException(str_id)
        return QA.parse_obj(qa)

    def get_or_create(self, dto: QAInputDTO) -> QACreateResult:
        # pipeline = self.inputDTO_to_pipeline(dto)
        with self.client.start_session() as session:
            with session.start_transaction():
                base = self.qa_base_collection.find_one_and_update(
                    {"type": dto.type, "question": dto.question},
                    {"$setOnInsert": {"_id": ObjectId()}},
                    upsert=True,
                    return_document=ReturnDocument.AFTER,
                    session=session,
                    projection={"_id": 1},
                )
                ids = list(
                    self.qa_collection.aggregate(
                        [
                            {
                                "$match": {
                                    "is_correct": dto.is_correct,
                                    "base_id": base["_id"],
                                    "$expr": {
                                        "$setIsSubset": [dto.answers, "$answers"]
                                    },
                                }
                            },
                            {
                                "$match": {
                                    "$expr": {"$setEquals": ["$answer", dto.answer]}
                                }
                            }
                            if dto.type == QATypeEnum.MultipleChoice
                            else {"$match": {"answer": dto.answer}},
                        ],
                        session=session,
                    )
                )
                # ids = list(
                #     self.client.get_database()
                #     .get_collection(self.QA_NAME)
                #     .aggregate(pipeline=pipeline, session=session)
                # )
                if ids:
                    return QACreateResult(
                        ids=[str(el["_id"] for el in ids)], is_new=False
                    )
                id = (
                    self.client.get_database()
                    .get_collection(self.QA_NAME)
                    .insert_one(dto.dict(), session=session)
                    .inserted_id
                )
                return QACreateResult(ids=[str(id)], is_new=True)

    # @staticmethod
    # def inputDTO_to_pipeline(dto: QAInputDTO):
    #     pipeline = [
    #         {
    #             "$match": {
    #                 "question": dto.question,
    #                 "type": dto.type,
    #                 "$expr": {"$setIsSubset": [dto.answers, "$answers"]}
    #                 if dto.is_incomplete
    #                 else {"$setEquals": [dto.answers, "$answers"]},
    #             }
    #         }
    #     ]
    #     if not dto.is_incomplete:
    #         pipeline.append(
    #             {
    #                 "$match": {
    #                     "is_incomplete": dto.is_incomplete,
    #                     "$expr": {"$setEquals": ["$extra_answers", dto.extra_answers]},
    #                 }
    #             }
    #         )
    #     if dto.is_correct:
    #         pipeline.append(
    #             {"$match": {"$expr": {"$setEquals": ["$correct", dto.answer]}}}
    #             if dto.type == QATypeEnum.MultipleChoice
    #             else {"$match": {"correct": dto.answer}}
    #         )
    #     else:
    #         pipeline.append(
    #             {
    #                 "$match": {
    #                     "$expr": {
    #                         "$anyElementTrue": [
    #                             {
    #                                 "$map": {
    #                                     "input": "$incorrect",
    #                                     "as": "el",
    #                                     "in": {"$setEquals": ["$$el", dto.answer]}
    #                                     if dto.type == QATypeEnum.MultipleChoice
    #                                     else {"$eq": ["$$el", dto.answer]},
    #                                 }
    #                             }
    #                         ]
    #                     }
    #                 }
    #             }
    #         )
    #     return pipeline
