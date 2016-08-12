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


def plot_curve(data_tuple, modelTimes, station, orientation):
    
    # data_tuple = (speed, offset, x, y, x_new, y_new, k_new)
    speed = data_tuple[0]
    m_top = data_tuple[1]
    x = data_tuple[2]
    y = data_tuple[3]
    x_new = data_tuple[4]
    y_new = data_tuple[5]
    k_new = data_tuple[6]

    if orientation == 'az':
        orientation = 'AZIMUT'
    if orientation == 'el':
        orientation = 'ELEVATION'

    # Plot graphs and save as .png
    plt.plot(x, y, 'ro', label='Discarded points', markersize=1)
    plt.plot(x_new, y_new, 'bo', label='Real time, sorted', markersize=1)
    plt.plot(x, modelTimes, 'c-', label='Current model', markersize=1)
    plt.plot(x, k_new*x + m_top, 'k', label='Calculated model')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Distance [Degree]')
    plt.ylabel('Time [s]')
    plt.suptitle('%s, %s' % (station.upper(),orientation.upper()) +\
                "\n"+ 'Speed: %.0f deg/min, offset: %.1f s'%(1/k_new*60,m_top))
    plt.savefig('./img/%s_%s.png' % (station, orientation))
    plt.close()
    return



def speed_offset(xdata, ydata):
    ysorted=[]
    xsorted=[]
    ytmp=[]
    xtmp=[]
    ans = (0,0,0,0,0,0,0)
    k_old = 0.0

    ymax = max(ydata)
    threshold = ymax/20

    # First line
    x = numpy.array(xdata)
    y = numpy.array(ydata)
    # Stack arrays vertically, .T transposes the matrix
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    # Return the least square solution to a linear matrix equation
    try:
        k,m = numpy.linalg.lstsq(A, y)[0]
    except:
        return
    # Only use point between those boundaries
    m_max = m + threshold
    m_min = m - threshold

    # Itterate to get a better solution
    while not (abs(k - k_old) < math.pow(10, -10)):
        for i in range(0,len(xdata)):
            if ydata[i] < k*xdata[i] + m_max:
                if ydata[i] > k*xdata[i] + m_min:
                   ysorted.append(ydata[i])
                   xsorted.append(xdata[i])

        x_new = numpy.array(xsorted)
        y_new = numpy.array(ysorted)

        A = numpy.vstack([x_new, numpy.ones(len(x_new))]).T
        try:
            k_new,m_new = numpy.linalg.lstsq(A, y_new)[0]
        except:
            return ans

        xtmp = xsorted
        ytmp = ysorted
        m_max = m_new + threshold
        m_min = m_new - threshold
        k_old = k
        k = k_new
        xsorted = []
        ysorted = []

    # Calculate the offset
    offset = 0.0
    for i in range(0,len(xtmp)):
        temp = float(ytmp[i]) - k * float(xtmp[i])
        if temp > offset:
            offset = temp

    speed = 1/k_new*60
    ans = (speed, offset, x, y, x_new, y_new, k_new)
#    print "X: " + str(x)
#    print "Y: " + str(y)
#    print "X_new: " + str(x_new)
#    print "y_new: " + str(y_new)
    return ans

