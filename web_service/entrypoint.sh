#!/bin/sh

# Exit script in case of error
set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser
# check if superuser exists
does_su_exist=$(python manage.py shell -c "from django.contrib.auth.models import User; \
                           import os; \
                           email = os.getenv('DJANGO_SUPERUSER_EMAIL'); \
                           exists = User.objects.filter(email=email).exists(); \
                           print(exists)")

# create superuser if it doesn't exist
if [ "$does_su_exist" == "False" ]; then
  echo "Creating superuser..."
  python manage.py createsuperuser --noinput
fi

# Start server
echo "Starting server..."
exec "$@"