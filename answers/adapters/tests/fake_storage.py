import os
from contextlib import contextmanager
from typing import Callable, ContextManager

from adapters.QAStorage.MongoStorage import MongoStorage

StorageContextManager = Callable[[], ContextManager[MongoStorage]]

db_name = os.environ.get("TEST_MONGO_DB_NAME")


@contextmanager
def FakeMongoStorage():
    assert db_name
    store = MongoStorage()
    store.client.drop_database(db_name)
    yield store
    store.client.close()
