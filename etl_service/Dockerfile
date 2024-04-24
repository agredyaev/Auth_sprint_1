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
COPY etl_service ./

RUN adduser -D etluser && \
    chown -R etluser:etluser /opt/web_service

# Switch to non-root user
USER etluser

# Use entrypoint.sh to perform run tasks
ENTRYPOINT ["python", "-m", "/opt/app/etl_service.main"]