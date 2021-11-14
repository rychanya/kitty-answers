from enum import Enum
from typing import Optional, Union

from bson import ObjectId
from pydantic import BaseModel, Field, validator

from answers.models import OIDStr
from answers.models.qa import QATypeEnum, SearchResultEl


class UploadTypeEnum(str, Enum):
    OnlyChoice = "единственный выбор"
    MultipleChoice = "множественный выбор"
    RangingChoice = "ранжирование"
    MatchingChoice = "соответствие"


class UploadQAinDB(BaseModel):
    class Config:
        use_enum_values = True
        json_encoders = {ObjectId: str}

    id: OIDStr = Field(..., alias="_id")
    type: QATypeEnum
    question: str
    is_corect: bool
    answers: list[str]
    answer: Union[str, list[str]]
    ids: Optional[list[OIDStr]]
    isNew: Optional[bool]

    def to_qa(self, by: ObjectId):
        return SearchResultEl(
            by=by,
            type=self.type,
            question=self.question,
            answers=self.answers,
            correct=(self.answer if self.is_corect else None),
            incorrect=([self.answer] if not self.is_corect else []),
            incomplete=True,
        )


class UploadQA(BaseModel):
    class Config:
        use_enum_values = True

    type: QATypeEnum = Field(..., alias="Тип")
    question: str = Field(..., alias="Вопрос")
    is_corect: bool = Field(..., alias="Правильный")
    answers: list[str] = Field(..., alias="Ответ")
    answer: Union[str, list[str]] = Field(..., alias="Ответ")

    @validator("type", pre=True)
    def validate_type(cls, v):
        if v == UploadTypeEnum.OnlyChoice:
            return QATypeEnum.OnlyChoice
        if v == UploadTypeEnum.MultipleChoice:
            return QATypeEnum.MultipleChoice
        if v == UploadTypeEnum.RangingChoice:
            return QATypeEnum.RangingChoice
        if v == UploadTypeEnum.MatchingChoice:
            return QATypeEnum.MatchingChoice
        raise ValueError

    @validator("is_corect", pre=True)
    def validate_correct(cls, v):
        if v == "+":
            return True
        if v == "-":
            return False
        raise ValueError

    @validator("answers", pre=True)
    def validte_answers(cls, v):
        return [el.removesuffix(";_x000D_") for el in str(v).split("\n")]

    @validator("answer", pre=True)
    def validte_answer(cls, v, values):
        type = values.get("type")
        if type == QATypeEnum.OnlyChoice:
            return v
        elif type in (
            QATypeEnum.MultipleChoice,
            QATypeEnum.MatchingChoice,
            QATypeEnum.RangingChoice,
        ):
            return [el.removesuffix(";_x000D_") for el in str(v).split("\n")]
        else:
            raise ValueError


class Upload(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}

    id: OIDStr = Field(None, alias="_id")
    by: OIDStr
    row_data: list[OIDStr] = []


class UploadinDB(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}

    id: OIDStr = Field(None, alias="_id")
    by: OIDStr
    row_data: list[UploadQAinDB] = []
