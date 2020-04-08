#!/bin/bash

python manage.py migrate

python manage.py shell -c "from django.contrib.auth.models import User; print('admin user exists') if User.objects.filter(username='admin').count() else User.objects.create_superuser('admin', 'verdandi@hagstofa.is', 'admin')"

python manage.py runserver 0.0.0.0:8000 
