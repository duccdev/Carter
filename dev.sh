#!/usr/bin/bash

source .venv/bin/activate

while true; do
    while read j; do
        killall python3 > /dev/null 2>&1
        CRANBERRY_ENV=dev .venv/bin/python3 main.py &
        sleep 1
    done < <(inotifywait -q -e modify -e delete -e create --exclude db.json *)
done
