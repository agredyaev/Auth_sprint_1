#!/bin/sh

# Exit script in case of error
set -e

# Make migrations
echo "Making database migrations..."
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
exec "$@"