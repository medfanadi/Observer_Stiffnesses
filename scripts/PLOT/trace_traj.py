#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from math import *
import numpy as np
import matplotlib.pyplot as plt
from cardraw import draw_car
import shapely.geometry as geom
from scipy import interpolate
from scipy import signal
from scipy import fftpack
from pylab import *

import shapely.geometry as geom
from scipy import spatial
from ButterFilter import butter_lowpass_filter


kk=180/pi

######Trajectory plot   #################################################################

res4=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/LQR_Stif_V5.txt')




X4= butter_lowpass_filter(res4[:,1], 0.04, 10, 8)
Y4= butter_lowpass_filter(res4[:,2], 0.04, 10, 8)




Xref= butter_lowpass_filter(res4[:,10], 0.04, 10, 8)
Yref= butter_lowpass_filter(res4[:,11], 0.04, 10, 8)

Xref=Xref[:]+X4[0]-Xref[0]
Yref=Yref[:]+Y4[0]-Yref[0]
#plt.plot(res1[:,10],res1[:,11], 'b', linewidth=4.0)


plt.plot(X4,Y4, 'r--', linewidth=3.0)
plt.plot(Xref,Yref, 'g', linewidth=3.0)

plt.axis('equal')
#plt.axis([-50, 10, -10, 70])
plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)
plt.xlabel('x [m]', fontsize=40)
plt.ylabel('y [m]', fontsize=40)

#########################################################################################
#########################################################################################

lf=0.7
lr=0.7
tr=0.5
rw=0.2
dx=0.2
dy=0.2

temps1=res4[:,0]
temps2=res4[:,0]
zoom=4


ix = interpolate.interp1d(res4[:,0],res4[:,1])
iy = interpolate.interp1d(res4[:,0],res4[:,2])
iyaw = interpolate.interp1d(res4[:,0],res4[:,3])
ibf = interpolate.interp1d(res4[:,0],res4[:,7])
ibr = interpolate.interp1d(res4[:,0],np.zeros(len(temps1)))
n=6
i=0

while (i<n):
	tempsp=temps1[int(i*(len(temps1)-1)/(n-1))]
	tempss=temps2[int(i*(len(temps2)-1)/(n-1))]
	x=np.array([ix(tempsp),iy(tempsp),iyaw(tempsp),ibf(tempss),ibr(tempss)])
	draw_car(x,lf,lr,tr,dx,dy,rw,zoom)
	i=i+1
#########################################################################################

#########################################################################################

plt.grid(True)
plt.legend([" Path at $V=4 m.s^{-1} $"," Path at $V=8 m.s^{-1} $","Reference path"],fontsize=25)
plt.show()

############################  Curvilinear abscissa  ##############################

s4=np.zeros(len(res4[:,1]))

i=0
while (i<len(res4[:,1])-1):
	s4[i+1]=s4[i]+hypot(res4[i+1,1]-res4[i,1],res4[i+1,2]-res4[i,2])
	i=i+1


########################### Error trace #########################################



y4= butter_lowpass_filter(res4[:,4], 0.03, 200, 6)



plt.plot(s4[:],y4[:], 'b', linewidth=3)



plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('$y$ [m]', fontsize=35)
plt.grid(True)
plt.legend(["y at $V_x=4 m.s^{-1} $","y at $V_x=8 m.s^{-1} $"])

#plt.xlim((15, 107))   # set the xlim to xmin, xmax
#plt.ylim(xmin, xmax)     # set the xlim to xmin, xmax
plt.show()
#####
y4= butter_lowpass_filter(res4[:,5], 0.03, 200, 6)


kk=180/pi
plt.plot(s4[:],y4[:]*kk, 'b', linewidth=3)



plt.xlabel('Curvilinear abscissa  [m]', fontsize=25)
plt.ylabel('$\\tilde \\theta$ [deg]', fontsize=25)
plt.grid(True)
plt.legend(["$\\tilde \\theta$ at $V_x=4 m.s^{-1} $","$\\tilde \\theta$ at $V_x=8 m.s^{-1} $"])

plt.xlim((15, 107))   # set the xlim to xmin, xmax

plt.show()

##### Braquage ################################################################################

yf4= butter_lowpass_filter(res4[:,8], 0.03, 200, 6)
yf5= butter_lowpass_filter(res4[:,9], 0.03, 200, 6)





 
plt.plot(s4[:],180/pi*yf4, 'b', linewidth=3)
plt.plot(s4[:],180/pi*yf5, 'r', linewidth=3)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('Steering angles [deg]', fontsize=35)
plt.grid(True)
plt.legend(["$\\delta_f$ at $V=4 m.s^{-1} $","$\\delta_r$ at $V=8 m.s^{-1} $"],fontsize=35)

plt.xlim((15, 107))   # set the xlim to xmin, xmax

plt.show()


##### Corr ################################################################################

yf4= butter_lowpass_filter(res4[:,16], 0.03, 200, 6)
yf5= butter_lowpass_filter(res4[:,17], 0.03, 200, 6)


plt.plot(s4[:],yf4, 'b', linewidth=3)
plt.plot(s4[:],yf5, 'r', linewidth=3)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('Cornering stiffness $[N.rad^{-1}]$', fontsize=35)
plt.grid(True)
plt.legend(["$C_f$ ","$C_r$"],fontsize=30)



plt.show()

##### slip ################################################################################

yf4= butter_lowpass_filter(res4[:,18], 0.03, 200, 6)
yf5= butter_lowpass_filter(res4[:,19], 0.03, 200, 6)


plt.plot(s4[:],yf4*kk, 'b', linewidth=3)
plt.plot(s4[:],yf5*kk, 'r', linewidth=3)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('Slip angles $[deg]$', fontsize=35)
plt.grid(True)
plt.legend(["$\\beta_{f}$ ","$\\beta_{r}$"],fontsize=30)



plt.show()

##### forces  ################################################################################

yf4= butter_lowpass_filter(res4[:,20], 0.03, 200, 6)
yf5= butter_lowpass_filter(res4[:,21], 0.03, 200, 6)

 
plt.plot(s4[:],yf4, 'b', linewidth=3)
plt.plot(s4[:],yf5, 'r', linewidth=3)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('Lateral forces $[N]$', fontsize=35)
plt.grid(True)
plt.legend(["$F_{yF}$ ","$F_{yR}$"],fontsize=30)



plt.show()



##### Vy ################################################################################

yf4= butter_lowpass_filter(res4[:,6], 0.02, 200, 6)






 
plt.plot(s4[:],yf4, 'b', linewidth=3)



plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('$V_y [m.s^{-1}]$', fontsize=35)
plt.grid(True)
plt.legend(["Vy"])



plt.show()


##### Vpsi ################################################################################

yf4= butter_lowpass_filter(res4[:,13], 0.02, 200, 6)

yf2= butter_lowpass_filter(res4[:,7], 0.02, 200, 6)





 
plt.plot(s4[:],yf4, 'b', linewidth=3)
plt.plot(s4[:],yf2, 'r', linewidth=3)



plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('$V_\psi[rad.s^{-1}]$', fontsize=35)
plt.grid(True)
plt.legend(["Vpsi"])



plt.show()


