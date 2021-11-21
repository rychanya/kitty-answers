from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from adapters.QAStorage.BaseQAStorage import InvalidQAIdException, QANotExistException
from web.routes import qa

app = FastAPI(title="Kitten", version="3.1.0")


app.include_router(qa.router)


@app.exception_handler(InvalidQAIdException)
def handle_invalid_qa_id(request: Request, exc: InvalidQAIdException):
    return JSONResponse(
        content={"error": f"{exc.str_id} is not valid id"},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.exception_handler(QANotExistException)
def handle_qa_not_exist(request: Request, exc: QANotExistException):
    return JSONResponse(
        content={"error": f"qa with id {exc.str_id} not exist"},
        status_code=status.HTTP_404_NOT_FOUND,
    )
