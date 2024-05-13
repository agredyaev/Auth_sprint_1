FROM python-base:0.1.0 AS base

ENV BASE_DIR="/opt/app" \
    ES_DSN="http://localhost:9200"

WORKDIR "${BASE_DIR}"

COPY db/elasticsearch/indices "${BASE_DIR}"
COPY docker/create_indices.sh "${BASE_DIR}"

RUN chmod +x create_indices.sh

CMD ["sh", "-c", "create_indices.sh"]