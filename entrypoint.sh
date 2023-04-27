#!/bin/bash

export DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
export DJANGO_DEBUG=$DJANGO_DEBUG

cd /opt/sherlock/sherlock_rest_service

# However, it's generally recommended to run migrations outside the
# Docker build process, because the build should be environment-agnostic.
# Instead, you can run the migration as a separate step when deploying
# the container. For example, you can add the following line in your
# docker-compose.yml file under the command section:
# command: ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
# Anyway, we don't actually use a database.
python3 manage.py migrate

#exec python manage.py runserver 0.0.0.0:8000
exec gunicorn sherlock_rest_service.wsgi:application --bind 0.0.0.0:8000 --workers 3

