from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from answers.models import OIDStr

class Upload(BaseModel):
    class Config:
        json_encoders = {ObjectId: str}

    id: OIDStr = Field(None, alias="_id")
    file_id: Optional[OIDStr]
    by: OIDStr