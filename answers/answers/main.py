from fastapi import FastAPI
from answers.routers import add_routs
from fastapi.staticfiles import StaticFiles

app = FastAPI()

add_routs(app)

