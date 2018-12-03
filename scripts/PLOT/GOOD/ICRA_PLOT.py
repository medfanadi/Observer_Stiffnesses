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

Obs2=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Obse_Stif_V5_C.txt')   #  Obse_Stif_V5_C
WithOb2=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Without_Stif_V5.txt')

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
#############All errors ############################################################################

y4= butter_lowpass_filter(Obs[:,4], 0.03, 200, 6)
y2= butter_lowpass_filter(WithOb[:,4], 0.03, 200, 6)

y44= butter_lowpass_filter(Obs2[:,4], 0.03, 200, 6)
y22= butter_lowpass_filter(WithOb2[:,4], 0.03, 200, 6)

plt.plot(s44[:],y44[:], 'r', linewidth=4.4)
plt.plot(s22[:],y22[:], 'k--', linewidth=4)

plt.plot(s4[:],y4[:], 'b', linewidth=4.4)
plt.plot(s2[:],y2[:], 'g--', linewidth=4)



plt.xlabel('Curvilinear abscissa  [m]', fontsize=45)
plt.ylabel('Lateral error [$m$]', fontsize=45)
plt.grid(True)
#plt.legend(["$e_y$ with NL observer at $V_x=5m.s^{-1}$ ","$e_y$ Without  observer $C_f$ and $C_r$ at $V_x=5m.s^{-1}$ ","$e_y$ with NL observer at $V_x=8m.s^{-1}$ ","$e_y$ Without  observer $C_f$ and $C_r$ at $V_x=8m.s^{-1}$ "],loc='upper left',fontsize=35)

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)


plt.text(10,0.25,'$(a)$', fontsize=60)


t=s2[2030]


annotate(r'Without  observer ' '\n' 'at $V_x=8m.s^{-1}$',
         xy=(t,y2[2030]), xycoords='data',color='g',
         xytext=(+90, +33), textcoords='offset points', fontsize=40,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color='g'))

t=s22[1850]


annotate(r'Without  observer ' '\n' 'at $V_x=5m.s^{-1}$',
         xy=(t,y22[1850]), xycoords='data',color='k',
         xytext=(-90,-110), textcoords='offset points', fontsize=40,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color='k'))

t=s4[3200]


annotate(r'With NL observer ' '\n' 'at $V_x=8m.s^{-1}$',
         xy=(t,y4[3200]), xycoords='data',color='b',
         xytext=(-150, 90), textcoords='offset points', fontsize=40,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color='b'))

t=s44[1400]


annotate(r'With NL observer ' '\n' 'at $V_x=5m.s^{-1}$',
         xy=(t,y44[1400]), xycoords='data',color='r',
         xytext=(-150, 150), textcoords='offset points', fontsize=40,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color='r'))


plt.xlim((7, 117))   # set the xlim to xmin, xmax
#plt.ylim(xmin, xmax)     # set the xlim to xmin, xmax
plt.show()

#############All errors Angular ############################################################################

kk=180/pi
y4= butter_lowpass_filter(Obs[:,5], 0.03, 200, 6)
y2= butter_lowpass_filter(WithOb[:,5], 0.03, 200, 6)

y44= butter_lowpass_filter(Obs2[:,5], 0.03, 200, 6)
y22= butter_lowpass_filter(WithOb2[:,5], 0.03, 200, 6)

plt.plot(s44[:],y44[:]*kk, 'r', linewidth=4.4)
plt.plot(s22[:],y22[:]*kk, 'k--', linewidth=4.)

plt.plot(s4[:],y4[:]*kk, 'b', linewidth=4.4)
plt.plot(s2[:],y2[:]*kk, 'g--', linewidth=4.)

plt.text(10,4.3,'$(b)$', fontsize=45)

plt.xlabel('Curvilinear abscissa  [m]', fontsize=45)
plt.ylabel('Angualr error [degree]', fontsize=45)
plt.grid(True)
#plt.legend(["$e_y$ with NL observer at $V_x=5m.s^{-1}$ ","$e_y$ Without  observer $C_f$ and $C_r$ at $V_x=5m.s^{-1}$ ","$e_y$ with NL observer at $V_x=8m.s^{-1}$ ","$e_y$ Without  observer $C_f$ and $C_r$ at $V_x=8m.s^{-1}$ "],loc='upper left',fontsize=35)

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)


t=s2[2550]


annotate(r'Without  observer ' '\n' 'at $V_x=8m.s^{-1}$',
         xy=(t,y2[2550]*kk), xycoords='data',color='g',
         xytext=(+33, +33), textcoords='offset points', fontsize=35,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color='g'))

t=s22[1650]


annotate(r'Without  observer ' '\n' 'at $V_x=5m.s^{-1}$',
         xy=(t,y22[1650]*kk), xycoords='data',color='k',
         xytext=(90, -70), textcoords='offset points', fontsize=35,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color='k'))

t=s4[2940]


annotate(r'With NL observer ' '\n' 'at $V_x=8m.s^{-1}$',
         xy=(t,y4[2940]*kk), xycoords='data',color='b',
         xytext=(-90, 90), textcoords='offset points', fontsize=32.5,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color='b'))

t=s44[900]


annotate(r'With NL observer ' '\n' 'at $V_x=5m.s^{-1}$',
         xy=(t,y44[900]*kk), xycoords='data',color='r',
         xytext=(-100, 100), textcoords='offset points', fontsize=35,
         arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2",color='r'))


plt.xlim((7, 117))   # set the xlim to xmin, xmax
#plt.ylim(xmin, xmax)     # set the xlim to xmin, xmax
plt.show()


##### Correnring Stifnesses  ################################################################################

yf4= butter_lowpass_filter(Obs[:,16], 0.03, 200, 6)
yf5= butter_lowpass_filter(Obs[:,17], 0.03, 200, 6)


yf44= butter_lowpass_filter(Obs2[:,16], 0.03, 200, 6)
yf55= butter_lowpass_filter(Obs2[:,17], 0.03, 200, 6)



plt.plot(s44[:],Obs2[:,17], 'r', linewidth=4)
plt.plot(s44[:],Obs2[:,16], 'b', linewidth=4)


plt.plot(s4[:],Obs[:,17]-2600*np.ones(len(yf4)), 'magenta', linewidth=4)
plt.plot(s4[:],Obs[:,16]-2600*np.ones(len(yf4)), 'g', linewidth=4)

plt.text(4,48000,'$(c)$', fontsize=60)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=45)
plt.ylabel('Cornering stiffness $[N.rad^{-1}]$', fontsize=45)
plt.grid(True)
plt.legend(["$\\hat{C}_r$ at $V_x=5m.s^{-1}$"," $\\hat{C}_f$ at $V_x=5m.s^{-1}$","$\\hat{C}_r$ at $V_x=8m.s^{-1}$","$\\hat{C}_f$ at $V_x=8m.s^{-1}$"],fontsize=45)


plt.xlim((0, 117))   # set the xlim to xmin, xmax
plt.ylim((0, 55000))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)
plt.show()

