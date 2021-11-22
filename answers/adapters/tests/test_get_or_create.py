import pytest

from adapters.QAStorage.MongoStorage import MongoStorage
from models.qa import QAInputDTO, QATypeEnum


def qa_complete_only_choice_1():
    return QAInputDTO(
        by=None,
        type=QATypeEnum.OnlyChoice,
        question="qa_complete_only_choice_1",
        answers=["qcac1", "qcac2", "qcac3", "qcac4"],
        correct="qcac2",
        incorrect=["qcac3", "qcac4"],
        is_incomplete=False,
    )


@pytest.mark.parametrize("qa", [qa_complete_only_choice_1()])
def test_create(MongoStorageMock: MongoStorage, qa: QAInputDTO):
    assert MongoStorageMock.qa_collection.count_documents({}) == 0
    res = MongoStorageMock.get_or_create(qa)
    assert MongoStorageMock.qa_collection.count_documents({}) == 1
    assert res.is_new
    id = MongoStorageMock.qa_collection.find_one({})
    assert id and str(id["_id"]) == res.ids[0]
