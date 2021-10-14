from pydantic import BaseSettings

class MongoSettings(BaseSettings):
    MONGO_DB_NAME: str
    MONGO_PASSWORD: str
    MONGO_USER: str
