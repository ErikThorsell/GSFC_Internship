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

ROOTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

SRC=$ROOTDIR/src/
SRC1=$ROOTDIR/src/extract.py
SRC2=$ROOTDIR/src/calcSlewRates.py
SRC3=$ROOTDIR/src/getStationSpecs.py
SRC4=$ROOTDIR/src/create_extract.py
SRCANTENNA=/shared/gemini/ftp/pub/sked/catalogs/antenna.cat
SRCANTENNA=$ROOTDIR/src/antenna.cat

OUTPUTDIR="/tmp/output"
DATADIR=""
IMGDIR=""
SESSIONPATH=""
OPT=""
GRAPH=""

###############################################################################
### Pre program 

if [ ! $# -gt 0 ]; then
    echo "## ERROR ##"
    echo "Invalid usage."
    exit
fi

while [ $# -gt 1 ]; do
    key="$1"
    case $key in
        -o|--output)
        OUTPUTDIR="$2"
        shift
        ;;
        -g|--graph)
        OPT="--graph"
        shift
        ;;
        -i|--input)
        shift
        SESSIONPATH=$@
        ;;
        *)
            # 
    esac
    shift
done

path_array=($SESSIONPATH)
DATADIR=$OUTPUTDIR/data/
IMGDIR=$OUTPUTDIR/img/

if [ ! -d $OUTPUTDIR ]; then
    echo "Creating: $OUTPUTDIR."
    mkdir $OUTPUTDIR
    mkdir $DATADIR
    mkdir $IMGDIR
else
    rm -rf $OUTPUTDIR/*
    mkdir $DATADIR
    mkdir $IMGDIR
fi

######################## Starting execution of program ########################

echo "Generating new main program."
if [ ! -f $SRCANTENNA ]; then
    echo "The file" $SRCANTENNA "is not present. Make sure the path for SRCANTENNA is correctly set."
    exit
fi

python2 $SRC3 $SRCANTENNA $SRC"/station_specs.py" $SRC"/station_names.dat"
python2 $SRC4 $SRCANTENNA $SRC1

echo "Generated" $SRC1
echo " "

for DIR in "${path_array[@]}"; do
    if [ ! -d $DIR ]; then
        echo "Unable to locate" $DIR"."
        echo "Please ensure that you have specified a valid path."
        exit
    fi
    echo " "
    echo "Processing session" $DIR
    python2 $SRC1 $OUTPUTDIR $DIR
done

echo " "
echo "Running program" $SRC2 $OPT
echo " "
python2 $SRC2 $OUTPUTDIR $OPT

echo "Execution completed."
echo " "
echo "The data is stored in" $DATADIR "and any plots are stored in" $IMGDIR
#
