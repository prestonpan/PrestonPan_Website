#!/bin/sh
if [ "$1" = "update" ]; then
    python3 satg.py
    rsync -vrP --delete-after ./build/ root@prestonpan.tech:/var/www/prestonpan
elif [ "$1" = "build" ]; then
    python3 satg.py
elif [ "$1" = "clean" ]; then
    rm -rf build/
elif [ "$1" = "view" ]; then
    python3 satg.py
    abrowser build/index.html
else
    python3 satg.py
    rsync -vrP --delete-after ./build/ root@prestonpan.tech:/var/www/prestonpan
fi
