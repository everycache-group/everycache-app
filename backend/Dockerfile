FROM python:3.9.0-slim

WORKDIR /app

RUN pip install -U pip
RUN pip install pipenv waitress

COPY Pipfile* ./
RUN pipenv install --system --deploy

COPY everycache_api everycache_api
COPY migrations migrations/
