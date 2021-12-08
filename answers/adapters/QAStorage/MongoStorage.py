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

    # @staticmethod
    # def str_to_id(str_id: str) -> ObjectId:
    #     try:
    #         return ObjectId(str_id)
    #     except (InvalidId, TypeError):
    #         raise InvalidQAIdException(str_id=str_id)


#     def _get_by_id(self, str_id: Optional[str], collection: Collection):
#         _id = None if str_id is None else self.str_to_id(str_id)
#         data = collection.find_one({"_id": _id})
#         if data is None:
#             raise NotExistExeption(str_id)
#         return data

#     def get_qa_by_id(self, str_id: str) -> QA:
#         data = self._get_by_id(str_id, self.qa_collection)
#         return QA.parse_obj(data)

#     def get_qa_base_by_id(self, str_id: str) -> QABase:
#         data = self._get_by_id(str_id, self.qa_base_collection)
#         return QABase.parse_obj(data)

#     def get_qa_group_by_id(self, str_id: str) -> QAGroup:
#         data = self._get_by_id(str_id, self.qa_group_collection)
#         return QAGroup.parse_obj(data)

#     def get_or_create_qa_base(
#         self, dto: QABase, session: ClientSession = None
#     ) -> QABase:
#         if dto.id is not None:
#             base = self.get_qa_base_by_id(dto.id)
#             if base == dto:
#                 return base
#             else:
#                 raise AlredyExistExeption(
#                     f"qa base with {dto.id} alredy exist with diferent data"
#                 )
#         filter = {"question": dto.question, "type": dto.type}
#         update = {"$setOnInsert": {"_id": ObjectId()}}
#         doc = self.qa_base_collection.find_one_and_update(
#             filter=filter,
#             update=update,
#             upsert=True,
#             session=session,
#             return_document=ReturnDocument.AFTER,
#         )
#         doc["id"] = str(doc["_id"])
#         return QABase.parse_obj(doc)

#     def get_or_create_qa_group(
#         self, base_id: ObjectId, dto: QAInputDTO, session: ClientSession
#     ):
#         group_id = None if dto.group_id is None else self.str_to_id(dto.group_id)
#         if group_id is None:
#             return None
#         doc = self.qa_group_collection.find_one_and_update(
#             {"base_id": base_id, "_id": group_id},
#             {
#                 "$setOnInsert": {
#                     "answers": dto.answers,
#                     "extra_answers": dto.extra_answers,
#                 }
#             },
#             session=session,
#             upsert=True,
#             return_document=ReturnDocument.AFTER,
#         )
#         return doc

#     def get_or_create_qa(self, dto: QAInputDTO) -> QACreateResult:
#         with self.client.start_session() as session:
#             with session.start_transaction():
#                 base = self.get_or_create_qa_base(dto.base, session=session)
#                 group = self.get_or_create_qa_group(base.id, dto, session)
#                 group_id = None if group is None else group["_id"]
#                 ids = list(
#                     self.qa_collection.aggregate(
#                         [
#                             {
#                                 "$match": {
#                                     "is_correct": dto.is_correct,
#                                     "base_id": base.id,
#                                     "group_id": group_id,
#                                     "$expr": {
#                                         "$setIsSubset": [dto.answers, "$answers"]
#                                     },
#                                 }
#                             },
#                             {
#                                 "$match": {
#                                     "$expr": {"$setEquals": ["$answer", dto.answer]}
#                                 }
#                             }
#                             if dto.type == QATypeEnum.MultipleChoice
#                             else {"$match": {"answer": dto.answer}},
#                         ],
#                         session=session,
#                     )
#                 )
#                 if ids:
#                     return QACreateResult(
#                         ids=[str(el["_id"] for el in ids)], is_new=False
#                     )
#                 doc = dto.dict(exclude={"type", "question"})
#                 doc["base_id"] = base.id
#                 id = self.qa_collection.insert_one(doc, session=session).inserted_id
#                 return QACreateResult(ids=[str(id)], is_new=True)

#     # @staticmethod
#     # def inputDTO_to_pipeline(dto: QAInputDTO):
#     #     pipeline = [
#     #         {
#     #             "$match": {
#     #                 "question": dto.question,
#     #                 "type": dto.type,
#     #                 "$expr": {"$setIsSubset": [dto.answers, "$answers"]}
#     #                 if dto.is_incomplete
#     #                 else {"$setEquals": [dto.answers, "$answers"]},
#     #             }
#     #         }
#     #     ]
#     #     if not dto.is_incomplete:
#     #         pipeline.append(
#     #             {
#     #                 "$match": {
#     #                     "is_incomplete": dto.is_incomplete,
#     #                     "$expr": {"$setEquals": ["$extra_answers", dto.extra_answers]},
#     #                 }
#     #             }
#     #         )
#     #     if dto.is_correct:
#     #         pipeline.append(
#     #             {"$match": {"$expr": {"$setEquals": ["$correct", dto.answer]}}}
#     #             if dto.type == QATypeEnum.MultipleChoice
#     #             else {"$match": {"correct": dto.answer}}
#     #         )
#     #     else:
#     #         pipeline.append(
#     #             {
#     #                 "$match": {
#     #                     "$expr": {
#     #                         "$anyElementTrue": [
#     #                             {
#     #                                 "$map": {
#     #                                     "input": "$incorrect",
#     #                                     "as": "el",
#     #                                     "in": {"$setEquals": ["$$el", dto.answer]}
#     #                                     if dto.type == QATypeEnum.MultipleChoice
#     #                                     else {"$eq": ["$$el", dto.answer]},
#     #                                 }
#     #                             }
#     #                         ]
#     #                     }
#     #                 }
#     #             }
#     #         )
#     #     return pipeline
