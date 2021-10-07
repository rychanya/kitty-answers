from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

with open("../kitty/dist/index.html") as file:
    home_page = file.read()

@router.get("/{p:path}", response_class=HTMLResponse)
@router.get("/", response_class=HTMLResponse)
def root():
    return home_page