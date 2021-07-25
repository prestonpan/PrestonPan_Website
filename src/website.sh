#!/bin/sh
if [ "$1" = "update" ]; then
    python3 libsatg.py
    rsync -vrP --delete-after $HOME/programming/PrestonPan_Website/src/build/ root@prestonpan.tech:/var/www/prestonpan
elif [ "$1" = "build" ]; then
    python3 libsatg.py
elif [ "$1" = "clean" ]; then
    rm -rf build/
elif [ "$1" = "view" ]; then
    python3 libsatg.py
    abrowser build/index.html
else
    echo "test"
fi
