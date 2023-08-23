#!/bin/sh

set -e
set -x

host="$1"
shift
# cmd="$@"

until PGPASSWORD=$DB_PASSWORD psql -h "$host" -U $DB_USER -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  echo $DB_USER
  echo $DB_PASSWORD
  sleep 1
done

>&2 echo "Postgres is up - moving ahead"
#exec $cmd