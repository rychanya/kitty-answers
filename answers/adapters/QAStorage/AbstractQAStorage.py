import abc
from typing import Optional, Tuple
from uuid import UUID

from pydantic import BaseModel, validator
from pydantic.types import ConstrainedStr as ConstrainedStrBase

from answers.models.qa import QATypeEnum


class StorageException(Exception):
    ...


class GroupException(StorageException):
    ...


class ConstrainedStr(ConstrainedStrBase):
    strip_whitespace = True
    min_length = 1
    max_length = 200


class QuestionDTO(BaseModel):
    class Config:
        use_enum_values = True

    question: ConstrainedStr
    type: QATypeEnum


class QuestionDB(QuestionDTO):
    id: UUID


class GroupDTO(BaseModel):
    all_answers: list[ConstrainedStr]
    all_extra_answers: list[ConstrainedStr]

    def check(self, type: QATypeEnum) -> None:
        if self.all_extra_answers:
            if type != QATypeEnum.MatchingChoice:
                raise GroupException(
                    "extra answers can be only in matching answer type"
                )
            if len(self.all_answers) != len(self.all_extra_answers):
                raise GroupException("answers and extra answers must be same lenth")


class GroupDB(GroupDTO):
    id: UUID
    question_id: UUID


class QADTO(BaseModel):
    question: QuestionDTO
    group: Optional[GroupDTO]
    answer: list[ConstrainedStr]
    is_correct: bool

    @validator("answer")
    def validate_answer(cls, v, values: dict):
        if not v:
            raise ValueError("answer must contain data")
        group: Optional[GroupDTO] = values.get("group")
        if group is None:
            return v
        question: Optional[QuestionDTO] = values.get("question")

        if question and hasattr(question, "type"):

            if question.type == QATypeEnum.OnlyChoice:
                if len(v) != 1:
                    raise ValueError(
                        "answer with type OnlyChoiche must contain only one el"
                    )
                if v[0] not in group.all_answers:
                    raise ValueError("answer must be in all_answers")

            if question.type == QATypeEnum.MultipleChoice:
                if not set(v).issubset(group.all_answers):
                    raise ValueError("all answer el must be in all_answers")

            if question.type in (QATypeEnum.MatchingChoice, QATypeEnum.RangingChoice):
                if set(v) != set(group.all_answers):
                    raise ValueError("all el from all_answers must be in answer")

        return v


class QADB(BaseModel):
    id: UUID
    question_id: UUID
    group_id: Optional[UUID]
    answer: list[ConstrainedStr]
    is_correct: bool


class AbstractQAStorage(abc.ABC):
    @abc.abstractmethod
    def get_or_create(self, in_dto: QADTO) -> Tuple[QADB, bool]:
        ...
