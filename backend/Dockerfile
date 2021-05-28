FROM python:3.9.0-slim

WORKDIR /app

RUN pip install -U pip
RUN pip install pipenv

COPY . ./
RUN pipenv install


CMD pipenv run python main.py run
