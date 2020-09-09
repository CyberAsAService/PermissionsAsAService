#!/usr/bin/env bash

case "$1" in
  webserver)
    # Run webserver
    python3 PaaS.py
    ;;
  worker)
    python3 -m celery -A PaaS.celery worker -l info
    ;;
  flower)
    python3 -m flower -A PaaS.celery
    ;;
  *)
    echo 'MISSING PARAMETER webserver | worker | flower';
    exit 1;
esac
