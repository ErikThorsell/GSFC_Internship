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

SRC1=./src/extract.py
SRC2=./src/calcSlewRates.py
SRC3=getStationSpecs.py
SRC4=create_extract.py
SRCANTENNA=/shared/gemini/ftp/pub/sked/catalogs/antenna.cat
OUTPUTDIR=""
DATADIR=""
IMGDIR=""
SESSIONPATH=""
OPT=""
GRAPH=""
var=""

if [ $# -gt 0 ]; then
    echo "# ERROR #"
    echo "Invalid usage. The program will prompt you for the information
          required."
    exit
fi

echo "Running calculate_slew.sh"
echo "Please provide the path(s) to the sessions you wish to analyze:"
IFS=' ' read -ra SESSIONPATH

echo "Please provide the path to where you want the output to be stored:"
read OUTPUTDIR
DATADIR=$OUTPUTDIR/data/
IMGDIR=$OUTPUTDIR/img/

echo $DATADIR
echo $IMGDIR

for SESSIONDIR in "${SESSIONPATH[@]}"; do
    echo $SESSIONDIR
done

#if [ ! -d $SKDDIR ]; then
#    echo "Unable to locate" $SKDDIR "please read the README.md for more info on how to use the program."
#    exit
#fi
#echo "Running program" $SRC1
#echo " "
#for f in $SKDDIR*; do
#    SKDFILE=$(echo $f | cut -d'/' -f 3)
#    tSKDFILE=$(echo $SKDFILE | cut -d'.' -f 1)
#    if [ ! -d $LOGDIR ]; then
#        echo "Unable to locate" $LOGDIR "please read the README.md for more info on how to use the program."
#        exit
#    fi
#    echo "Working on session" $tSKDFILE
#    for l in $LOGDIR*; do
#        tLOG=$(echo $l | cut -d'/' -f 3)
#        if [ $tLOG == $tSKDFILE ]; then
#            LOGFILES=$l
#            SKDFILE=$SKDDIR$SKDFILE
#            python2 $SRC1 $LOGFILES $SKDFILE
#        fi
#    done
#done
#
#if [ $# -gt 0 ]; then
#    OPT="$1"
#fi
#
#echo " "
#echo "Running program" $SRC2 $OPT
#echo " "
#python2 $SRC2 $OPT
#
#echo "Execution completed."
#echo " "
#echo "The data is stored in" $DATADIR "and any plots are stored in" $IMGDIR
#
