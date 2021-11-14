from fastapi import FastAPI

from answers.routers import qa, rating, search, upload

app = FastAPI()
app.include_router(qa.router)
app.include_router(upload.router)
app.include_router(rating.router)
app.include_router(search.router)
