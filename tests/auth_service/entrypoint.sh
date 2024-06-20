#!/bin/bash

set -e
set -x

if [ -z "${BASE_PATH}" ]; then
  echo "BASE_PATH is not set"
  exit 1
fi

cd "${BASE_PATH}"
python -m tests.auth_service.utils.wait_for_redis
python -m tests.auth_service.utils.wait_for_app
pytest tests/auth_service/src
