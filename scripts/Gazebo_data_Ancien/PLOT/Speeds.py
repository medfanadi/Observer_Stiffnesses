#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from math import *
import numpy as np
from math import *
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

Vpsi_gazebo=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/Vpsi_Gazebo_V8.txt')
Vy_gazebo=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/Vy_Gazebo_V8.txt')
Vx_gazebo=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/Vy_Gazebo_V8.txt')
res=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/Traj_V8.txt')
sim=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/LQR_Stif_V8.txt')

Obs=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data/PLOT/LQR_Stif_V8.txt')#np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Obse_Stif_V8.txt')
WithOb=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Without_Stif_V8.txt')




#X4= butter_lowpass_filter(Vpsi_gazebo[:,1], 0.04, 10, 8)
#Y4= butter_lowpass_filter(Vpsi_gazebo[:,2], 0.04, 10, 8)

k=[]
Vy=[]
q=[]


for i in range(len(Vpsi_gazebo)):
	if i % 2==1:
		q.append(Vpsi_gazebo[i])


print(np.shape(res[:,3]))
print(len(Vy_gazebo))
print(np.shape(Vx_gazebo))

for i in range(len(Vy_gazebo)):
	if i % 2==0:
		Vy=Vy_gazebo[i]*math.cos(res[i/2,3]-pi)-Vx_gazebo[i]*math.sin(res[i/2,3]-pi)-1.9
		k.append(Vy)
		

#for i in range(len(k)):
#	k[i]=-k[i]

X4= butter_lowpass_filter(k[:], 0.8, 10, 8)
q4= butter_lowpass_filter(q[:], 0.04, 10, 8)
yf4= butter_lowpass_filter(sim[:,6], 0.02, 200, 6)

############################  Curvilinear abscissa  ##############################





s4=np.zeros(len(res[:,1]))



i=0
while (i<len(res[:,1])-1):
	s4[i+1]=s4[i]+hypot(res[i+1,1]-res[i,1],res[i+1,2]-res[i,2])
	i=i+1


s44=np.zeros(len(sim[:,1]))


s14=np.zeros(len(Obs[:,1]))
s2=np.zeros(len(WithOb[:,1]))
i=0
while (i<len(Obs[:,1])-1):
	s14[i+1]=s14[i]+hypot(Obs[i+1,1]-Obs[i,1],Obs[i+1,2]-Obs[i,2])
	i=i+1

i=0
while (i<len(sim[:,1])-1):
	s44[i+1]=s44[i]+hypot(sim[i+1,1]-sim[i,1],sim[i+1,2]-sim[i,2])
	i=i+1


#############################################

yf4= butter_lowpass_filter(Obs[:,6], 0.02, 200, 6)
plt.plot(s14[:],yf4, 'r', linewidth=3.5)

plt.plot(s4[:]-12*np.ones(len(s4[:])),X4/-19-0.005*np.ones(len(X4[:])), 'k--', linewidth=4.0)




#plt.plot(s44[:],yf4, 'r', linewidth=3.0)

plt.xlabel('Curvilinear abscissa  [$m$]', fontsize=40)
plt.ylabel('Lateral velocity $[m.s^{-1}]$', fontsize=35)
plt.grid(True)
plt.legend(["$V_y$ estimated","$V_y$ calculated by gazebo"],fontsize=30)

plt.xlim((21, 120))   # set the xlim to xmin, xmax
plt.ylim(-0.35, 0.35)     # set the xlim to xmin, 

plt.yticks( color='k', size=38)
plt.xticks( color='k', size=38)

plt.show()




##################



yf4= butter_lowpass_filter(sim[:,13], 0.02, 200, 6)

yf2= butter_lowpass_filter(sim[:,7], 0.02, 200, 6)

plt.plot(s44[:],yf4, 'r', linewidth=3.0)



plt.plot(s44[:],yf4+0.01, 'g--', linewidth=4.50)

plt.plot(s4[:],q4-0.01, 'k--', linewidth=4.0)

plt.xlabel('Curvilinear abscissa  [m]', fontsize=45)
plt.ylabel('Yaw rate $[rad.s^{-1}]$', fontsize=45)
plt.grid(True)
plt.legend(["$V_\psi$ observed","$V_\psi$ measured","$V_\psi$ calculated by gazebo"],loc='upper left',fontsize=45)

plt.xlim((5, 120))   # set the xlim to xmin, xmax
plt.ylim(-0.65, 0.73)     # set the xlim to xmin


plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)


#plt.text(106,0.68,'$(d)$', fontsize=60)

plt.show()


