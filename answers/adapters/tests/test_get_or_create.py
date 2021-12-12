from hypothesis import given

from adapters.QAStorage.MongoStorage import QADTO
from adapters.tests.fake_data import QADTOSrtategies
from adapters.tests.fake_storage import FakeMongoStorage


@given(QADTOSrtategies())
def test_tt(dto: QADTO):
    with FakeMongoStorage() as store:
        print(dto.group)
        store.get_or_create(dto)
        assert False
