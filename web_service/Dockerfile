# Builder stage for installing dependencies and Poetry
FROM python-venv-builder:0.1.0 AS venv-builder

WORKDIR "${BASE_PATH}"

# https://python-poetry.org/docs/#installation
RUN poetry install --only backend --no-root --only main

# Final stage for the production image
FROM python-base:0.1.0 AS production

# Copy installed python dependencies
COPY --from=venv-builder "$VENV_PATH" "$VENV_PATH"

# Copy entrypoint and application code
COPY web_service ./

ARG USERNAME=web

RUN mkdir -p "${BASE_PATH}"/static/admin && \
    ./setup_user.sh "${GID}" "${UID}" "${USERNAME}" && \
    chmod +x entrypoint.sh gunicorn_conf.py

# Switch to non-root user
USER "${USERNAME}"

# Use entrypoint.sh to perform initial setup tasks
ENTRYPOINT ["./entrypoint.sh"]

# Use Gunicorn to serve the web_service
CMD ["gunicorn", "-c", "./gunicorn_conf.py"]