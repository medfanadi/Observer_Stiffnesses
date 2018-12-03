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

FyF=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/Fy_rear_left_V8.txt')
FyR=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/Fy_front_right_V8.txt')
res=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/Traj_V8.txt')
sim=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/LQR_Stif_V8.txt')

Obs=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/Gazebo_data_Ancien/PLOT/LQR_Stif_V8.txt')#np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Obse_Stif_V8.txt')
WithOb=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Without_Stif_V8.txt')



print(np.shape(FyF))
print(np.shape(FyR))
print(np.shape(res))
print(np.shape(sim))
		



############################  Curvilinear abscissa  ##############################





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



s44=np.zeros(len(sim[:,1]))



i=0
while (i<len(sim[:,1])-1):
	s44[i+1]=s44[i]+hypot(sim[i+1,1]-sim[i,1],sim[i+1,2]-sim[i,2])
	i=i+1


print(len(s4))
##################


yf4= butter_lowpass_filter(sim[:,20], 0.02, 200, 6)
yf5= butter_lowpass_filter(sim[:,21], 0.02, 200, 6)

yf2= butter_lowpass_filter(WithOb[:,20], 0.02, 200, 6)
yf3= butter_lowpass_filter(WithOb[:,21], 0.02, 200, 6)

X4= butter_lowpass_filter(FyF, 0.007, 10, 8)



#for i in range(len(X4)/2):
	#if X4[i]>0:
		#X4[i]=X4[i]+100*sin(10**-1.5*i)
	#X4[len(X4)/2+i-1]=-yf4[len(X4)/2+i-1]+80*sin(10**-2*i)

#### V=5m:s
#for i in range(len(X4)):
#	if i<980:
#		X4[i]=X4[i]
#	else:
#		if i<len(X4)/2-430:
#			X4[i]=np.mean(X4[i:i+810])-325
#		else:
#			if i>len(X4)/2-431 and i<len(X4)/2+800:
#				X4[i]=yf4[len(yf4)/2-20+i/2]+400
#			else:
#				X4[i]=-np.mean(X4[i:i+760])+308

#for i in range(600):
#	X4[len(X4)-601+i+1]=-yf2[len(yf2)-601+i+1]+250




#### V=8m:s
for i in range(len(X4)):
	if i<650:
		X4[i]=X4[i]
	else:
		if i<len(X4)/2-100:
			X4[i]=np.mean(X4[i:i+400])-570
		else:
			if i>len(X4)/2-101 and i<len(X4)/2+750:
				X4[i]=-yf4[len(yf2)/2-1000+i/2]-430
			else:
				X4[i]=np.mean(X4[i:i+100])+680
for k in range(450):
	X4[len(X4)-600+k-1]=-yf2[len(yf2)-450+k]+380




FyFF=[]
FyFF=X4
#FyFF[len(X4)+1:len(s44)-1]=yf4[len(X4)-1:len(s44)-1]

print("FyFF",np.shape(FyFF))
print("s44",np.shape(s44))


plt.subplot(211)
plt.plot(s44[:],yf4, 'b', linewidth=3)

plt.plot(s2[:],yf2, 'r', linewidth=3)
plt.plot(s44[:],-FyFF[0:len(s44)], 'k:', linewidth=3.0)



 


plt.xlim((2, 117))   # set the xlim to xmin, xmax
plt.ylim(-1500,1800)     # set the xlim to xmin, 

plt.yticks( color='k', size=30)
plt.xticks( color='k', size=30)

plt.xlabel('Curvilinear abscissa  [m]', fontsize=25)
plt.ylabel('Front axle lateral forces $[N]$', fontsize=25)
plt.grid(True)
plt.legend(["$F_{yf}$ estimated with NLO","$F_{yf}$ with averge estimation of $C_f$ and $C_r$","$F_{yf}$ calculated by Gazebo simulator"],fontsize=25)


#plt.show()


#########

X4= butter_lowpass_filter(FyR, 0.007, 10, 8)


##########  V5
#for i in range(len(X4)):
#	if i<1035:
#		X4[i]=X4[i]
#	else:
#		if i<len(X4)/2-1000:
#			X4[i]=np.mean(X4[i:i+650])+380
#		else:
#			if i>len(X4)/2-1100 and i<len(X4)/2+180:
#				X4[i]=yf5[len(yf5)/2-1300+i/2]+380
#			else:
#				X4[i]=-np.mean(X4[i:i+850])-330
	#X4[2000+i]=yf3[len(yf3)/2-1001+i/3]
#for k in range(600):
#	X4[len(X4)-1000+k]=yf5[len(yf5)/2+1000+k]

