#!/usr/bin/env bash

echo $TEST
./wait-for-it.sh redis:6379 -- echo "Redis is up"
export FLASK_APP=wordz.py
flask init_words
exec gunicorn --workers 3 -w 2 -b :8000 wordz:app "$@"