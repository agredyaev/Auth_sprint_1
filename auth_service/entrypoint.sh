#!/bin/bash
set -e
set -x


cd auth_service
alembic revision --autogenerate
alembic upgrade head
gunicorn -c ./gunicorn_conf.py auth_service.src.main:app