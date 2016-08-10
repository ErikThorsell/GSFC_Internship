#!/usr/bin/python
#############################################################
#                                                           #
# This module computes least square solutions for antenna   #
# slew rate data.                                           #
#                                                           #
# plot_curve() plots the solution and its original data     #
# speed_offet() returns the speed and offset  of the antenna#
#                                                           #
# Author: Lina Olandersson, Simon Strandberg                #
# Date: 2016-08-10                                          #
#                                                           #
#############################################################

try:
    import matplotlib.pyplot as plt
except ImportError:
    pass
import numpy
import math


def plot_curve(xdata, ydata, pret, stat, ori):
    t = numpy.array(pret)
    ysorted=[]
    xsorted=[]
    ytmp=[]
    xtmp=[]
    k_old = 0.0

    ymax = max(ydata)
    threshold = ymax/20

    # First least square line
    x = numpy.array(xdata)
    y = numpy.array(ydata)
    # Stack arrays vertically, .T transposes the matrix
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    # Return the least square solution to a linear matrix equation
    try:
        k,m = numpy.linalg.lstsq(A, y)[0]
    except:
        return
    m_max = m + threshold
    m_min = m - threshold

    # Itterate to get a better solution
    while not (abs(k - k_old) < math.pow(10,-10)):
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
            return

        xtmp = xsorted
        ytmp = ysorted
        m_max = m_new + threshold
        m_min = m_new - threshold
        k_old = k
        k = k_new
        xsorted = []
        ysorted = []

    # Calculate the offset
    m_top = 0.0
    for i in range(0,len(xtmp)):
        temp = float(ytmp[i]) - k * float(xtmp[i])
        if temp > m_top:
            m_top = temp

    # Plot graphs and save as .png
    plt.plot(x, y, 'ro', label='Discarded points', markersize=1)
    plt.plot(x_new, y_new, 'bo', label='Real time, sorted', markersize=1)
    plt.plot(x, t, 'c-', label='Current model', markersize=1)
    plt.plot(x, k_new*x + m_top, 'k', label='Calculated model')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Distance [Degree]')
    plt.ylabel('Time [s]')
    plt.suptitle('Antenna: %s, orientation:  %s' % (stat.upper(),ori.upper())+\
    "\n"+ 'Speed: %.0f deg/min, offset: %.1f s'%(1/k_new*60,m_top))
    plt.savefig('./img/%s_%s.png' % (stat, ori))
    plt.close()

    return


def speed_offset(xdata, ydata):
    ysorted=[]
    xsorted=[]
    ytmp=[]
    xtmp=[]
    ans = (0,0)
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
#        k_new,m_new = numpy.linalg.lstsq(A, y_new)[0]
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
    ans = (speed, offset)

    return ans

