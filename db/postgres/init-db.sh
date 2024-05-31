#!/usr/bin/bash

set -e
set -x

# create user and database for app service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${APP_POSTGRES_USER} WITH PASSWORD '${APP_POSTGRES_PASSWORD}';
    CREATE DATABASE ${APP_POSTGRES_DB} OWNER ${APP_POSTGRES_USER};
EOSQL

# execute init script for app service
psql -v ON_ERROR_STOP=1 --username "$APP_POSTGRES_USER" --dbname "$APP_POSTGRES_DB" < /docker-entrypoint-initdb.d/app_service/init.sql


# create user and database for auth service
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${AUTH_POSTGRES_USER} WITH PASSWORD '${AUTH_POSTGRES_PASSWORD}';
    CREATE DATABASE ${AUTH_POSTGRES_DB} OWNER ${AUTH_POSTGRES_USER};
EOSQL

# execute init script for auth service
psql -v ON_ERROR_STOP=1 --username "$AUTH_POSTGRES_USER" --dbname "$AUTH_POSTGRES_DB" < /docker-entrypoint-initdb.d/auth_service/init.sql