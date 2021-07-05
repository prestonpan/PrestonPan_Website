#!/bin/sh
python3 libsatg.py
rsync -vrP --delete-after $HOME/programming/PrestonPan_Website/src/build/ root@prestonpan.tech:/var/www/prestonpan
