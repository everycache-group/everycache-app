#!/bin/bash

waitress-serve $@ --call "everycache_api.app:create_app"
