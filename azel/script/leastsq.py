#!/usr/bin/python
#############################################################
#                                                           #
# This module computes least square solutions for antenna   #
# slew rate data.                                           #
#                                                           #
# plot_curve() plots the solution and its original data     #
# speed() returns the velocity of the antenna in rad/s      #
# start_time() returns the startup time fori the antenna    #
#                                                           #
# Author: Lina Olandersson                                  #
# Date: 2016-07-29                                          #
#                                                           #
#############################################################

try:
    import matplotlib.pyplot as plt
except ImportError:
    pass
import numpy


def plot_curve(xdata, ydata, pret, stat, ori):
    x = numpy.array(xdata)
    y = numpy.array(ydata)
    t = numpy.array(pret)

    # Stack arrays vertically, .T transposes the matrix
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    # Return the least square solution to a linear matrix equation
    k,m = numpy.linalg.lstsq(A, y)[0]

    plt.plot(x, y, 'bo', label='Real time', markersize=1)
    plt.plot(x, t, 'ro', label='Theoretical time', markersize=1)
    plt.plot(x, k*x + m, 'k', label='Least sq fit')
    plt.legend()
    plt.grid(True)
    plt.xlabel('Distance [Degree]')
    plt.ylabel('Time [s]')
    plt.suptitle('Antenna: %s, orientation:  %s' % (stat.upper(),ori.upper())+\
    "\n"+ 'Speed: %.0f deg/min, offset: %.1f s'%(1/k*60,m))
    plt.savefig('../img/%s_%s.png' % (stat, ori))
    plt.close()
    return

def speed(xdata, ydata):
    x = numpy.array(xdata)
    y = numpy.array(ydata)

    A = numpy.vstack([x, numpy.ones(len(x))]).T
    k,m = numpy.linalg.lstsq(A, y)[0]
    k = 1/k*60
    return k

def start_time(xdata, ydata):
    x = numpy.array(xdata)
    y = numpy.array(ydata)

    A = numpy.vstack([x, numpy.ones(len(x))]).T
    k,m = numpy.linalg.lstsq(A, y)[0]

    return m
