# import pytest

# from adapters.QAStorage.MongoStorage import MongoStorage
# from models.qa import QAInputDTO, QATypeEnum


# def generate_qa_dto(
#     type: str = QATypeEnum.OnlyChoice,
#     question: str = "qa_question",
#     answer_template: str = "qa_answer",
#     answer: list[int] = [1],
#     is_correct: bool = True,
#     is_incomplete: bool = True,
# ) -> QAInputDTO:
#     answers = [f"{answer_template}_{index}" for index in range(1, 5)]
#     _answer = [el for index, el in enumerate(answers, 1) if index in answer]
#     if type == QATypeEnum.OnlyChoice:
#         _answer = _answer[0]
#     return QAInputDTO(
#         by=None,
#         type=type,
#         question=question,
#         answers=answers,
#         answer=_answer,
#         is_correct=is_correct,
#         is_incomplete=is_incomplete,
#     )


# @pytest.mark.parametrize(
#     "qa, qa_in_db, is_new, count",
#     [
#         (generate_qa_dto(type=QATypeEnum.OnlyChoice, answer=[2]), [], True, 1),
#         (
#             generate_qa_dto(type=QATypeEnum.OnlyChoice, answer=[2]),
#             [generate_qa_dto(type=QATypeEnum.OnlyChoice, answer=[2])],
#             False,
#             0,
#         ),
#         (
#             generate_qa_dto(type=QATypeEnum.OnlyChoice, answer=[2]),
#             [generate_qa_dto(type=QATypeEnum.OnlyChoice, answer=[3])],
#             True,
#             1,
#         ),
#     ],
# )
# def test_create(
#     MongoStorageMock: MongoStorage,
#     qa: QAInputDTO,
#     qa_in_db: list[QAInputDTO],
#     is_new: bool,
#     count: int,
# ):
#     assert MongoStorageMock.qa_collection.count_documents({}) == 0
#     for el in qa_in_db:
#         base_id = MongoStorageMock.qa_base_collection.insert_one(
#             el.dict(include={"question", "type"})
#         ).inserted_id
#         data = el.dict(exclude={"question", "type"})
#         data["base_id"] = base_id
#         MongoStorageMock.qa_collection.insert_one(data)
#     qa_in_db_count = MongoStorageMock.qa_collection.count_documents({})
#     assert qa_in_db_count == len(qa_in_db)
#     res = MongoStorageMock.get_or_create_qa(qa)
#     assert MongoStorageMock.qa_collection.count_documents({}) - qa_in_db_count == count
#     assert res.is_new == is_new

from adapters.QAStorage.AbstractQAStorage import QuestionDTO
from adapters.QAStorage.MongoStorage import MongoStorage
from answers.models.qa import QATypeEnum


def test___g():
    s = MongoStorage()
    print(s.client.get_database().name)
    assert False
