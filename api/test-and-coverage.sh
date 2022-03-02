#!/bin/bash

pipenv run pytest -vvv --cov-report term-missing --cov=everycache_api everycache_api/tests

