from services.qa import GetByIdUseCase
from web.dependencies import get_storege


def get_use_case():
    return GetByIdUseCase(storage=get_storege())
