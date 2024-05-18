# Base image
FROM python-base:0.1.0 AS base

# Set environment variables
ENV ES_DSN="http://elasticsearch:9200" \
    ES_DIR="db/elasticsearch"

# Set work directory
WORKDIR /opt/app

# Copy entrypoint and application code
COPY "${ES_DIR}"/indices ./indices
COPY docker/elasticsearch_operations.sh ./

# Set entrypoint
RUN chmod +x elasticsearch_operations.sh

# Set default command
CMD ["sh", "./elasticsearch_operations.sh"]