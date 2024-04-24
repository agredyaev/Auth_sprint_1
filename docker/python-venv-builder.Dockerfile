FROM python-base:0.1.0 AS venv-builder

WORKDIR /opt/app

SHELL ["/bin/sh", "-eo", "pipefail", "-c"]

# Copy pyproject and poetry.lock
COPY poetry.lock ./
COPY pyproject.toml ./

# Install system dependencies required for Poetry
# https://python-poetry.org/docs/#installation
RUN curl -sSL https://install.python-poetry.org | python -
