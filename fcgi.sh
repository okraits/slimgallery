#!/bin/bash

PROJDIR="/home/sc-pfettrach/slimgallery"
PIDFILE="$PROJDIR/slimgallery.pid"
SOCKET="$PROJDIR/slimgallery.sock"

cd $PROJDIR
if [ -f $PIDFILE ]; then
    kill `cat -- $PIDFILE`
    rm -f -- $PIDFILE
fi

#exec /usr/bin/env - \
#  PYTHONPATH="../python:.." \
#  ./manage.py runfcgi socket=$SOCKET pidfile=$PIDFILE
exec /usr/bin/env - \
  PYTHONPATH="../python:.." \
  ./manage.py runfcgi method=threaded host=127.0.0.1 port=3034
