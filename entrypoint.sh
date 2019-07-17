#!/bin/bash

python manage.py migrate

./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('notandi', 'notandi@hagstofa.is', 'notandi')"
