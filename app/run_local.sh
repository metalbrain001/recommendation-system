#!/bin/sh

# Set the Django settings module
export DJANGO_SETTINGS_MODULE=app.settings

# Wait for Postgres to be ready
../wait-for-postgres.sh

# Run migrations
python manage.py migrate &&

# Start the Django development server
python manage.py runserver 0.0.0.0:8000