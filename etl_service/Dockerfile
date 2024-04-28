# Builder stage for installing dependencies and Poetry
FROM python-venv-builder:0.1.0 AS venv-builder

WORKDIR /opt/app

SHELL ["/bin/sh", "-eo", "pipefail", "-c"]

# https://python-poetry.org/docs/#installation
RUN poetry install --only etl --no-root --no-dev

# Final stage for the production image
FROM python-base:0.1.0 AS production

# Copy installed python dependencies
COPY --from=venv-builder "$VENV_PATH" "$VENV_PATH"

# Copy entrypoint and application code
COPY etl_service /opt/app/etl_service

RUN addgroup -g "${GID}" etl && \
    adduser -D -h /opt/app -u "${UID}" -G etl etl && \
    chown -R etl:etl /opt/app

# Switch to non-root user
USER etl

# Use entrypoint.sh to perform run tasks
ENTRYPOINT ["python", "-m", "etl_service.main"]

