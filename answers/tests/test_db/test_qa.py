import pytest
from pytest_mock import MockerFixture

from answers.db import client


@pytest.fixture
def qa_client(mocker: MockerFixture):
    collection_name = "TEST_QA"
    mocker.patch("answers.db.qa.COL_NAME", collection_name)
    yield client.get_database().get_collection(collection_name)
    client.get_database().drop_collection(collection_name)
