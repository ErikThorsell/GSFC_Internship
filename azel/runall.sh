#!/bin/bash

LOGDIR=./logs/
SKDDIR=./skds/
DATADIR=./data/
SRC=./script/extraxct.py

rm $DATADIR*

for f in $SKDDIR*; do
    SKDFILE=$(echo $f | cut -d'/' -f 3)
    tSKDFILE=$(echo $SKDFILE | cut -d'.' -f 1)
    for l in $LOGDIR*; do
        tLOG=$(echo $l | cut -d'/' -f 3)
        if [ $tLOG == $tSKDFILE ]; then
            LOGFILES=$l
            SKDFILE=$SKDDIR$SKDFILE
            python2 $SRC $LOGFILES $SKDFILE
        fi
    done
done
