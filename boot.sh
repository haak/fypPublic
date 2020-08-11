#!/bin/sh
# shellcheck disable=SC2039
source venv/bin/activate
flask db upgrade
flask translate compile
exec gunicorn -b :5000 --access-logfile - --error-logfile - recommender:app