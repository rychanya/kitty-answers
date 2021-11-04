from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class MongoSettings(BaseSettings):
    MONGO_DB_NAME: str
    MONGO_PASSWORD: str
    MONGO_USER: str


class Auth0Settings(BaseSettings):
    VUE_APP_AUTH0_DOMAIN: str
    VUE_APP_AUTH0_AUDIENCE: str
    AUTH0_ALGORITHMS: str
    AUTH0_ISSUER: str
