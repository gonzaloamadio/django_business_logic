#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh && workon djangoenv;

echo "Running Django: " ;
python manage.py --version;
nohup python manage.py runserver 0.0.0.0:8010 &

echo "";echo""
echo "Running on background."
echo "";echo""

echo "";echo""
echo "we show tail -f of nohup, with Ctrl+C you will cut but server will till be running"
echo "";echo""
tail -f nohup.out

