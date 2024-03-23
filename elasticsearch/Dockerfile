FROM docker.elastic.co/elasticsearch/elasticsearch:8.6.2

EXPOSE 9200

ENV discovery.type=single-node
ENV xpack.security.enabled=false
ENV ES_JAVA_OPTS="-Xms200m -Xmx200m"
