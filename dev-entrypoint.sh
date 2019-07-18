#!/bin/bash

cd src/verd_andi

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 0.0.0.0:8000 
#./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('rabbit', 'rabbit@hagstofa.is', 'rabbit')"
