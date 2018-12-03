import numpy as np
from control import *
from control.matlab import *  # MATLAB-like functions
from math import *
from scipy import signal
from scipy.integrate import odeint
#import symengine
import matplotlib.pyplot as plt

#################################################################################
# Extended Kalman Filter Functions
#################################################################################

def kalman(x0,Gamma0,u,y,Gammaalpha,Gammabeta,A,C):
    S = C.dot(Gamma0) .dot(np.transpose(C)) + Gammabeta
    Kal = Gamma0 .dot(np.transpose(C)) .dot(np.linalg.inv(S) )
    ytilde = y - C .dot(x0 )
    Gup = (np.eye(len(x0))-Kal .dot(C) ).dot(Gamma0)
    xup = x0 + Kal.dot(ytilde)
    Gamma1 = A .dot(Gup) .dot(np.transpose(A)) + Gammaalpha
    x1 = A .dot(xup) + u
    return(x1,Gamma1)


################################################################################

def get_model_A_matrix(k,Cf,Cr,vit) :
    masse       = 880
    moment      = 86.7
    a       = 0.85
    b       = 0.85
    d       = 0.5
    
    a11=-2*(Cf+Cr)/(masse*vit)
    a12=-2*(a*Cf-b*Cr)/(masse*vit)-vit
    a13=0
    a14=0
    a21=-2*(a*Cf-b*Cr)/(vit*moment)
    a22=-2*(a*a*Cf+b*b*Cr)/(vit*moment)
    a23=0
    a24=0
    a31=1
    a32=0
    a33=0
    a34=vit
    a41=0
    a42=1
    a43=k*k*vit
    a44=0


    return np.array([   [a11,a12, a13, a14],
                        [a21,a22, a23, a24],
                        [a31,a32, a33, a34],
                        [a41,a42, a43, a44]])

################################################################################
def get_model_B_matrix(Cf,Cr) :
    masse       = 880
    moment      = 86.7
    a       = 0.85
    b       = 0.85
    d       = 0.5
    b11=2*Cf/masse
    b12=2*Cr/masse
    b21=2*a*Cf/moment
    b22=-2*b*Cr/moment
    b31=0
    b32=0
    b41=0
    b42=0
    return np.array([[b11,b12],
                        [b21,b22],
                        [b31,b32],
                        [b41,b42]])
################################################################################

################################################################################
def get_slipObserver_B_matrix(Vy,Vpsi,deltaf,deltar,Vx) :
    masse       = 880
    moment      = 86.7
    a       = 0.85
    b       = 0.85
    d       = 0.5
    
    b11=-2*(Vy+a*Vpsi-Vx*deltaf)/(masse*Vx)
    b12=-2*(Vy-b*Vpsi-Vx*deltar)/(masse*Vx)
    b21=-2*(a*Vy+a*a*Vpsi-a*Vx*deltaf)/(masse*moment)
    b22=-2*(b*Vy+b*b*Vpsi-b*Vx*deltar)/(masse*moment)
    b31=0
    b32=0
    b41=0
    b42=0
    return np.array([[b11,b12],
                        [b21,b22],
                        [b31,b32],
                        [b41,b42]])

################################################################################
def get_slipObserver_A_matrix(Vx,k) :
    masse       = 880
    moment      = 86.7
    a       = 0.85
    b       = 0.85
    d       = 0.5
    
    a11=0
    a12=0
    a13=0
    a14=0
    a21=0
    a22=-Vx
    a23=0
    a24=0
    a31=1
    a32=0
    a33=0
    a34=Vx
    a41=0
    a42=1
    a43=k*k*Vx
    a44=0

    return np.array([[a11,a12, a13, a14],
                        [a21,a22, a23, a24],
                        [a31,a32, a33, a34],
                        [a41,a42, a43, a44]])
                        

################################################################################
def get_slipObserver_A2_matrix(Vx,k) :
    masse       = 880
    moment      = 86.7
    a       = 0.85
    b       = 0.85
    d       = 0.5
    
    a11=0
    a12=0
    a21=0
    a22=-Vx


    return np.array([[a11,a12],
                        [a21,a22]])

