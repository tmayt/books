#!/bin/bash

echo "****** Apply database migrations ******"
python manage.py makemigrations 
python manage.py migrate --noinput
python manage.py graph_models -a -o ERD.png


echo "****** Collecting static files ******"
python manage.py collectstatic --noinput


echo "****** Load fixrures ******"
python manage.py loaddata fixtures/users.json
python manage.py loaddata fixtures/books.json


echo "****** Run django testcases ******"
python manage.py test

# Run server 
uwsgi --ini ./uwsgi.ini 
