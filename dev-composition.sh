#!/bin/bash

docker-compose --env-file dev.env --file docker-compose.yaml --file docker-compose.dev.yaml $@
