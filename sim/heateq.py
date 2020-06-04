import numpy as np
import matplotlib.pyplot as plt

"""1D heat equation to be solved
dT/dt = (k/(rho*cp)) * laplacian (T) 
Initial condition T=30 deg
Boundary condition:
    T(x=0,l,t=0)=T_hot
    T(cooling points,t=0 or >t_cool)=T_cold

"""
"""Geometry"""
l   =   0.1         #m

"""Spatial grid"""
n   =   10          #nodes
dx  =   l/n         #m
x   =   np.linspace(dx/2, l-dx/2, n)

"""Temporal"""
t_final =  40    #s
dt  =   0.5         #s
t = np.arange(0, t_final, dt)

"""Material properties for Al"""
rho =   2700        #kg/m3
cp  =   897         #J/Kg.K
k   =   247         #W/m.K
alpha   =   k/(rho*cp)

"""Initial condition"""
T0  =   293.15      #30deg

"""Heat source"""
T_hot   =   313.15  #40deg

"""Cooling source"""
T_cold  =   293.15  #20deg
t_cool = 10          #time to start cooling in s   
ntc = t_cool/dt

"""Initialisation"""
T = np.ones(n)*T0
dTdt = np.empty(n)


for j in range(1,len(t)):

    plt.clf()
    for i in range(1, n-1):
        
        dTdt[i] = alpha*((T[i+1]-2*T[i]+T[i-1])/dx**2)
        
    dTdt[0] = alpha*((T[1]-2*T[0]+T_hot)/dx**2)
    dTdt[n-1] = alpha*((T_hot-2*T[n-1]+T[n-2])/dx**2)


    T = T + dTdt*dt
    
    """
    Multiple cooling and heating locations can be added
    """
    """Cooling init from start of simulation"""
    #T[5]    =   T_cold
    """Cooling init from t_cool"""
    if (j>=ntc):
        T[5] = T_cold
    
    #print(T-273.15)
    
    plt.figure(1)
    plt.plot(x,T-273.15)
    plt.axis([0, l, 0, 50])
    plt.xlabel('Distance (m)')
    plt.ylabel('Temperature (C)')
    plt.show()
    plt.pause(0.01)
