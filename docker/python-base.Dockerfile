# Base stage for docker environment setup
FROM --platform=linux/amd64 python:3.10.13-alpine3.19 AS python-base

# Set work directory
WORKDIR /opt/app

# Set environment variables
    # user
ENV GID=1000 \
    UID=1000 \
    # python
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # poetry
    POETRY_HOME="/opt/poetry" \
    POETRY_VERSION=1.8.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    # paths
    BASE_PATH="/opt/app"

# Ensure scripts in .venv are callable
ENV PYTHONPATH="$BASE_PATH"
ENV VENV_PATH="$BASE_PATH/.venv"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PATH="$VENV_PATH/bin:$PATH"

# Set the default shell to bash with pipefail option
SHELL ["/bin/sh", "-eo", "pipefail", "-c"]

COPY ./docker/setup_user.sh ./

RUN apk update && \
    apk add --no-cache bash curl && \
    chmod +x setup_user.sh