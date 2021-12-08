import os
from typing import Optional, Tuple
from uuid import uuid4

import certifi
from bson import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
from pydantic import BaseSettings
from pymongo import MongoClient, ReturnDocument
from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from adapters.QAStorage.AbstractQAStorage import (
    QAINDTO,
    AbstractQAStorage,
    GroupDTO,
    QuestionDTO,
    QuestionException,
)

load_dotenv()


class MongoSettings(BaseSettings):
    MONGO_DB_NAME: str
    MONGO_PASSWORD: str
    MONGO_USER: str


settings = MongoSettings()
settings.MONGO_DB_NAME = "TEST_A"


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

    def get_or_create(self, in_dto: QAINDTO) -> Tuple[str, bool]:
        return ("1", True)

    def _get_or_create_question(
        self, question: QuestionDTO, session: ClientSession = None
    ) -> QuestionDTO:
        return QuestionDTO.parse_obj(
            self.questions_collection.find_one_and_update(
                filter=question.dict(exclude={"id"}),
                update={"$setOnInsert": {"id": uuid4()}},
                upsert=True,
                return_document=ReturnDocument.AFTER,
                session=session,
            )
        )

    def _get_or_create_group(self, group: Optional[GroupDTO]) -> Optional[GroupDTO]:
        if group is None:
            return None

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
