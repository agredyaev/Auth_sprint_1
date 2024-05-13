FROM python-base:0.1.0 AS base

ENV ES_DSN="http://elasticsearch:9200"

WORKDIR /opt/app

COPY db/elasticsearch/indices ./indices
COPY docker/create_indices.sh ./

RUN chmod +x create_indices.sh

CMD ["sh", "./create_indices.sh"]