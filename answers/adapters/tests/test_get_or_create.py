from adapters.QAStorage.MongoStorage import MongoStorage


def test_(MongoStorageMock: MongoStorage):
    MongoStorageMock.client.get_database().get_collection(
        MongoStorageMock.QA_NAME
    ).insert_one({})
    assert True
