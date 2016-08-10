#!/bin/bash

LOGDIR=./logs/
SKDDIR=./skds/
DATADIR=./data/
SRC1=./script/extract.py
SRC2=./script/antennaslew.py
IMGDIR=./img/
OPT=""
GRAPH=""

CLEANIMG=$(shopt -s nullglob dotglob; echo $IMGDIR*)
CLEANDATA=$(shopt -s nullglob dotglob; echo $DATADIR*)

echo "Starting."

if [ ${#CLEANIMG} -gt 0 ]; then
    echo "Emptying directory:" $IMGDIR
    rm $IMGDIR*
fi

if [ ${#CLEANDATA} -gt 0 ]; then
    echo "Emptying directory:" $DATADIR
    rm $DATADIR*
fi

echo "Finding each skd-file and its corresponding log files."
echo "Running program" $SRC1
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

echo "Running program" $SRC2 $OPT
python2 $SRC2 $OPT

echo "Execution completed."
echo "The data is stored in" $DATADIR "and any plots are stored in" $IMGDIR