################################################################################
def get_slipObserver_B2_matrix(Vy,Vpsi,deltaf,deltar,Vx) :
    masse       = 880
    moment      = 86.7
    a       = 0.85
    b       = 0.85
    d       = 0.5
    
#    b11=-2*(Vy+a*Vpsi-Vx*deltaf)/(masse*Vx)
#    b12=-2*(Vy-b*Vpsi-Vx*deltar)/(masse*Vx)
#    b21=-2*(a*Vy+a*a*Vpsi-a*Vx*deltaf)/(masse*moment)
#    b22=-2*(b*Vy+b*b*Vpsi-b*Vx*deltar)/(masse*moment)

    b11=-2*(-deltaf)/(masse)
    b12=-2*(deltar)/(masse)
    b21=-2*(-a*deltaf)/(moment)
    b22=-2*(-b*deltar)/(moment)

    return np.array([[b11,b12],
                        [b21,b22]])
################################################################################
def SlipObserver(Ao,Bo,C,xc,xcd,Ts,Vx) :
    Do=np.zeros((1,2))
#    SysCo=signal.StateSpace(Ao,Bo,C,Do)
#    SysDi=signal.cont2discrete(SysCo,Ts,method='zoh')
#    Aod=np.array([[1,(-Vx*Ts)],[0,1]])#SysDi.A
#    Bod=np.array([[Bo[(0,0)]*Ts+(1/2)*Vx*Bo[(1,0)]*Ts*Ts,Bo[(0,1)]*Ts+(1/2)*Vx*Bo[(1,1)]*Ts*Ts],[Bo[(1,0)]*Ts,Bo[(1,1)]*Ts]])#np.array([[Bo[(0,0)]*Ts+(1/2)*Vx*Bo[(1,0)]*Ts*Ts,[Bo[(0,1)]*Ts+(1/2)*Vx*Bo[(1,1)]*Ts*Ts]],[Bo[(1,0)],Bo[(1,1)]]])#SysDi.B
#    Aod=SysDi.A
#    print Aod
#    Bod=SysDi.B
    #Cod=SysDi.C
#    P = np.array([-0.2, -0.5])
#    L = signal.place_poles(Ao, Bo, P)
#    print L
#    
    CorneringStiff=np.linalg.pinv(Bo).dot(xcd-Ao.dot(xc))
    Cf=int(abs(CorneringStiff[0,0]))
    Cr=int(abs(CorneringStiff[1,0]))
#    if abs(np.linalg.det(Bo))<=10**-50:
#        Cf=15000
#        Cr=15000
#    else:
#        CorneringStiff=np.linalg.pinv(Bo).dot(xcd-Ao.dot(xc))
#        if (abs(CorneringStiff[0,0]))>20000 or(abs(CorneringStiff[0,0]))<5000 or(abs(CorneringStiff[1,0]))>20000 or (abs(CorneringStiff[1,0]))<5000:
#            Cf=15000
#            Cr=15000
#        else:
#            Cf=int(abs(CorneringStiff[0,0]))
#            Cr=int(abs(CorneringStiff[1,0]))
    return Cf,Cr
    
    
################################################################################
def SlipModel(Vx,Vy,Vpsi,deltaf,deltar) :
    masse       = 880
    moment      = 86.7
    a       = 0.85
    b       = 0.85
    d       = 0.5
    Ac=np.array([[0,-Vx],[0,0]])#SysDi.A
    Bc=np.array([[(-2*Vy-2*a*Vpsi+2*Vx*deltaf)/(masse*Vx),(-2*Vy+2*b*Vpsi-2*Vx*deltar)/(masse*Vx)],[(-2*a*Vy-2*a*a*Vpsi+2*a*Vx*deltaf)/(moment*Vx),(2*b*Vy-2*b*b*Vpsi+2*b*Vx*deltar)/(moment*Vx)]])#SysDi.A
    G=np.array([[(-4*a*Vy-4*a*a*Vpsi+4*a*Vx*deltaf)/(masse*moment*Vx),0],[0,(-4*a*Vy-4*a*a*Vpsi+4*a*Vx*deltaf)/(masse*moment*Vx)]])  #Observer gain matrix 
    c=np.array([[(a*Vy)/moment+Vpsi/masse],[(-a*Vy)/moment+Vpsi/masse]])
    return Ac,Bc,G,c

    
