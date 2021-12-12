import os

import pytest
from dotenv import load_dotenv
from pytest_mock import MockerFixture

load_dotenv()


@pytest.fixture(autouse=True)
def MongoStorageMock(mocker: MockerFixture):
    db_name = os.environ.get("TEST_MONGO_DB_NAME")
    password = os.environ.get("TEST_MONGO_PASSWORD")
    user = os.environ.get("TEST_MONGO_USER")
    mocker.patch("adapters.QAStorage.MongoStorage.settings.MONGO_DB_NAME", db_name)
    mocker.patch("adapters.QAStorage.MongoStorage.settings.MONGO_PASSWORD", password)
    mocker.patch("adapters.QAStorage.MongoStorage.settings.MONGO_USER", user)
