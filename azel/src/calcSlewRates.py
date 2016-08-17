#!/usr/bin/python
##############################################################################
#                                                                            #
# Antennaslew calculates the antenna speed and offset, and prints the        #
# results to lsq_result.dat.                                                 #
#                                                                            #
# If the --graph option is present it will also plot the results and save    #
# as .png files                                                              #
#                                                                            #
# Author: Interns 2016 (Lina Olandersson, Simon Strandberg, Erik Thorsell)   #
# Date: 2016-08-04                                                           #
#                                                                            #
##############################################################################
import leastsq
import getStationName as gsn
import csv
import os
import sys
import numpy

path_to_dat = './data/'
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
            station = gsn.getStationName(station)
            orientation = file[3:5]

            with open(path_to_dat + file) as csvfile:
                readCSV = csv.reader(csvfile,delimiter=',')
                realTimes = []
                distance = []
                modelTimes = []
                stationname = []
                source = []
                timestamp = []
                for row in readCSV:
                    modelTimes.append(float(row[0]))
                    realTimes.append(float(row[1]))
                    distance.append(float(row[2]))
                    stationname.append(str(row[3]))

                    ## Convert hundreds back to the date used in Sked.
                    time = float(row[4])
                    days = int(time / 86400)
                    time = time % 86400
                    hours = int(time / 3600)
                    time = time % 3600
                    minutes = int(time / 60)
                    time = time % 60
                    seconds = int(time)
                    time = time-seconds
                    hundreds = int(time*100)

                    timestamp.append("yy" + str(days).zfill(3) + "-" + str(hours).zfill(2) + str(minutes).zfill(2) + str(seconds).zfill(2))

                    source.append(str(row[5]))

                if len(realTimes) != 0:

                    solution = leastsq.speed_offset(distance, realTimes, stationname, timestamp, source)

                    # Calculate current model
                    x = numpy.array(distance)
                    y = numpy.array(modelTimes)
                    A = numpy.vstack([x, numpy.ones(len(x))]).T
                    curspeed, curoffset = numpy.linalg.lstsq(A, y)[0]
                    curspeed = 1/curspeed * 60

                    lines.append('Station: %s, Orientation: %s' % \
                    (station.upper(), orientation.upper())+ '\n'+ \
                    'Station: %s, calculated model: \t offset = %.1f s, speed = %.0f deg/min' % \
                    (station.upper(), solution[1], solution[0])+ '\n' +\
                    'Station: %s, current model: \t offset = %.1f s, speed = %.0f deg/min.' \
                    % (station.upper(), curoffset, curspeed) + '\n\n')

                    if graph == True and solution[0] != 0 and solution[1] != 0:
                        leastsq.plot_curve(solution, modelTimes, station, orientation)
                else:
                    lines.append( "No trakl or flagr for station: " + station.upper() + \
                    ',' + orientation.upper() + "\n\n")

lines.sort()

res = open('./data/lsq_result.dat', 'w')
for i in range(0,len(lines)):
    res.write(lines[i])
res.close()