################################################################################
def SlipModel2(Vx,Vy,Vpsi,deltaf,deltar,k,Gamma,Tsamp) :
    masse       = 880
    moment      = 86.7
    a       = 0.85
    b       = 0.85
    d       = 0.5
    
    Ac=np.array([[0,-Vx],[0,0]])#SysObse.A
    
    Bc1=(-2*Vy-2*a*Vpsi+2*Vx*deltaf)/(masse*Vx)
    Bc2=(-2*Vy+2*b*Vpsi-2*Vx*deltar)/(masse*Vx)
    Bc3=(-2*a*Vy-2*a*a*Vpsi+2*a*Vx*deltaf)/(moment*Vx)
    Bc4=(2*b*Vy-2*b*b*Vpsi+2*b*Vx*deltar)/(moment*Vx)
    Bc=np.array([[Bc1,Bc2],[Bc3,Bc4]])#SysObse.B
    
    print('Bc=',Bc)
    
#    G11=(4*a*Vy+4*a**2*Vpsi-4*a*Vx*deltaf)/(Vx)
#    G12=0
#    G21=0
#    G22=(4*b*Vy-4*b**2*Vpsi+4*b*Vx*deltar)/(Vx)
#    
#    G=np.array([[G11,G12],[G21,G22]]) #observer gain
#    
#
#            
#    c1=(masse*a*Vy+moment*Vpsi)
#    c2=(masse*a*Vy-moment*Vpsi)
#    c=np.array([[(c1)],[(c2)]])

    
#    J1=(masse*a)
#    J2=(moment)
#    J3=(masse*a)
#    J4=(-moment)
#    
#    
#    J=np.array([[J1,J2],[J3,J4]]) # jacobian of c vector
    
#    print k
#    print Vy
#    print Vpsi
    
#    print('c=',c)
#    
#    print('J=',J)
#    print('Bc=',Bc) 
    
#    G=J.dot(Bc)
    
    
    
#    if G[0,0]<0 and G[1,1]<0:
#        c=np.array([[(-c1)],[(-c2)]])
##        J=np.array([[-J1,-J2],[-J3,-J4]])
#        G=np.array([[-G11,-G12],[-G21,-G22]])
#    else:
#        if G[1,1]<0:
#            c=np.array([[(c1)],[(-c2)]])
##            J=np.array([[J1,J2],[-J3,-J4]])
#            G=np.array([[G11,G12],[G21,-G22]])
#        elif G[0,0]<0  :
#            c=np.array([[(-c1)],[(c2)]])
##            J=np.array([[-J1,-J2],[J3,J4]])
#            G=np.array([[-G11,G12],[G21,G22]])
#        else:
#            G=np.array([[G11,G12],[G21,G22]])
#    print('G=',G)   
    

#
#    G=np.array([[(G11),G12],[G21,(G22)]])
#    c=np.array([[(c1)],[(c2)]])

