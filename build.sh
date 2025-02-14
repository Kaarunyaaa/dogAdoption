#!/bin/bash

# Exit on error
set -o errexit  

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the server (if needed, Render may handle this separately)
# gunicorn your_project_name.wsgi:application --bind 0.0.0.0:$PORT
