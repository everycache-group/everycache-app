FROM python:3.9-alpine
WORKDIR /code
RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps build-base gcc musl-dev postgresql-dev
COPY Pipfile Pipfile
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install
EXPOSE 8080
COPY . .
RUN chmod +x main.sh
CMD ["pipenv", "run", "/bin/sh", "main.sh"]
