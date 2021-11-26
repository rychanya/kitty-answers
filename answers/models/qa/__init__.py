from enum import Enum
from typing import Generic, Optional, TypeVar

from bson import ObjectId
from pydantic import Field, validator
from pydantic.generics import GenericModel
from pydantic.main import BaseModel


class QATypeEnum(str, Enum):
    OnlyChoice = "Выберите один правильный вариант"
    MultipleChoice = "Выберите все правильные варианты"
    RangingChoice = "Перетащите варианты так, чтобы они оказались в правильном порядке"
    MatchingChoice = "Соедините соответствия справа с правильными вариантами"


AnswerType = TypeVar("AnswerType", str, list[str])


class QA(GenericModel, Generic[AnswerType]):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True

    id: str = Field(..., alias="_id")
    by: Optional[str]
    type: QATypeEnum
    question: str
    answers: list[str]
    extra_answers: list[str] = []
    correct: Optional[AnswerType]
    incorrect: list[AnswerType] = []
    is_incomplete: bool

    @validator("id", pre=True)
    def validate_by(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("by", pre=True)
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class QAInputDTO(GenericModel, Generic[AnswerType]):
    class Config:
        use_enum_values = True

    by: Optional[str]
    type: QATypeEnum
    question: str
    answers: list[str]
    extra_answers: list[str] = []
    answer: AnswerType
    is_correct: bool

    @validator("answer")
    def validate_answer(cls, v, values):
        _type = values.get("type")
        _answers = values.get("answers", [])
        if _type == QATypeEnum.OnlyChoice and v not in _answers:
            raise ValueError("answer must be in answers")
        if _type == QATypeEnum.MultipleChoice and not set(v).issubset(_answers):
            raise ValueError("answer must be subset of answers")
        if _type in (QATypeEnum.MatchingChoice, QATypeEnum.RangingChoice) and not set(
            v
        ) == set(_answers):
            raise ValueError("answer must contain all answers")
        return v


class QACreateResult(BaseModel):
    ids: list[str]
    is_new: bool
