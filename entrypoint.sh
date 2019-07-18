#!/bin/bash

python manage.py makemigrations

python manage.py migrate

#./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('rabbit', 'rabbit@hagstofa.is', 'rabbit')"
