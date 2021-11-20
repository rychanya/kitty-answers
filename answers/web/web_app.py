import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


with open("./dist/manifest.json") as file:
    manifest = json.load(file)
    script = manifest["src/main.ts"]["file"]
    css = manifest["src/main.ts"]["css"]


app.mount("/assets", StaticFiles(directory="./dist/assets"))

templates = Jinja2Templates(directory="templates")


@app.get("/{p:path}", response_class=HTMLResponse)
def main_(request: Request, p):
    if p and p[-1] == "/":
        root_path = request.scope.get("root_path")
        print(root_path)
        return RedirectResponse(f"{root_path}/{p[:-1]}")
    return templates.TemplateResponse(
        "index.html", {"request": request, "css": css, "script": script}
    )
