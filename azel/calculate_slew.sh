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

SRC=./src/
SRC1=./src/extract.py
SRC2=./src/calcSlewRates.py
SRC3=./src/getStationSpecs.py
SRC4=./src/create_extract.py
SRCANTENNA=/shared/gemini/ftp/pub/sked/catalogs/antenna.cat
SRCANTENNA=./src/antenna.cat

OUTPUTDIR=""
DATADIR=""
IMGDIR=""
SESSIONPATH=""
OPT=""
GRAPH=""

###############################################################################
### Pre program 

if [ $# -gt 0 ]; then
    echo "## ERROR ##"
    echo "Invalid usage. The program will prompt you for the information required."
    echo "Please do not enter any options!"
    exit
fi

echo "Running calculate_slew.sh"
echo "For instructions on how to run the program, please see the README.md"
echo " "
echo "Please provide the path(s) to the sessions you wish to analyze:"
echo "You can specify arbitrarily many sessions, wildcards are allowed."
read SESSIONPATH
path_array=($SESSIONPATH)

echo " "

echo "Please provide the path to where you want the output to be stored."
echo "# WARNING #"
echo "The directory specified will be purged!"
read OUTPUTDIR
DATADIR=$OUTPUTDIR/data/
IMGDIR=$OUTPUTDIR/img/

if [ ! -d $OUTPUTDIR ]; then
    echo "Could not find the specified output path."
    echo "Do you wish to create" $OUTPUTDIR"? [y/n]"
    read ans
    if [ $ans != 'y' ]; then
        echo "You did not answer 'y'."
        echo "Exiting program."
        exit
    fi
    echo "Creating: $OUTPUTDIR."
    mkdir $OUTPUTDIR
    mkdir $DATADIR
    mkdir $IMGDIR
else
    echo $OUTPUTDIR "already exists. Do you wish to purge (rm -rf $OUTPUTDIR)? [y/n]"
    read ans
    if [ $ans != 'y' ]; then
        echo "You did not answer 'y'."
        echo "Exiting program."
        exit
    fi
    rm -rf $OUTPUTDIR/*
    mkdir $DATADIR
    mkdir $IMGDIR
fi

echo " "
echo "Do you want to plot graphs? [y/n]"
read graph

if [ "$graph" == 'y' ]; then
    OPT="--graph"
fi

echo "The graphs will be stored in" $IMGDIR


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
