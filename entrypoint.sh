#!/bin/bash

export DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
export DJANGO_DEBUG=$DJANGO_DEBUG

# However, it's generally recommended to run migrations outside the
# Docker build process, because the build should be environment-agnostic.
# Instead, you can run the migration as a separate step when deploying
# the container. For example, you can add the following line in your
# docker-compose.yml file under the command section:
# command: ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
cd /opt/sherlock/sherlock_rest_service && python3 manage.py migrate

env
exec python manage.py runserver 0.0.0.0:8000

