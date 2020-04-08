#! /bin/bash

python manage.py migrate

gunicorn --bind 0.0.0.0 verd_andi.wsgi
