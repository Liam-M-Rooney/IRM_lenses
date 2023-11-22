# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 10:50:12 2022

@author: bwats
"""

import numpy as np
import matplotlib.pyplot as plt

def bins(x, b_num):
    length = (max(x))/b_num # is the width of each bin
    bin0 = np.arange(0, max(x)+length, length)
    bin1 = np.array([])
    i = 0
    while i < b_num:
        a = x[bin0[i] < x ]
        a = a[ a < bin0[i+1]]
        bin1 = np.append(bin1, len(a))
        i += 1
    return bin1
    

'''
loads in the file created in the 3D reconstruction code
'''
d = np.loadtxt('35mm rep3 data')
'''
R is the theoretical Radius of curvature of the lens in meters
binl is the number of bins used in the histogram
'''
R = 0.01809
binl = 200
bins = bins(d, binl)
# bins = bins[bins>0]
x_vals = np.linspace(0, max(d), len(bins))
y_vals = np.linspace(0, max(bins), 100)

fig1, ((ax1)) = plt.subplots(1, 1, figsize=(15, 10))
ax1.bar(x_vals, bins, color='k',  align='edge', width=0.0008, label='Practical results')
# plt.plot(np.mean(d)* np.ones(len(y_vals)), y_vals, '--b', 
#           label='average radius')
ax1.plot(R * np.ones(len(y_vals)), y_vals, '--g', 
          label='Theoretical value')
ax1.set(title='Measured distribution of radius of curvature over lens surface')
ax1.legend()
ax1.set(xlabel='Radius of Curvature (m)',
        ylabel='Frequency of points at radius')


fig2, ((ax2)) = plt.subplots(1, 1, figsize=(15, 10))

x_vals2 = np.linspace(0, len(d), len(d))
ax2.plot(x_vals2, d, '.k', label='data points')
ax2.set(title='lens curvature across its surface', 
        xlabel='data points from reconstructed lens', 
        ylabel='radius at point (m)')
ax2.plot(x_vals2, np.ones(len(x_vals2)) * R, '-.g', 
         label='theoretical curvature')
ax2.legend()

'''
data in d is all the recorded points on the reconstructed lens
the way the recorded data starts at the smallest bright fringe and the smallest 
angle. then the next point is the smallest bright fringe at a slightly larger 
angle, once the angle has incresed to 360 degrees the next point on in the data 
is the second smallest fringe at angle 0. this then repeats

due to this the data on the left hand side of the plot is the lens curvature at 
small r, the waveyness of the plot is due to not being perfectly circular. 

'''
D = np.where(bins==bins.max())
curve = x_vals[D]
print('\n Curvature of the lens UV4 is', curve, 'm')

