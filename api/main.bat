@echo off

waitress-serve %* --call "everycache_api.app:create_app"
