# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 15:04:37 2022

@author: bwats

This file whill give an output of two figures:
    
1. the IRM image which can be used to compare to the 3d reconstruction

2.  is the 3d reconstruction of the lens with the theoretical 
    lens also implemented
    
this file will also print the max the min and the mean of the 
lens curvature
"""


import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from matplotlib import cm 
from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'qt')

# creates figure
fig1, ((ax1)) = plt.subplots(1,1)


'''
imput IRM image file name into the variable img
'''
# importing the image and showing the image
img = plt.imread('35mm rep3.png')
# shows the first image - the IRM image
ax1.imshow(img)


'''
in the variable o imput the same values for the 
centre as are in the calibration code
'''
# centre of lens
o = np.array([1026 , 1071])

# angle and radius
angle = np.linspace(0, 2*np.pi, 360)

'''
imput the radius from the calibration code
'''
r = 950


'''
is the wavelength of light used for the IRM imaging
'''
# wavelength
lamb = 458e-9


'''
the number of fringes will take some trial and error to find what 
number of fringes are detected by the code.
if you have too many fringes you will get an error message like:
    
    IndexError: index 12 is out of bounds for axis 0 with size 12
    
this tells you the max number of fringes the code can read which can
then be imputed into the variable N as:
    
    N = np.linspace(0, 11, 12)

'''
# number of fringes
N = np.linspace(0, 13, 14).astype(int)
# z vals
Z = (N + 0.5) * lamb/2

# fringe counter
J = 0

# angle counter
i = 0

# ploting 3d plot
fig1 = plt.figure(figsize=(30,30))

# will store all the value R of the curvature
bigR = np.array([]) #???

# creating the 3d plot
ax = plt.axes(projection='3d')


'''
the scale of the plot will depend on how much of the lens you image 
the lens is at the origin so in the x -y plane the valus should have 
equal distance on either side of the origin
putting the scale of the z axis to 50x larger than x- y plane gives a 
good image of the lens.
'''
# setting the limits on the lens graph
ax.set_xlim3d(-800e-6/2, 800e-6/2)
ax.set_ylim3d(-800e-6/2, 800e-6/2)
ax.set_zlim3d(0, 1e-5)

while J<len(N):
    # these arrays will store info used to plot the lens
    R_vals = np.array([]) # ???
    X = np.array([])
    Y = np.array([])
    
    while i<len(angle):
        
        #point at the end of the line
        point = np.array([r*np.cos(angle[i])+o[0], r*np.sin(angle[i])+o[1]])
        num_points = 800
        
        # creating the line
        xarray = np.linspace(o[0], point[0], num_points)
        m = (point[1]-o[1])/(point[0]-o[0])
        yarray = m * (xarray - point[0]) + point[1]

# the three lines below can be used to plot the radiuses that the intensitys
# taken over on the IRM image 
       
        # # plotting the line
        # ax1.plot(xarray, yarray, 'r')
        # ax1.plot(point[0], point[1], 'xb')
        
        # the straght line but all the points are rounded to 0 d.p.
        xarray2 = np.around(xarray, 0).astype(int)
        yarray2 = np.around(yarray, 0).astype(int)
        
        # pickes the same points on the lens image which is the intensity
        dark = img[yarray2, xarray2, 1]
        
        # distance from the centre
        r_vals = np.sqrt((xarray2-xarray2[0])**2+(yarray2-yarray[0])**2)
        
        '''
        input scaling value (um/px)
        '''
        r_vals = r_vals * (847.87e-6 / 2048) 


        '''
        the variable peak can be copyed from calibration code
        '''
        # selecting the troughs
        peak, _ = find_peaks(dark, height=(0.2), distance=(7), 
                             prominence=(0.5))
        
        R_vals = np.append(R_vals, r_vals[peak[J]])   # ???
        # x- y coordinates
        x = r_vals[peak[J]]*np.cos(angle[i])
        y = r_vals[peak[J]]*np.sin(angle[i])
        X = np.append(X, x)
        Y = np.append(Y, y)
        i+=1
    

    # radius calculater 
    R_vals = R_vals[1:]   #???
    R1 = (R_vals**2 + Z[J]**2)/(2 * Z[J]) # ??? 
    bigR = np.append(bigR, R1) #???
    
    # plotting  3d graph
    ax.scatter3D(X, Y, Z[J], c='k')
    i = 0



    
    J += 1

    
# ???
# finding the mean curvature
meanr = np.mean(bigR)
# finding the min curvature
minr = min(bigR)
# finding the max curvature
maxr = max(bigR)
print('\n Theoretical curvature is 0.01809m')
print('\n avarage curve of lens is', meanr, 'm')
print('\n minimum curvature is', minr, 'm')
print('\n maximum curvature is', maxr, 'm')
# ???

'''
the line below can be uncomented to save the lens curvature bigR as a seperate 
file
'''
np.savetxt('35mm rep3 data', bigR) 


# theoretical radius which has been copyed in from the theory lens code
start = 0
end  = 2 * np.pi

R = 18.09e-3
z1 = 3.3e-3
r1 = (abs((z1 - R)**2 - R**2))**(1/2)
i = 1

while start < np.pi * 2:
    angle = np.linspace(start, end, 360)
    r_vals = np.linspace(0, r1, len(angle))
    z1 = R - np.sqrt(abs(R**2 - (r_vals)**2))
    z1 = z1[z1< max(Z)]
    
    x1 = r_vals * np.cos(angle)
    x1 = x1[:len(z1)]
    y1 = r_vals * np.sin(angle)
    y1 = y1[:len(z1)]
    ax.plot3D(x1, y1, z1, c=((0,1,0)))
    i+=1
    start += np.pi /180
    end += np.pi /180


# this code double checks that the theoretical lens curvature 
# is what is expected 
r1 = r_vals[:len(z1)]
z1 = z1[1:]
r1 = r1[1:]
R1 = (r1**2 + z1**2)/(2*z1)



