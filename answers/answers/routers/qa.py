from fastapi import APIRouter
from typing import Optional
from answers.tasks import add

router = APIRouter()

@router.post("/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    # return {"item_id": item_id, "q": q}
    return add.delay(str(item_id), q).id