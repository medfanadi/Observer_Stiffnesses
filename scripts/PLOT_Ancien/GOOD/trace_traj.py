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

Obs=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Obse_Stif_V8.txt')
WithOb=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Without_Stif_V8.txt')

Obs2=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Obse_Stif_V5.txt')
WithOb2=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Without_Stif_V5.txt')

X4= butter_lowpass_filter(Obs[:,1], 0.04, 10, 8)
Y4= butter_lowpass_filter(Obs[:,2], 0.04, 10, 8)

X2= butter_lowpass_filter(WithOb[:,1], 0.04, 10, 8)
Y2= butter_lowpass_filter(WithOb[:,2], 0.04, 10, 8)


Xref= butter_lowpass_filter(Obs[:,10], 0.04, 10, 8)
Yref= butter_lowpass_filter(Obs[:,11], 0.04, 10, 8)

Xref=Xref[:]+X4[0]-Xref[0]
Yref=Yref[:]+Y4[0]-Yref[0]
#plt.plot(res1[:,10],res1[:,11], 'b', linewidth=4.0)

plt.plot(Xref,Yref, 'g', linewidth=4.5)
plt.plot(X4,Y4, 'r--', linewidth=4)
plt.plot(X2,Y2, 'b--', linewidth=4)
plt.axis('equal')
#plt.axis([-50, 10, -10, 70])
plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)
plt.xlabel('x [m]', fontsize=48)
plt.ylabel('y [m]', fontsize=48)

#########################################################################################
#########################################################################################

lf=0.7
lr=0.7
tr=0.5
rw=0.2
dx=0.2
dy=0.2

temps1=Obs[:,0]
temps2=Obs[:,0]
zoom=5.5


ix = interpolate.interp1d(Obs[:,0],Obs[:,1])
iy = interpolate.interp1d(Obs[:,0],Obs[:,2])
iyaw = interpolate.interp1d(Obs[:,0],Obs[:,3])
ibf = interpolate.interp1d(Obs[:,0],Obs[:,7])
ibr = interpolate.interp1d(Obs[:,0],-Obs[:,7])
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
plt.ylim(-5, 76)     # set the xlim to xmin, xmax
plt.xlim(-110,8)     # set the xlim to xmin, xmax
plt.grid(True)
plt.legend(["Reference path"," Path with NLO  "," Path without observer"],loc='upper left',fontsize=36)
plt.show()

############################  Curvilinear abscissa  ##############################

s4=np.zeros(len(Obs[:,1]))
s2=np.zeros(len(WithOb[:,1]))
i=0
while (i<len(Obs[:,1])-1):
	s4[i+1]=s4[i]+hypot(Obs[i+1,1]-Obs[i,1],Obs[i+1,2]-Obs[i,2])
	i=i+1

i=0
while (i<len(WithOb[:,1])-1):
	s2[i+1]=s2[i]+hypot(WithOb[i+1,1]-WithOb[i,1],WithOb[i+1,2]-WithOb[i,2])
	i=i+1

s44=np.zeros(len(Obs2[:,1]))
s22=np.zeros(len(WithOb2[:,1]))
i=0
while (i<len(Obs2[:,1])-1):
	s44[i+1]=s44[i]+hypot(Obs2[i+1,1]-Obs2[i,1],Obs2[i+1,2]-Obs2[i,2])
	i=i+1

i=0
while (i<len(WithOb2[:,1])-1):
	s22[i+1]=s22[i]+hypot(WithOb2[i+1,1]-WithOb2[i,1],WithOb2[i+1,2]-WithOb2[i,2])
	i=i+1
########################### Error trace #########################################



y4= butter_lowpass_filter(Obs[:,4], 0.03, 200, 6)
y2= butter_lowpass_filter(WithOb[:,4], 0.03, 200, 6)


plt.plot(s4[:],y4[:], 'b', linewidth=3)
plt.plot(s2[:],y2[:], 'r', linewidth=3)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=38)
plt.ylabel('Lateral error [m]', fontsize=40)
plt.grid(True)
plt.legend(["$e_y$ with NLO ","$e_y$ with averge estimation of $C_f$ and $C_r$"],loc='upper left',fontsize=35)

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)



plt.xlim((7, 117))   # set the xlim to xmin, xmax
#plt.ylim(xmin, xmax)     # set the xlim to xmin, xmax
plt.show()
#########################################################################################
y4= butter_lowpass_filter(Obs[:,5], 0.025, 200, 6)
y2= butter_lowpass_filter(WithOb[:,5], 0.025, 200, 6)

kk=180/pi
plt.plot(s4[:],y4[:]*kk, 'b', linewidth=3)
plt.plot(s2[:],y2[:]*kk, 'r', linewidth=3)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('Angular error [deg]', fontsize=40)
plt.grid(True)
plt.legend(["$e_\\psi$ with NLO ","$e_\\psi$ with averge estimation of $C_f$ and $C_r$"],loc='upper left',fontsize=35)
plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)

plt.xlim((7, 117))   # set the xlim to xmin, xmax

plt.show()


##### Braquage ################################################################################

yf4= butter_lowpass_filter(Obs2[:,8], 0.02, 200, 6)
yf5= butter_lowpass_filter(Obs2[:,9], 0.02, 200, 6)

yf2= butter_lowpass_filter(WithOb2[:,8], 0.02, 200, 6)
yf3= butter_lowpass_filter(WithOb2[:,9], 0.02, 200, 6)


