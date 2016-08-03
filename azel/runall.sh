#!/bin/bash

LOGDIR=./logs/
SKDDIR=./skds/
DATADIR=./data/
SRC=./script/extraxct.py

rm $DATADIR*

for f in $SKDDIR*; do
    SKDFILE=$f
    SKDFILE=$(echo $SKDFILE | cut -d'/' -f 3)
    tSKDFILE=$(echo $SKDFILE | cut -d'.' -f 1)
    for l in $LOGDIR*; do
        tLOG=$(echo $l | cut -d'/' -f 3)
        if [ $tLOG == $tSKDFILE ]; then
            LOGFILE=$l
            SKDFILE=$SKDDIR$SKDFILE
            python2 $SRC $LOGFILE $SKDFILE
        fi
    done
done
