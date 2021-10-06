from typing import Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
app.mount("/web", StaticFiles(directory="../kitty/dist"))

with open("../kitty/dist/index.html") as file:
    home_page = file.read()

@app.post("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/{p:path}", response_class=HTMLResponse)
@app.get("/", response_class=HTMLResponse)
def root():
    return home_page

