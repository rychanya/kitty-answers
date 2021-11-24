import nox

nox.options.sessions = ["prety"]


@nox.session(py=False)
def prety(session: nox.Session):
    session.run("poetry", "run", "isort", ".")
    session.run("poetry", "run", "black", ".")
    session.run("poetry", "run", "flake8", ".")


@nox.session(py=False)
def serv(session: nox.Session):
    session.run("poetry", "run", "uvicorn", "web.main:app", "--reload")
