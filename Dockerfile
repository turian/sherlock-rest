# Use Python 3.11 slim image as base
FROM python:3.11-slim-bullseye as build

# Set working directory
WORKDIR /wheels

# Copy requirements.txt
COPY requirements.txt /opt/sherlock/

# Install build dependencies and generate wheels
RUN apt-get update \
  && apt-get install -y build-essential \
  && pip3 wheel -r /opt/sherlock/requirements.txt

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
COPY . /opt/sherlock/

RUN pip3 install --upgrade pip

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt -f /wheels \
  && rm -rf /wheels

# Move sherlock files into the Django project
RUN mv /opt/sherlock/sherlock /opt/sherlock/sherlock_rest_service

# However, it's generally recommended to run migrations outside the
# Docker build process, because the build should be environment-agnostic.
# Instead, you can run the migration as a separate step when deploying
# the container. For example, you can add the following line in your
# docker-compose.yml file under the command section:
# command: ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
RUN cd /opt/sherlock/sherlock_rest_service && python3 manage.py migrate

# Expose port for Django server
EXPOSE 8000

# Start Django server
CMD ["python", "/opt/sherlock/sherlock_rest_service/manage.py", "runserver", "0.0.0.0:8000"]
