from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from answers.routers import qa, web


def add_web(func):
    def wraper(app: FastAPI):
        app.mount("/static", StaticFiles(directory="../kitty/dist"))
        func(app)
        app.include_router(web.router)

    return wraper


@add_web
def add_routs(app: FastAPI):
    app.include_router(qa.router, prefix="/qa")
