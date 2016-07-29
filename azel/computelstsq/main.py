#!/usr/bin/python

# Import module
import leastsq

# Data points
ydata = [0.1,1.2,1.8,4,5,6,7,8,9]
xdata = [0,1,2,4,5,6,7,8,9]

# Calculate least square
ans = leastsq.least_sq(xdata, ydata)
print ans

# Plot graph of the result and the original data
leastsq.plot_curve(xdata, ydata)

# Compute the time it takes to get up to max speed
t = leastsq.start_time(xdata, ydata)
print 'Start time is: %.5f s'% (t)

# Compute the speed of the antenna
v = leastsq.speed(xdata, ydata)
print 'Speed of the antenna: %.5f deg/s'% (v)
