# Builder stage for installing dependencies and Poetry
FROM python-venv-builder:0.1.0 AS venv-builder

WORKDIR /opt/app

SHELL ["/bin/sh", "-eo", "pipefail", "-c"]

# https://python-poetry.org/docs/#installation
RUN poetry install --only backend --no-root --no-dev

# Final stage for the production image
FROM python-base:0.1.0 AS production

# Copy installed python dependencies
COPY --from=venv-builder "$VENV_PATH" "$VENV_PATH"

# Copy entrypoint and application code
COPY web_service ./

RUN adduser -D webuser && \
    mkdir -p /opt/app/static/admin && \
    chown -R webuser:webuser /opt/app && \
    chmod +x entrypoint.sh gunicorn.conf.py

# Switch to non-root user
USER webuser

# Use entrypoint.sh to perform initial setup tasks
ENTRYPOINT ["./entrypoint.sh"]

# Use Gunicorn to serve the web_service
CMD ["gunicorn", "-c", "./gunicorn.conf.py"]