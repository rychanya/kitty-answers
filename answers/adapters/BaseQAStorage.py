import abc

from models.qa import QA, QACreateResult, QAInputDTO


class BaseQAStorage(abc.ABC):
    @abc.abstractmethod
    def get_qa_by_id(self, str_id: str) -> QA:
        ...

    @abc.abstractmethod
    def get_or_create(self, dto: QAInputDTO) -> QACreateResult:
        ...


class InvalidQAIdException(Exception):
    def __init__(self, str_id: str) -> None:
        self.str_id = str_id


class QANotExistException(Exception):
    def __init__(self, str_id) -> None:
        self.str_id = str_id
