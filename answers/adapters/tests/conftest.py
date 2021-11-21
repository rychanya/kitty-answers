import os

import pytest
from dotenv import load_dotenv
from pytest_mock import MockerFixture

from adapters.QAStorage.MongoStorage import MongoStorage
from models.qa import QAInputDTO, QATypeEnum

load_dotenv()


@pytest.fixture
def MongoStorageMock(mocker: MockerFixture):
    db_name = os.environ.get("TEST_MONGO_DB_NAME")
    password = os.environ.get("TEST_MONGO_PASSWORD")
    user = os.environ.get("TEST_MONGO_USER")
    mocker.patch("adapters.QAStorage.MongoStorage.settings.MONGO_DB_NAME", db_name)
    mocker.patch("adapters.QAStorage.MongoStorage.settings.MONGO_PASSWORD", password)
    mocker.patch("adapters.QAStorage.MongoStorage.settings.MONGO_USER", user)
    storage = MongoStorage()
    yield storage
    storage.client.drop_database(db_name)

@pytest.fixture
def qa_complete_only_choice_1():
    return QAInputDTO(
        by=None,
        type=QATypeEnum.OnlyChoice,
        question="qa_complete_only_choice_1",
        answers=["qcac1", "qcac2", "qcac3", "qcac4"],
        correct="qcac2",
        incorrect=["qcac3", "qcac4"],
        is_incomplete=False
    )
