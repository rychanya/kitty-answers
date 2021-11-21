from adapters.QAStorage.BaseQAStorage import BaseQAStorage


class GetByIdUseCase:
    def __init__(self, storage: BaseQAStorage) -> None:
        self.storage = storage

    def execute(self, str_id: str):
        return self.storage.get_qa_by_id(str_id=str_id)
