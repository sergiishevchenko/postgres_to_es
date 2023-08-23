#!/usr/bin/env bash

./wait-postgres.sh db

python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --strict --ini uwsgi.ini