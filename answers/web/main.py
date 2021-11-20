from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from web import api_app, web_app

app = FastAPI(title="Kitten", version="3.1.0")
app.mount("/web", web_app.app)
app.mount("/api", api_app.app)


@app.get("/")
def redirect_to_home():
    return RedirectResponse("/web/")
