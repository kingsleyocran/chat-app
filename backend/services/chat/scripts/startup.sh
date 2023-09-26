#!/bin/bash


python manage.py migrate --pythonpath .
python manage.py search_index --create
gunicorn --env DJANGO_SETTINGS_MODULE=core.settings core.wsgi -b :8083
