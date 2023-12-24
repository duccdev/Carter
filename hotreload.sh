#!/usr/bin/bash

while true; do
    while read j; do
        echo -e "\e[31mHot Reloading...\e[0m"
        killall python3 > /dev/null 2>&1
        .venv/bin/python3 main.py &
    done < <(inotifywait -q -e modify -e delete -e create --exclude hotreload.sh *)
done
