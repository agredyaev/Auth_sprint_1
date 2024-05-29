# Builder stage for installing dependencies and Poetry
FROM python-venv-builder:0.1.0 AS venv-builder

WORKDIR "${BASE_PATH}"

# https://python-poetry.org/docs/#installation
RUN poetry install --only auth --no-root --only main

# Final stage for the production image
FROM python-base:0.1.0 AS production

# Copy installed python dependencies
COPY --from=venv-builder "$VENV_PATH" "$VENV_PATH"

# Copy entrypoint and application code
COPY auth_service /opt/app/auth_service

ARG USERNAME=auth

RUN ./setup_user.sh "${GID}" "${UID}" "${USERNAME}"


# Switch to non-root user
USER "${USERNAME}"

# Use entrypoint.sh to perform run tasks
CMD ["gunicorn", "-c", "./auth_service/gunicorn_conf.py", "auth_service.src.main:app"]