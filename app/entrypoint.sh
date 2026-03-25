#!/bin/sh

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Seeding data..."
python manage.py seed_data

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000