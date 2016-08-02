#!/usr/bin/python

# Import module
import leastsq
import csv

# Data points
#ydata = [0.1,1.2,1.8,4,5,6,7,8,9]
#xdata = [0,1,2,4,5,6,7,8,9]

# Get data from files

with open('../script/ft_az.dat') as csvfile:
    readCSV = csv.reader(csvfile,delimiter=',')
    times = []
    distance = []
    pret = []
    for row in readCSV:
        pret.append(float(row[0]))
        times.append(float(row[1]))
        distance.append(float(row[2]))


# Calculate least square
ans = leastsq.least_sq(distance, times)
print ans

# Plot graph of the result and the original data
leastsq.plot_curve(distance, times)

# Compute the time it takes to get up to max speed
t = leastsq.start_time(xdata, ydata)
print 'Start time is: %.5f s'% (t)

# Compute the speed of the antenna
v = leastsq.speed(xdata, ydata)
print 'Speed of the antenna: %.5f deg/s'% (v)
