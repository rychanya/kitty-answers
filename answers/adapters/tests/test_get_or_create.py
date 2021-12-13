from datetime import timedelta

from hypothesis import given, settings

from adapters.QAStorage.AbstractQAStorage import QADTO
from adapters.tests.fake_data import QADTOSrtategies
from adapters.tests.fake_storage import FakeMongoStorage


@given(QADTOSrtategies())
@settings(deadline=None)
def test_tt(dto: QADTO):
    with FakeMongoStorage() as store:
        qa, is_new = store.get_or_create(dto)
        assert qa.is_correct == dto.is_correct
        assert qa.answer == dto.answer
        assert (qa.group_id is None) == (dto.group is None)
        assert is_new
