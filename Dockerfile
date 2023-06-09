# Use Python 3.11 slim image as base
FROM python:3.11-slim-bullseye as build

# Set working directory
WORKDIR /wheels

# Copy requirements.txt
COPY requirements.txt /opt/sherlock/

# Install build dependencies and generate wheels
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && pip3 wheel -r /opt/sherlock/requirements.txt \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Use Python 3.11 slim image for runtime
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV VCS_REF ""
ENV VCS_URL "https://github.com/sherlock-project/sherlock"

# Set working directory
WORKDIR /opt/sherlock

# Copy wheels and app files
COPY --from=build /wheels /wheels
COPY requirements.txt /opt/sherlock
RUN pip3 install --upgrade pip \
  && pip3 install --no-cache-dir -r requirements.txt -f /wheels \
  && rm -rf /wheels

# Copy app files
COPY . /opt/sherlock/

RUN rm /opt/sherlock/sherlock_rest_service/sherlock

# Move sherlock files into the Django project
RUN mv /opt/sherlock/sherlock /opt/sherlock/sherlock_rest_service

# Expose port for Django server
EXPOSE 8000

# Copy entrypoint script
COPY entrypoint.sh /opt/sherlock/

# Set entrypoint
ENTRYPOINT ["/opt/sherlock/entrypoint.sh"]
#CMD DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY DJANGO_DEBUG=$DJANGO_DEBUG python manage.py runserver 0.0.0.0:8000