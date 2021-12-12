import os
from typing import Optional, Tuple
from uuid import uuid4

import certifi
from dotenv import load_dotenv
from pydantic import BaseSettings
from pymongo import MongoClient, ReturnDocument
from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from adapters.QAStorage.AbstractQAStorage import (
    QADB,
    QADTO,
    AbstractQAStorage,
    GroupDB,
    GroupDTO,
    QuestionDB,
    QuestionDTO,
)
from answers.models.qa import QATypeEnum

load_dotenv()


class MongoSettings(BaseSettings):
    MONGO_DB_NAME: str
    MONGO_PASSWORD: str
    MONGO_USER: str


settings = MongoSettings()


class MongoStorage(AbstractQAStorage):
    _client = None
    _ANSWERS = "Answers"
    _QUESTIONS = "Questions"
    _GROUPS = "Groups"

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
    def answers_collection(self) -> Collection:
        return self.client.get_database().get_collection(self._ANSWERS)

    @property
    def questions_collection(self) -> Collection:
        return self.client.get_database().get_collection(self._QUESTIONS)

    @property
    def groups_collection(self) -> Collection:
        return self.client.get_database().get_collection(self._GROUPS)

    def get_or_create(self, in_dto: QADTO) -> Tuple[QADB, bool]:
        with self.client.start_session() as session:
            with session.start_transaction():
                question = self._get_or_create_question(
                    in_dto.question, session=session
                )
                group = self._get_or_create_group(
                    in_dto.group, question, session=session
                )
                filter = {
                    "question_id": question.id,
                    "group_id": group.id if group else None,
                    "is_correct": in_dto.is_correct,
                }
                if question.type in (
                    QATypeEnum.OnlyChoice,
                    QATypeEnum.RangingChoice,
                    QATypeEnum.MatchingChoice,
                ):
                    filter.update({"answer": in_dto.answer})
                else:
                    filter.update({"$expr": {"$setEquals": [in_dto.answer, "$answer"]}})
                doc = self.answers_collection.find_one(filter=filter, session=session)
                if doc is not None:
                    return (QADB.parse_obj(doc), False)
                else:
                    answer_dict = {
                        "answer": in_dto.answer,
                        "is_correct": in_dto.is_correct,
                        "question_id": question.id,
                        "group_id": group.id if group else None,
                        "id": uuid4(),
                    }
                    self.answers_collection.insert_one(answer_dict, session=session)
                    return (QADB.parse_obj(answer_dict), True)

    def _get_or_create_question(
        self, question: QuestionDTO, session: ClientSession = None
    ) -> QuestionDB:
        return QuestionDB.parse_obj(
            self.questions_collection.find_one_and_update(
                filter=question.dict(),
                update={"$setOnInsert": {"id": uuid4()}},
                upsert=True,
                return_document=ReturnDocument.AFTER,
                session=session,
            )
        )

    def _get_or_create_group(
        self,
        group_dto: Optional[GroupDTO],
        question: QuestionDB,
        session: ClientSession = None,
    ) -> Optional[GroupDB]:
        if group_dto is None:
            return None

        group_dto.check(question.type)

        doc = self.groups_collection.find_one(
            filter={
                "question_id": question.id,
                "$expr": {
                    "$and": [
                        {"$setEquals": [group_dto.all_answers, "$all_answers"]},
                        {
                            "$setEquals": [
                                group_dto.all_extra_answers,
                                "$all_extra_answers",
                            ]
                        },
                    ]
                },
            },
            session=session,
        )
        if doc is not None:
            return GroupDB.parse_obj(doc)
        else:
            group_dict = group_dto.dict()
            group_dict["question_id"] = question.id
            group_dict["id"] = uuid4()
            self.groups_collection.insert_one(group_dict, session=session)
            return GroupDB.parse_obj(group_dict)
