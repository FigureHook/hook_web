#!/bin/bash

if ! python _cmd.py checkdb; then
    echo "Can't get connection with database."
    exit 1
fi

if [ -n $WORKERS ]; then
    WORKERS=2
fi

if [ -n $PORT ]; then
    PORT=8000
fi

gunicorn -w ${WORKERS} -b 0.0.0.0:${PORT} hook_web.wsgi:app
