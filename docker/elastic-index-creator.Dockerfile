# Base image
FROM python-base:0.1.0 AS base

ENV ES_DSN="http://elasticsearch:9200" \
    ES_DIR="db/elasticsearch" \
    SCRIPT_FILE="elasticsearch_operations.sh" \
    DATA_DIR="indices" \
    SCRIPT_DIR="docker" \
    OPERATION="create_index"

# Set work directory
WORKDIR /opt/app

# Copy entrypoint and application code
COPY "${ES_DIR}"/"${DATA_DIR}" ./"${DATA_DIR}"
COPY "${SCRIPT_DIR}"/"${SCRIPT_FILE}" ./

# Install elasticdump
RUN chmod +x "${SCRIPT_FILE}"

# Set default command
ENTRYPOINT ["bash", "-c","./${SCRIPT_FILE} ${DATA_DIR} ${OPERATION}"]

