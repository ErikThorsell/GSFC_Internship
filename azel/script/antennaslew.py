#!/usr/bin/python
##############################################################################
#                                                                            #
# Antennaslew produces plots of the antenna speed and offset, and also       #
# prints the results to lsq_result.dat.                                      #
#                                                                            #
# Author: Interns 2016 (Lina Olandersson, Simon Strandberg, Erik Thorsell)   #
# Date: 2016-08-04                                                           #
#                                                                            #
##############################################################################
import leastsq
import csv
import os
import sys
import numpy

path_to_dat = './data/'
res = open('./data/lsq_result.dat', 'w')
lines=[]
graph = False

if len(sys.argv) > 1:
    if sys.argv[1] == "--graph":
        graph = True
    else:
        graph = False
        print "Invalid usage!"
        print "Only valid flag is --graph"
        sys.exit()

for subdir, dirs, files in os.walk(path_to_dat):
    for file in files:
        if file[-4:] == ".dat":
            station = file[0:2]
            orientation = file[3:5]

            with open(path_to_dat + file) as csvfile:
                readCSV = csv.reader(csvfile,delimiter=',')
                realtimes = []
                distance = []
                modeltimes = []
                for row in readCSV:
                    modeltimes.append(float(row[0]))
                    realtimes.append(float(row[1]))
                    distance.append(float(row[2]))
                if len(realtimes) != 0:

                    t = leastsq.speed_offset(distance, realtimes)

                    # Calculate current model
                    x = numpy.array(distance)
                    y = numpy.array(modeltimes)
                    A = numpy.vstack([x, numpy.ones(len(x))]).T
                    curspeed, curoffset = numpy.linalg.lstsq(A, y)[0]
                    curspeed = 1/curspeed * 60

                    lines.append('Station: %s, Orientation: %s' % \
                    (station.upper(), orientation.upper())+ '\n'+ \
                    'Station: %s, calculated model: \t offset = %.1f s, speed = %.0f deg/min' % \
                    (station.upper(), t[1], t[0])+ '\n' +\
                    'Station: %s, current model: \t offset = %.1f s, speed = %.0f deg/min.' \
                    % (station.upper(), curoffset, curspeed) + '\n\n')

                    if graph == True:
                        leastsq.plot_curve(distance, realtimes, modeltimes, station, orientation)
                else:
                    lines.append( "No trakl or flagr for station: " + station.upper() + \
                    ',' + orientation.upper() + "\n\n")

lines.sort()

for i in range(0,len(lines)):
    res.write(lines[i])
res.close()
