FROM node:latest as build-stage
WORKDIR /kitty
COPY ./kitty/package*.json /kitty
RUN npm install
COPY ./kitty /kitty
RUN npm run build


FROM python:3.9
WORKDIR /answers
COPY ./answers/requirements.txt /answers
RUN pip install --no-cache-dir --upgrade -r /answers/requirements.txt
COPY ./answers /answers
COPY --from=build-stage /kitty/dist /kitty/dist
CMD uvicorn answers.main:app --host 0.0.0.0 --port ${PORT}