#!/usr/bin/python
#############################################################
#                                                           #
# This module computes least square solutions for antenna   #
# slew rate data.                                           #
#                                                           #
# plot_curve() plots the solution and its original data     #
# speed_offet() returns the speed and offset  of the antenna#
#                                                           #
# Author: Lina Olandersson, Simon Strandberg, Erik Thorsell #
# Date: 2016-08-10                                          #
#                                                           #
#############################################################

try:
    import matplotlib.pyplot as plt
except ImportError:
    pass
import numpy
import math


def plot_curve(data_tuple, modelTimes_original, station, orientation, path):
    # data_tuple = (speed, offset, x, y, x_new, y_new, k_new)
    speed = data_tuple[0]
    offset = data_tuple[1]
    x_original = data_tuple[2]
    y_original = data_tuple[3]
    x_new = data_tuple[4]
    y_new = data_tuple[5]
    k_new = data_tuple[6]
    x_tmp = []
    y_tmp = []
    modelTimes_tmp = []

    y_mean = numpy.mean(y_original)
    for i in range(0, len(y_original)):
        if y_original[i] < 3*y_mean:
            y_tmp.append(y_original[i])
            x_tmp.append(x_original[i])
            modelTimes_tmp.append(modelTimes_original[i])
    
    x = numpy.array(x_tmp)
    y = numpy.array(y_tmp)
    modelTimes = numpy.array(modelTimes_tmp)

    if orientation == 'az':
        orientation = 'AZIMUTH'
    if orientation == 'el':
        orientation = 'ELEVATION'
    
    # Plot graphs and save as .png
    plt.plot(x, y, 'r.', label='Discarded points', markersize=2)
    plt.plot(x_new, y_new, 'b.', label='Real time, sorted', markersize=2)
    plt.plot(x, modelTimes, 'c-', label='Current model', markersize=1)
    plt.plot(x, k_new*x + offset, 'k-', label='Calculated model')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Distance [Degree]')
    plt.ylabel('Time [s]')
    plt.suptitle('%s, %s' % (station.upper(),orientation.upper()) +\
               "\n"+ 'Speed: %.0f deg/min, offset: %.1f s'%(1/k_new*60,offset))
    plt.savefig(path + "/img/%s_%s.png" % (station, orientation))
    plt.close()
    return



def speed_offset(xdata, ydata, station, time, source, path):
    ysorted=[]
    xsorted=[]
    ydisc=[]
    xdisc=[]
    ans = (0,0,0,0,0,0,0)
    k_old = 0.0
    threshold = numpy.mean(ydata)/10
    discfile = open(path + "/data/lsq_disc.dat", 'a')
    discfile.write("# Station" + "," + "Date" + "," + "Source" + "," + "dAz" + "," + "dEl" + '\n')

    # First line
    x_original = numpy.array(xdata)
    y_original = numpy.array(ydata)

    # Stack arrays vertically, .T transposes the matrix
    A = numpy.vstack([x_original, numpy.ones(len(x_original))]).T
    # Return the least square solution to a linear matrix equation
    try:
        k,m = numpy.linalg.lstsq(A, y_original)[0]
    except:
        return

    # Itterate to get a better solution
    while not (abs(k - k_old) < math.pow(10, -10)):
        for i in range(0,len(xdata)):
            y_tmp = k * xdata[i] + m
            if y_tmp - threshold < ydata[i] < y_tmp + threshold:
                ysorted.append(ydata[i])
                xsorted.append(xdata[i])
            else:
                discfile.write(station[i] + "," + time[i] + "," + source[i] + "," + str(xdata[i]) + "," + str(ydata[i]) + '\n')

        x_new = numpy.array(xsorted)
        y_new = numpy.array(ysorted)

        A = numpy.vstack([x_new, numpy.ones(len(x_new))]).T
        try:
            k_new, m = numpy.linalg.lstsq(A, y_new)[0]
        except:
            return ans

        k_old = k
        k = k_new
        xsorted = []
        ysorted = []

    discfile.close()

    # Calculate the offset
    offset = 0.0
    for i in range(0,len(x_new)):
        temp = float(y_new[i]) - k * float(x_new[i])
        if temp > offset:
            offset = temp

    speed = 1/k_new*60
    ans = (speed, offset, x_original, y_original, x_new, y_new, k_new)
    return ans

