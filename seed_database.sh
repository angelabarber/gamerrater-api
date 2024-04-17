#!/bin/bash

rm db.sqlite3
rm -rf ./raterapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations raterapi
python3 manage.py migrate raterapi
python3 manage.py loaddata user
python3 manage.py loaddata token
# python3 manage.py loaddata category