#plt.text(10,12.5,'$(b)$', fontsize=45)
 
plt.plot(s44[:],kk*yf4, 'b', linewidth=3.5)

plt.plot(s44[:],kk*yf5, 'r', linewidth=3.5)

plt.plot(s22[:],kk*yf2, 'g', linewidth=3.5)



plt.plot(s22[:],kk*yf3, 'magenta', linewidth=3.5)

plt.xlabel('Curvilinear abscissa  [$m$]', fontsize=40)
plt.ylabel('Steering angles [$^\\circ$]', fontsize=40)
plt.grid(True)
plt.legend(["$\\delta_f$ with NLO  ","$\\delta_r$ with NLO  ","$\\delta_f$ without NLO ","$\\delta_r$ without observer"],fontsize=42)

plt.xlim((5, 115))   # set the xlim to xmin, xmax
plt.ylim((-10, 12))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)

plt.show()


##### Correnring Stifnesses  ################################################################################

yf4= butter_lowpass_filter(Obs[:,16], 0.03, 200, 6)
yf5= butter_lowpass_filter(Obs[:,17], 0.03, 200, 6)



 
plt.plot(s4[:],yf4, 'b', linewidth=3)
plt.plot(s4[:],yf5, 'r', linewidth=3)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=38)
plt.ylabel('Cornering stiffness $[N.rad^{-1}]$', fontsize=35)
plt.grid(True)
plt.legend(["$C_f$ ","$C_r$"],fontsize=40)


plt.xlim((10, 117))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=30)
plt.xticks( color='k', size=30)
plt.grid(True)
plt.show()

##### slip  Angles ################################################################################

yf4= butter_lowpass_filter(Obs[:,18], 0.02, 200, 6)
yf5= butter_lowpass_filter(Obs[:,19], 0.02, 200, 6)


yf2= butter_lowpass_filter(WithOb[:,18], 0.02, 200, 6)
yf3= butter_lowpass_filter(WithOb[:,19], 0.02, 200, 6)

#plt.text(10,8.,'$(b)$', fontsize=60)


plt.plot(s4[:],180/pi*yf4, 'b', linewidth=4.2)
plt.plot(s4[:],180/pi*yf5, 'b--', linewidth=4)

plt.plot(s2[:],180/pi*yf2, 'r', linewidth=4.2)
plt.plot(s2[:],180/pi*yf3, 'r--', linewidth=4)

plt.xlabel('Curvilinear abscissa  [$m$]', fontsize=45)
plt.ylabel('Slip angles [$^\\circ$]', fontsize=45)
plt.grid(True)
plt.legend(["$\\beta_f$ with NLO  ","$\\beta_r$ with NLO ","$\\beta_f$ without NLO ","$\\beta_r$ without NLO"],fontsize=45)

plt.xlim((2, 118))   # set the xlim to xmin, xmax
plt.ylim((-6.1, 9.2))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)
plt.grid(True)
plt.show()

##### forces  ################################################################################

yf4= butter_lowpass_filter(Obs[:,20], 0.03, 200, 6)
yf5= butter_lowpass_filter(Obs[:,21], 0.03, 200, 6)

yf2= butter_lowpass_filter(WithOb[:,20], 0.03, 200, 6)
yf3= butter_lowpass_filter(WithOb[:,21], 0.03, 200, 6)



 
plt.plot(s4[:],yf4, 'b', linewidth=3)

plt.plot(s2[:],yf2, 'r', linewidth=3)

plt.plot(s4[:],yf5, 'b--', linewidth=3)

plt.plot(s2[:],yf3, 'r--', linewidth=3)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=40)
plt.ylabel('Lateral forces $[N]$', fontsize=40)
plt.grid(True)
plt.legend(["$F_{yF}$ with NLO  ","$F_{yF}$ with averge estimation of $C_f$ and $C_r$  ","$F_{yR}$ with NLO  ","$F_{yR}$ with averge estimation of $C_f$ and $C_r$  "],fontsize=28)


plt.xlim((2, 118))   # set the xlim to xmin, xmax
plt.ylim((-1500, 1500))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=30)
plt.xticks( color='k', size=30)

plt.show()



##### Vy ################################################################################

yf4= butter_lowpass_filter(Obs[:,6], 0.02, 200, 6)
plt.plot(s4[:],yf4, 'b', linewidth=3)



plt.xlabel('Curvilinear abscissa  [m]', fontsize=35)
plt.ylabel('Lateral velocity $ [m.s^{-1}]$', fontsize=40)
plt.grid(True)
plt.legend(["$V_y$ observed"],fontsize=40)


plt.xlim((4, 120))   # set the xlim to xmin, xmax
plt.ylim((-0.35, 0.35))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)


plt.show()


##### Vpsi ################################################################################

yf4= butter_lowpass_filter(Obs[:,13], 0.02, 200, 6)

yf2= butter_lowpass_filter(Obs[:,7], 0.02, 200, 6)





 
plt.plot(s4[:],yf4, 'b+', linewidth=3)
plt.plot(s4[:],yf2, 'r--', linewidth=3)



plt.xlabel('Curvilinear abscissa  [m]', fontsize=40)
plt.ylabel('Yaw rate $[rad.s^{-1}]$', fontsize=40)
plt.grid(True)
plt.legend(["$V_\psi$ observed ","$V_\psi$ measured "],fontsize=25)


plt.xlim((4, 120))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)


plt.show()


