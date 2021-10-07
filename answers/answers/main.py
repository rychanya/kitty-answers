from fastapi import FastAPI
from answers.routers import add_routs

app = FastAPI()
# app.mount("/static", StaticFiles(directory="../kitty/dist"))

add_routs(app)