#    G11=(((-2*Vy-2*a*Vpsi+2*Vx*deltaf)**2)/(masse*Vx)+((-2*a*Vy-2*a*a*Vpsi+2*a*Vx*deltaf)**2))/(moment*Vx)
#    G21=(((-2*Vy-2*a*Vpsi+2*Vx*deltaf)*(-2*Vy+2*a*Vpsi-2*Vx*deltar))/(masse*Vx)+((2*a*Vy-2*a*a*Vpsi+2*a*Vx*deltar)*(-2*a*Vy-2*a*a*Vpsi+2*a*Vx*deltaf))/(moment*Vx))
#    G12=(((-2*Vy+2*a*Vpsi-2*Vx*deltar)*(-2*Vy-2*a*Vpsi+2*Vx*deltaf))/(masse*Vx)+((2*a*Vy-2*a*a*Vpsi+2*a*Vx*deltar)*(-2*a*Vy-2*a*a*Vpsi+2*a*Vx*deltaf))/(moment*Vx))
#    G22=(((-2*Vy+2*a*Vpsi-2*Vx*deltar)**2)/(masse*Vx)+((2*a*Vy-2*a*a*Vpsi+2*a*Vx*deltar)**2))/(moment*Vx)
    
    
    c1=Vx**0.8*(-Vy*Vy-a*a*Vpsi*Vpsi-2*a*Vpsi*Vy+2*Vx*deltaf*(Vy+a*Vpsi))
    c2=Vx**0.002*(-Vy*Vy-a*a*Vpsi*Vpsi+2*a*Vpsi*Vy+2*Vx*a*deltar*(-Vy+a*Vpsi))
    
   
    J1=Vx**0.8*(-2*Vy-2*a*Vpsi+2*Vx*deltaf)
    J2=Vx**0.8*(-2*a*a*Vpsi-2*a*Vy+2*Vx*a*deltaf)
    J3=Vx**0.002*(-2*Vy+2*a*Vpsi-2*Vx*deltar)
    J4=Vx**0.002*(-2*a*a*Vpsi+2*a*Vy+2*Vx*a*deltar)
   
    J=np.array([[J1,J2],[J3,J4]])
#    jj=np.array([[1,0],[0,0.1]])
#    J=jj.dot(J)
    co=np.array([[c1],[c2]])
#    co=jj.dot(co)
    Go=J.dot(Bc)#np.array([[(G11),G12],[G21,(G22)]])
    w, v = np.linalg.eig(Go)
    if w[0]<0 or w[1]<0:
        print('LOOOOOOOOOOOOOOxxxxxxxxxxxxxxxxxxxOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOl')

#    
#    G=J.dot(Bc) #Observer gain matrix
#    
#    print G
    
    X=np.array([[Vy],[Vpsi]])
    dGammadt=-Go.dot(Gamma)-Go.dot(np.linalg.pinv(Bc).dot(X)+co)
    dd=np.array([[1,0],[0,1]])
    if Gamma[0,0] < 0 and Gamma[1,0] < 0:
        dGammadt=-dd.dot(dGammadt)
    else:
        dGammadt=dd.dot(dGammadt)  
        
    
    Gamma=Gamma+Tsamp*dGammadt

    g=np.array([[1,0],[0,1]])
    CorneringStiff=g.dot(Gamma+co)
    Cf=CorneringStiff[0,0]#int(abs(CorneringStiff[0,0]))
    Cr=CorneringStiff[1,0]#int(abs(CorneringStiff[1,0]))
    
    print('Cf=',Cf)
    print('Cr=',Cr)

    return Cf,Cr,Gamma
################################################################################    
def SlipAngles(Vx,Vy,Vpsi,deltaf,deltar) :
    a       = 0.85
    b       = 0.85
    betaf=(Vy+a*Vpsi)/Vx-deltaf
    betar=(Vy-b*Vpsi)/Vx-deltar
#    print('betaf=',betaf*180/pi)
#    print('betar=',betar*180/pi)
    return betaf,betar
################################################################################
def ForceLater_observed(betaf,betar,Cf,Cr,k) :
    if (abs(k)>30):
        Fyf_obs       = 7000*betaf
        Fyr_obs       = 7000*betar
    else :
        Fyf_obs       = Cf*betaf
        Fyr_obs       = Cr*betar
    
    return Fyf_obs,Fyr_obs 
################################################################################
def AccAng(ay_F,ay_R) :
    l=1.7
    psidd=(ay_R-ay_F)/l
    return psidd    
    
    