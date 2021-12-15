#!/bin/bash

arg1=$1

if [ "$arg1" == "" ]; then
    exit 1
fi


check_db() {
    if ! hookweb check db; then
        echo "Can't get connection with database."
    exit 1
    fi
}


check_redis() {
    if ! hookweb check db; then
        echo "Can't get connection with redis."
    exit 1
    fi
}


if [ -n $WORKERS ]; then
    WORKERS=2
fi

if [ -n $PORT ]; then
    PORT=8000
fi

if [ $arg1 == "start" ]; then
    check_db
    check_redis
    gunicorn -w ${WORKERS} -b 0.0.0.0:${PORT} hook_web.wsgi:app
fi

if [ $arg1 == "test" ]; then
    if  [ -d "./tests" ]; then
        pytest
    else
        echo "No tests found."
    fi
fi
