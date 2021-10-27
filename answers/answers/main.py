from fastapi import FastAPI
from answers.routers import add_routs

app = FastAPI()

add_routs(app)

