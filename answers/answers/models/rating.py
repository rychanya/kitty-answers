from bson import ObjectId
from pydantic import BaseModel, Field

from answers.models import OIDStr


class Rating(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}

    id: OIDStr = Field(..., alias="_id")
    likes_count: int
    dislikes_count: int
    is_liked: bool
    is_disliked: bool
