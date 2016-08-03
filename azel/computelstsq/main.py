#!/usr/bin/python

# Import module
import leastsq
import csv
import os

path_to_dat = '../script/'

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

                    ans = leastsq.least_sq(distance, times)
                    print station, orientation, ans

                    t = leastsq.start_time(distance, times)
                    print 'Start time is: %.5f s for station %s in %s'%(t,station, orientation)

                    v = leastsq.speed(distance, times)
                    print 'Speed of %s in %s is: %.5f deg/min'%(station,orientation, v), "\n"

                    leastsq.plot_curve(distance, times, pret, station, orientation)
                else:
                    print "No trakl for station:", station, "\n"
#leastsq.plot_curve(distance, times, station, orientation)
