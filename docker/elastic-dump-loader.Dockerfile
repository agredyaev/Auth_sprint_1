FROM node:current-alpine3.19 AS builder

# Set environment variables
ENV ES_DSN="http://elasticsearch:9200" \
    ES_DIR="db/elasticsearch" \
    SCRIPT_FILE="elasticsearch_operations.sh" \
    DATA_DIR="dumps" \
    SCRIPT_DIR="docker" \
    OPERATION="load_dump"

# Set work directory
WORKDIR /opt/app

# Copy entrypoint and application code
COPY "${ES_DIR}"/"${DATA_DIR}" ./"${DATA_DIR}"
COPY "${SCRIPT_DIR}"/"${SCRIPT_FILE}" ./

# Install elasticdump
RUN chmod +x "${SCRIPT_FILE}" \
    && npm install -g elasticdump

# Set default command
ENTRYPOINT ["bash", "-c","./${SCRIPT_FILE} ${DATA_DIR} ${OPERATION}"]