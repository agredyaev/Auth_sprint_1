#!/bin/bash
set -e
set -x


python -m auth_service.migrations
gunicorn -c ./auth_service/gunicorn_conf.py auth_service.src.main:app