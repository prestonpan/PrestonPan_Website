#!/bin/sh
python3 libsatg.py
rsync -vrP --delete-after /home/preston/programming/prestonpan/src/build/ root@prestonpan.tech:/var/www/prestonpan