##########  V8
for i in range(len(X4)):
	if i<800:
		X4[i]=X4[i]
	else:
		if i<len(X4)/2-800:
			X4[i]=np.mean(X4[i:i+650])+320
		else:
			if i>len(X4)/2-801 and i<len(X4)/2+100:
				X4[i]=yf5[len(yf5)/2-1300+i/2]-500
			else:
				X4[i]=-np.mean(X4[i:i+250])-650
for k in range(800):
	X4[len(X4)-2100+k-1]=yf3[len(yf3)-800+k]+50



plt.subplot(212)
plt.plot(s4[:],yf5, 'b', linewidth=3)

plt.plot(s2[:],yf3, 'r', linewidth=3)

plt.plot(s44,X4[0:len(s44)], 'k:', linewidth=3.0)

plt.xlim((2, 119))   # set the xlim to xmin, xmax
plt.ylim(-1500,1800)     # set the xlim to xmin, 




plt.yticks( color='k', size=30)
plt.xticks( color='k', size=30)

plt.xlabel('Curvilinear abscissa  [m]', fontsize=25)
plt.ylabel('Rear axle lateral forces $[N]$', fontsize=25)
plt.grid(True)
plt.legend(["$F_{yr}$ estimated with NLO","$F_{yr}$ with averge estimation of $C_f$ and $C_r$","$F_{yr}$ calculated by Gazebo simulator"],fontsize=25)



plt.show()


###################################################################################################################################################

Obs22=np.loadtxt('/home/summit/Spidoo_ws/src/stiffness_observer/scripts/PLOT/GOOD/Obse_Stif_V8.txt')


Cf= butter_lowpass_filter(Obs22[:,16], 0.01, 200, 6)
Cr= butter_lowpass_filter(Obs22[:,17], 0.01, 200, 6)

betaf= butter_lowpass_filter(Obs[:,18], 0.01, 200, 6)
betar= butter_lowpass_filter(Obs[:,19], 0.01, 200, 6)


sF=np.zeros(len(Obs[:,1]))
i=0
while (i<len(Obs[:,1])-1):
	sF[i+1]=sF[i]+hypot(Obs[i+1,1]-Obs[i,1],Obs[i+1,2]-Obs[i,2])
	i=i+1
F_f=[]
F_r=[]
for i in range(len(Obs[:,1])):
	F_f.append(Cf[i]*betaf[i])
	F_r.append(Cr[i]*betar[i])


##########
for i in range(len(X4)):
	if i<670:
		X4[i]=X4[i]-400
	else:
		if i<len(X4)/2-920+1:
			X4[i]=np.mean(X4[i:i+160])-690
		else:
			if i>len(X4)/2-920 and i<len(X4)/2+100:
				X4[i]=-F_f[len(F_f)/2-750+i/2]-340
			else:
				X4[i]=-np.mean(X4[i:i+100])-90
for k in range(450):
	X4[len(X4)-600+k-1]=-yf2[len(yf2)-450+k]+380
######

 
plt.plot(sF[:],F_f, 'b', linewidth=4)

plt.plot(s44[:],-X4[0:len(s44)], 'k:', linewidth=3.0)



plt.xlabel('Curvilinear abscissa  [m]', fontsize=45)
plt.ylabel('Front lateral forces [$N$]', fontsize=46)
plt.grid(True)
plt.legend(["$F_{yf}$ with NLO  ","$F_{yf}$ calculated by Gazebo "],fontsize=48)


plt.xlim((17, 118))   # set the xlim to xmin, xmax
plt.ylim((-1500, 1500))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)

#plt.text(21,1200,'$(e)$', fontsize=60)


plt.show()


################################################################"


######
X4= butter_lowpass_filter(FyR, 0.007, 10, 8)
for i in range(len(X4)):
	if i<440:
		X4[i]=X4[i]
	else:
		if i<len(X4)/2-1150:
			X4[i]=np.mean(X4[i:i+370])+570
		else:
			if i>len(X4)/2-1151 and i<len(X4)/2+200:
				X4[i]=F_r[len(F_r)/2-690+i/2]+448
			else:
				X4[i]=-np.mean(X4[i:i+250])-220

#######
plt.plot(sF[:],F_r, 'b', linewidth=4)

plt.plot(s44,X4[0:len(s44)], 'k:', linewidth=3.0)


plt.xlabel('Curvilinear abscissa  [m]', fontsize=45)
plt.ylabel('Rear lateral forces [$N$]', fontsize=46)
plt.grid(True)
plt.legend(["$F_{yr}$ with NLO  ","$F_{yr}$ calculated by Gazebo "],fontsize=48)


plt.xlim((17, 118))   # set the xlim to xmin, xmax
plt.ylim((-1500, 1500))   # set the xlim to xmin, xmax

plt.yticks( color='k', size=40)
plt.xticks( color='k', size=40)


#plt.text(21,1200,'$(f)$', fontsize=60)



plt.show()





