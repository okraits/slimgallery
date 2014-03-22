#!/bin/bash

PROJDIR="/home/sc-pfettrach/galerie"
PIDFILE="$PROJDIR/galerie.pid"
SOCKET="$PROJDIR/galerie.sock"

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
  ./manage.py runfcgi method=threaded host=127.0.0.1 port=3033
