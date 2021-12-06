import abc
from typing import Optional

from models.qa import QA, QABase, QACreateResult, QAGroup, QAInputDTO


class BaseQAStorage(abc.ABC):
    @abc.abstractstaticmethod
    def str_to_id(self, str_id: str):
        ...

    @abc.abstractmethod
    def get_qa_by_id(self, str_id: str) -> QA:
        ...

    @abc.abstractmethod
    def get_qa_base_by_id(self, str_id: str) -> QABase:
        ...

    @abc.abstractmethod
    def get_qa_group_by_id(self, str_id: str) -> QAGroup:
        ...

    @abc.abstractmethod
    def get_or_create_qa(self, dto: QAInputDTO) -> QACreateResult:
        ...

    @abc.abstractclassmethod
    def get_or_create_qa_group(self, dto: QAGroup) -> Optional[QAGroup]:
        ...

    @abc.abstractclassmethod
    def get_or_create_qa_base(self, dto: QABase) -> QABase:
        ...


class InvalidQAIdException(Exception):
    def __init__(self, str_id: str) -> None:
        self.str_id = str_id


class StorageException(Exception):
    def __init__(self, msg: str) -> None:
        self.msg = msg


class NotExistExeption(Exception):
    def __init__(self, str_id) -> None:
        self.str_id = str_id


class AlredyExistExeption(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg


class QANotExistException(Exception):
    def __init__(self, str_id) -> None:
        self.str_id = str_id
