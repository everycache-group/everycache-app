FROM python:3.9-alpine

WORKDIR /code

RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps build-base gcc musl-dev postgresql-dev

COPY Pipfile* ./

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY . .
EXPOSE 8080

RUN chmod +x main.sh
CMD ["/bin/sh", "main.sh"]
