import certifi
from pymongo import MongoClient
from answers.models.settings import MongoSettings
import gridfs

settings = MongoSettings()


client = MongoClient(
    f"mongodb+srv://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@cluster0.ys89g.mongodb.net/{settings.MONGO_DB_NAME}?retryWrites=true&w=majority",
    tlsCAFile=certifi.where(),
)

fs = gridfs.GridFS(client.get_database())
