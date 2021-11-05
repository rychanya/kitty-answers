ARG VUE_APP_AUTH0_DOMAIN
ARG VUE_APP_AUTH0_CLIENT_KEY
ARG VUE_APP_AUTH0_AUDIENCE


FROM node:16 as build-stage
ENV VUE_APP_AUTH0_DOMAIN=${VUE_APP_AUTH0_DOMAIN}
ENV VUE_APP_AUTH0_CLIENT_KEY=${VUE_APP_AUTH0_CLIENT_KEY}
ENV VUE_APP_AUTH0_AUDIENCE=${VUE_APP_AUTH0_AUDIENCE}
WORKDIR /kitty
COPY ./kitty/package*.json /kitty
RUN npm install
COPY ./kitty /kitty
RUN npm run build


FROM python:3.9 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./answers/pyproject.toml ./answers/poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.9
WORKDIR /answers
COPY --from=requirements-stage /tmp/requirements.txt /answers/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /answers/requirements.txt
COPY ./answers /answers
COPY --from=build-stage /kitty/dist /kitty/dist
# CMD uvicorn answers.main:app --host 0.0.0.0 --port ${PORT}