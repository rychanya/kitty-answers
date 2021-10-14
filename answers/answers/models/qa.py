from typing import Optional, Union
from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field

from answers.models import OIDStr



class QATypeEnum(str, Enum):
    OnlyChoice = "Выберите один правильный вариант"
    MultipleChoice = "Выберите все правильные варианты"
    RangingChoice = "Перетащите варианты так, чтобы они оказались в правильном порядке"
    MatchingChoice = "Соедините соответствия справа с правильными вариантами"


AnswerType = Union[str, list, dict[str, str]]


class SearchResultEl(BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True

    id: OIDStr = Field(None, alias="_id")
    by: Optional[OIDStr]
    type: QATypeEnum
    question: str
    answers: list[str]
    extra_answers: list[str] = []
    correct: Optional[AnswerType]
    incorrect: list[AnswerType] = []
    incomplete: bool = False


class SearchResultGroup(BaseModel):
    class Config:
        use_enum_values = True

    type: QATypeEnum
    question: str


class SearchResult(BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

    id: SearchResultGroup = Field(..., alias="_id")
    data: list[SearchResultEl]