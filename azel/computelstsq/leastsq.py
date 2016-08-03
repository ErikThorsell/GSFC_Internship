#!/usr/bin/python
#############################################################
#                                                           #
# This module computes least square solutions               #
#                                                           #
# least_sq() computes a least square solution               #
# plot_curve() plots the solution and its original data     #
# speed() returns the velocity of the antenna in rad/s      #
# start_time() returns the startup time fori the antenna    #
#                                                           #
# Author: Lina Olandersson                                  #
# Date: 2016-07-29                                          #
#                                                           #
#############################################################

import matplotlib.pyplot as plt
import numpy

def least_sq(xdata, ydata):
    x = numpy.array(xdata)
    y = numpy.array(ydata)

    # Stack arrays vertically, .T transposes the matrix
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    # Return the least square solution to a linear matrix equation
    k,m = numpy.linalg.lstsq(A, y)[0]
    v = 1/k * 60
    return "Least square solution: f(x)= %.5f x + %.5f" % (v,m)

def plot_curve(xdata, ydata, pret, stat, ori):
    x = numpy.array(xdata)
    y = numpy.array(ydata)
    t = numpy.array(pret)

    A = numpy.vstack([x, numpy.ones(len(x))]).T
    k,m = numpy.linalg.lstsq(A, y)[0]

    plt.plot(x, y, 'bo', label='Original data', markersize=1)
    plt.plot(x, t, 'ro', label='Pre data', markersize=1)
    plt.plot(x, k*x + m, 'k', label='Fitted line')
    plt.legend()
    plt.xlabel('Distance [Degree]')
    plt.ylabel('Time [s]')
    plt.suptitle('Antenna: %s, in %s' % (stat, ori)+ "\n"+ 'Speed:  %.3f, offset: %.3f'%(1/k*60,m))
#    plt.show()
    plt.savefig('%s_%s.png' % (stat, ori))
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


