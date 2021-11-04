from bson import ObjectId
from pydantic import BaseModel, Field

from answers.models import OIDStr


class User(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}

    id: OIDStr = Field(None, alias="_id")
    sub: str
