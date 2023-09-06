#!/usr/bin/env bash

#gunicorn wsgi:app --bind 0.0.0.0:8080 --log-level=debug --workers=4

gunicorn wsgi:app --bind 0.0.0.0:8080 --log-level=debug --workers=4 --error-logfile gunicorn.error.log --access-logfile gunicorn.log --capture-output