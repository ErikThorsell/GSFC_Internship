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
# Import module
import leastsq
import csv
import os

path_to_dat = '../data/'
res = open('lsq_result.dat', 'w')
lines=[]
for subdir, dirs, files in os.walk(path_to_dat):
    for file in files:
        if file[-4:] == ".dat":
            station = file[0:2]
            orientation = file[3:5]

            with open(path_to_dat + file) as csvfile:
                readCSV = csv.reader(csvfile,delimiter=',')
                times = []
                distance = []
                pret = []
                for row in readCSV:
                    pret.append(float(row[0]))
                    times.append(float(row[1]))
                    distance.append(float(row[2]))
                if len(times) != 0:

                    t = leastsq.start_time(distance, times)
                    v = leastsq.speed(distance, times)

                    lines.append('Station: %s, Orientation: %s' % \
                    (station.upper(), orientation.upper())+ '\n'+ \
                    'Station: %s, offset = %.1f, speed = %.0f deg/s' % \
                    (station.upper(), t, v) + '\n\n')

                    leastsq.plot_curve(distance, times, pret, station, orientation)
                else:
                    lines.append( "No trakl for station: " + station.upper() + \
                    "\n\n")

lines.sort()

for i in range(0,len(lines)):
    res.write(lines[i])
res.close()
