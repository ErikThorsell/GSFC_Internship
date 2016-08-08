#!/bin/bash

LOGDIR=./logs/
SKDDIR=./skds/
DATADIR=./data/
SRC1=./script/extraxct.py
SRC2=./script/antennaslew.py
IMGDIR=./img/
OPT=""

rm $DATADIR*
rm $IMGDIR*

for f in $SKDDIR*; do
    SKDFILE=$(echo $f | cut -d'/' -f 3)
    tSKDFILE=$(echo $SKDFILE | cut -d'.' -f 1)
    for l in $LOGDIR*; do
        tLOG=$(echo $l | cut -d'/' -f 3)
        if [ $tLOG == $tSKDFILE ]; then
            LOGFILES=$l
            SKDFILE=$SKDDIR$SKDFILE
            python2 $SRC1 $LOGFILES $SKDFILE
        fi
    done
done

if [ $# -gt 0 ]; then
    OPT="$1"
fi

python2 $SRC2 $OPT
