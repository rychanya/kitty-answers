FROM python:3.9 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./answers/pyproject.toml ./answers/poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM node:16 as build-stage
WORKDIR /kitty
COPY ./kitty/package*.json /kitty/
RUN npm install
COPY ./kitty /kitty
RUN npm run build


FROM python:3.9
WORKDIR /answers
COPY --from=requirements-stage /tmp/requirements.txt /answers/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /answers/requirements.txt
COPY ./answers /answers
COPY --from=build-stage /answers/dist /answers/dist
# CMD uvicorn answers.main:app --host 0.0.0.0 --port ${PORT}