#!/bin/bash 

/usr/sbin/postfix start
gunicorn --config gunicorn.py devopsweb:app
