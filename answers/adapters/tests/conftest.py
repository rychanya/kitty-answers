import pytest
from pytest_mock import MockerFixture

from adapters.MongoStorage import MongoStorage


@pytest.fixture
def MongoStorageMock(mocker: MockerFixture):
    db_name = "TEST_DB_TEST"
    mocker.patch("adapters.MongoStorage.settings.MONGO_DB_NAME", db_name)
    storage = MongoStorage()
    yield storage
    storage.client.drop_database(db_name)
