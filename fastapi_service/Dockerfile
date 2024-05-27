# Builder stage for installing dependencies and Poetry
FROM python-venv-builder:0.1.0 AS venv-builder

WORKDIR "${BASE_PATH}"

# https://python-poetry.org/docs/#installation
RUN poetry install --only fastapi --no-root --only main

# Final stage for the production image
FROM python-base:0.1.0 AS production

# Copy installed python dependencies
COPY --from=venv-builder "$VENV_PATH" "$VENV_PATH"

# Copy entrypoint and application code
COPY fastapi_service /opt/app/fastapi_service

ARG USERNAME=fastapi

RUN ./setup_user.sh "${GID}" "${UID}" "${USERNAME}"


# Switch to non-root user
USER "${USERNAME}"

# Use entrypoint.sh to perform run tasks
CMD ["gunicorn", "-c", "./fastapi_service/gunicorn_conf.py", "fastapi_service.src.main:app"]