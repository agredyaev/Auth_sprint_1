# Builder stage for installing dependencies and Poetry
FROM python-venv-builder:0.1.0 AS venv-builder

WORKDIR "${BASE_PATH}"

# https://python-poetry.org/docs/#installation
RUN poetry install --only functionaltest --no-root --only main

# Final stage for the production image
FROM python-base:0.1.0 AS production

ENV TESTS_PATH="/tests/auth_service"

# Copy installed python dependencies
COPY --from=venv-builder "$VENV_PATH" "$VENV_PATH"

# Copy entrypoint and application code
COPY "${TESTS_PATH}" "${BASE_PATH}""${TESTS_PATH}"

ARG USERNAME=functional_tests

RUN ./setup_user.sh "${GID}" "${UID}" "${USERNAME}" && \
    chmod +x "${BASE_PATH}""${TESTS_PATH}"/entrypoint.sh

# Switch to non-root user
USER "${USERNAME}"

ENTRYPOINT ["sh", "-c", "${BASE_PATH}${TESTS_PATH}/entrypoint.sh"]