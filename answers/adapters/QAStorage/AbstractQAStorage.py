import abc
from typing import Optional, Tuple

from pydantic import BaseModel
from pydantic.types import ConstrainedStr as ConstrainedStrBase


class ConstrainedStr(ConstrainedStrBase):
    strip_whitespace = True
    min_length = 1
    max_length = 200


from answers.models.qa import QATypeEnum


class QuestionDTO(BaseModel):
    class Config:
        use_enum_values = True

    id: Optional[str]
    question: ConstrainedStr
    type: QATypeEnum


class GroupDTO(BaseModel):
    id: Optional[str]
    all_answers: list[ConstrainedStr]
    all_extra_answers: list[ConstrainedStr]


class QAINDTO(BaseModel):
    id: Optional[str]
    question: QuestionDTO
    group: Optional[GroupDTO]
    answer: list[ConstrainedStr]


class AbstractQAStorage(abc.ABC):
    @abc.abstractmethod
    def get_or_create(self, in_dto: QAINDTO) -> Tuple[str, bool]:
        ...
