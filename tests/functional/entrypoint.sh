#!/bin/bash

set -e
set -x

if [ -z "${BASE_PATH}" ]; then
  echo "BASE_PATH is not set"
  exit 1
fi

cd "${BASE_PATH}"
python -m tests.functional.utils.wait_for_es
python -m tests.functional.utils.wait_for_redis
pytest tests/functional/src
