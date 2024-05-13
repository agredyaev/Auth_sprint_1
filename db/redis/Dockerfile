FROM redis:7.2.4-alpine

COPY /db/redis/entrypoint.sh /etc/redis/entrypoint.sh

RUN chmod +x /etc/redis/entrypoint.sh

ENTRYPOINT ["sh", "/etc/redis/entrypoint.sh"]
