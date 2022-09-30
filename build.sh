#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

rm -rf ./aulas/migrations/*00
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate

echo "from aulas.models import Usuario; usuario = Usuario.objects.filter(username='admin'); None if usuario else Usuario.objects.create_superuser('admin', 'admin', 'admin')" | python manage.py shell
