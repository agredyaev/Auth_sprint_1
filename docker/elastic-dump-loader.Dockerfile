FROM node:current-alpine3.19 AS builder

# Set environment variables
ENV ES_DSN="http://elasticsearch:9200" \
    ES_DIR="db/elasticsearch"

# Set work directory
WORKDIR /opt/app

# Copy entrypoint and application code
COPY "${ES_DIR}"/dumps ./dumps
COPY docker/elasticsearch_operations.sh ./

# Install elasticdump
RUN chmod +x elasticsearch_operations.sh \
    && npm install -g elasticdump

# Set the default shell to bash with pipefail option
SHELL ["/bin/sh", "-eo", "pipefail", "-c"]

# Set default command
CMD ["sh", "./elasticsearch_operations.sh"]