#!/bin/bash

export DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
export DJANGO_DEBUG=$DJANGO_DEBUG
export ALLOWED_HOSTS=$ALLOWED_HOSTS

cd /opt/sherlock/sherlock_rest_service

exec python manage.py runserver 0.0.0.0:8000
#exec gunicorn sherlock_rest_service.wsgi:application --bind 0.0.0.0:8000 --workers 3

