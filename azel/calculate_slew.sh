#!/bin/bash
###############################################################################
# This script acts as the main program for the antenna slewing time           #
# calculations. It first checks that the necessary programs and directories   #
# are present and creates them if necessary. The script then launches a       #
# sequence of programs that calculates the slewing time for the antennas      #
# specified in the included sessions.                                         #
#                                                                             #
# Args: --graph, enables the graph printing feature in calcSlewRates.py       #
#                                                                             #
# Author: Erik Thorsell, Summer Internship 2016                               #
###############################################################################

LOGDIR=./logs/
SKDDIR=./skds/
DATADIR=./data/
SRC1=./src/extract.py
SRC2=./src/calcSlewRates.py
SRC3=getStationSpecs.py
SRC4=create_extract.py
SRCANTENNA=./src/antenna.cat
IMGDIR=./img/
OPT=""
GRAPH=""

CLEANIMG=$(shopt -s nullglob dotglob; echo $IMGDIR*)
CLEANDATA=$(shopt -s nullglob dotglob; echo $DATADIR*)

echo "Starting execution of ./calculate_slew.sh"
echo " "

## House keeping!
echo "Running pre processing and house keeping!"
echo " "

# Checking that the program has been generated.
if [ ! -f $SRC1 ]; then
    echo $SRC1 "is not present. Trying to generate..."
    if [ ! -f $SRCANTENNA ]; then
        echo "The file" $SRCANTENNA "is not present. Please fetch your copy from gemini."
        exit
    fi
    cd src/
    python2 $SRC3
    python2 $SRC4
    cd ..
    echo "Generated" $SRC1
    echo " "
fi

# Check that img/ and data/ are present in the folder.
if [ ! -d $IMGDIR ]; then
    echo "Created folder $IMGDIR"
    mkdir $IMGDIR
fi

if [ ! -d $DATADIR ]; then
    echo "Created folder $DATADIR"
    mkdir $DATADIR
fi

# Empty img/ and data/ if they contain any data.
if [ ${#CLEANIMG} -gt 0 ]; then
    echo "Emptying directory:" $IMGDIR
    rm $IMGDIR*
fi

if [ ${#CLEANDATA} -gt 0 ]; then
    echo "Emptying directory:" $DATADIR
    rm $DATADIR*
fi
echo " "

echo "Finding each skd-file and its corresponding log files."
echo " "
if [ ! -d $SKDDIR ]; then
    echo "Unable to locate" $SKDDIR "please read the README.md for more info on how to use the program."
    exit
fi
echo "Running program" $SRC1
echo " "
for f in $SKDDIR*; do
    SKDFILE=$(echo $f | cut -d'/' -f 3)
    tSKDFILE=$(echo $SKDFILE | cut -d'.' -f 1)
    if [ ! -d $LOGDIR ]; then
        echo "Unable to locate" $LOGDIR "please read the README.md for more info on how to use the program."
        exit
    fi
    echo "Working on session" $tSKDFILE
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

echo " "
echo "Running program" $SRC2 $OPT
echo " "
python2 $SRC2 $OPT

echo "Execution completed."
echo " "
echo "The data is stored in" $DATADIR "and any plots are stored in" $IMGDIR

