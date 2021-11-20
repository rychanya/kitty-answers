from fastapi import APIRouter, Depends

from services.qa import GetByIdUseCase
from web.dependencies.qa import get_use_case

router = APIRouter(prefix="/qa", tags=["QA"])


@router.get("/{id}")
def get_by_id(id: str, use_case: GetByIdUseCase = Depends(get_use_case)):
    return use_case.execute(id)
