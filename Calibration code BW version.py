# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:45:58 2022

@author: bwats

This code creates 3 figures which can be used to optimise settings 
when makeing the 3d image.

Figure 1: is an image of the lens with a line that the intensity is read from

Figure 2: is the intensity along the red line in figure 1, the peaks of this graph
    should be marked with an x to mark them

Figure 3: is a profile of the lens from the centre to the end of red line in figure 
    1, the points on this graph corispond to the peaks in figure 2 
    

the # comments discribe what the code does
the coments inside ""  discribe the places that the code might be adjusted
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


# creating a figure
fig1, ((ax1)) = plt.subplots(1,1)


'''
input the name of the IRM image you want to look at below 
''' 
# plotting the lens image
img = plt.imread('35mm rep3.png')
ax1.imshow(img)


'''
input centre coordinates determined in FIJI (in pixels)
'''
# centre of lens
o = np.array([1026 , 1071])


'''
length of the red line can be adjusted so the maximum number of fringes are
recorded - this should be the distance in pixels from the centre of the image to the edge.
'''
# radius of outward line
r = 950


'''
angle of red line r is adjusted to check the find_peak perameters at different 
places on the lens (in radians) 
'''
# angle of outward line
angle =0

# point at the end of the line
point = np.array([r*np.cos(angle)+o[0], r*np.sin(angle)+o[1]])
num_points = int(abs((o[0]-point[0])+1 + abs(o[1]-point[1]+1)/2))

# creating the line
xarray = np.linspace(o[0], point[0], num_points)
m = (point[1]-o[1])/(point[0]-o[0])
yarray = m * (xarray - point[0]) + point[1]

# plotting the line
ax1.plot(xarray, yarray, 'r')
ax1.plot(point[0], point[1], 'xb')

# the straght line but all the points are rounded to 0 d.p.
xarray2 = np.around(xarray, 0).astype(int)
yarray2 = np.around(yarray, 0).astype(int)

# picks the same points on the lens image which is the intensity
intensity = img[yarray2, xarray2, 0]

# distance from the centre
r_vals = np.sqrt((xarray2-xarray2[0])**2+(yarray2-yarray[0])**2)

# intensity plot
fig2, ((ax2)) = plt.subplots(1, 1, figsize=(12, 6))
ax2.plot(r_vals, intensity, label='intensity of pixels')
ax2.set(title='Intensity Plot Along line',
        xlabel='Distance From Centre (m)',
        ylabel='Intensity (AU)')

'''
the lines below can be used to adjust which peaks are selected,
three variables are used in the function below:
 height - is the minimum height that a peak can be
 distance - is the minimum distance between peaks (messured in pixels)
 prominance - is to do with a peaks height relitive to its surrounding peaks

for more details and more variable options see find_peaks documentation 
'''
# selecting the peaks
peak, _ = find_peaks(intensity, height=(0.2), 
                     distance=(7), prominence=(0.5)) 

# plots the peaks of the intensity onto the same figure
ax2.plot(r_vals[peak], intensity[peak], 'xk', label='intensity peaks')
ax2.legend()
# loop creates the values for the hights at each peak 
N = 0
Z = []
'''
lamb is wavelength in meters, should be updated according 
to image acquisition settings.
'''
lamb = 458e-9
while N < len(peak):
    z = (N + 1/2) * lamb/2
    Z.append(z)
    N +=1

# creates an array of all the z values
Z = np.array(Z)

# plots the graph of the profile
fig3, ((ax3)) = plt.subplots(1, 1, figsize=(12,8))
ax3.plot(r_vals[peak], Z, 'o', label='Bright Fringes')
ax3.set(title='Lens Profile',
        xlabel='Distance Along r (pixels)',
        ylabel='Distance in z (m)')
ax3.legend()


