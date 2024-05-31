#!/bin/bash
set -e
set -x

{
  echo "requirepass $REDIS_PASSWORD"
  echo "aclfile /etc/redis/users.acl"
  echo "save 20 1"
  echo "loglevel warning"
} > /etc/redis/redis.conf

{
  echo "user $REDIS_USER on >$REDIS_PASSWORD ~* &* +@all"
  echo "user $AUTH_REDIS_USER on >$AUTH_REDIS_PASSWORD ~auth:* &auth:* +get +set +del +select"
  echo "user $APP_REDIS_USER on >$APP_REDIS_PASSWORD ~movies:* &movies:* +get +set +del +select"
} > /etc/redis/users.acl

chmod 600 /etc/redis/redis.conf
chmod 600 /etc/redis/users.acl

exec redis-server /etc/redis/redis.conf
