# Base stage for common environment setup
FROM python:3.10.13-alpine3.19 AS python-base

# Set work directory
WORKDIR /opt/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    VENV_PATH="/opt/app/.venv" \
    POETRY_VERSION=1.8.1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PROJECT_ROOT_NAME="docker_compose"

# Ensure scripts in .venv are callable'
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PATH="$VENV_PATH/bin:$PATH"

# Set the default shell to bash with pipefail option
SHELL ["/bin/sh", "-eo", "pipefail", "-c"]

RUN apk update && \
    apk add --no-cache curl

# Builder stage for installing dependencies and Poetry
FROM python-base AS venv-builder

# Copy pyproject and poetry.lock
COPY ../poetry.lock ./
COPY ../pyproject.toml ./

# Install system dependencies required for Poetry
# https://python-poetry.org/docs/#installation
RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry install --only backend --no-root

# Final stage for the production image
FROM python-base AS production

# Copy installed python dependencies
COPY --from=venv-builder "$VENV_PATH" "$VENV_PATH"

# Copy entrypoint and application code
COPY "./$PROJECT_ROOT_NAME/configs/entrypoint.sh" ./
COPY "./$PROJECT_ROOT_NAME/configs/gunicorn.conf.py" ./
COPY "./$PROJECT_ROOT_NAME/app" ./

RUN adduser -D appuser && \
    chown -R appuser:appuser /opt/app && \
    chmod +x entrypoint.sh gunicorn.conf.py

# Switch to non-root user
USER appuser

# Use entrypoint.sh to perform initial setup tasks
ENTRYPOINT ["./entrypoint.sh"]

# Use Gunicorn to serve the app
CMD ["gunicorn", "-c", "./gunicorn.conf.py"]

