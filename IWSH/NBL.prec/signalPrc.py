import numpy as np
from numpy import *
import matplotlib.pyplot as plt
import signalPrcClass
from signalPrcClass import *
import random

''' examples '''
''' temporal and spatial power spectrum '''
t = linspace(0,1,2000)
x = 7*sin(2*pi*180*t) + 2.8*sin(2*pi*390*t) + 5.1*sin(2*pi*600*t) + 4.2*sin(2*pi*900*t)
signal = SignalSeq(x)
x = signal.PSE_t_AM(2000)[0,:]
y = signal.PSE_t_AM(2000)[1,:]
plt.plot(x.T, y.T, 'r-', linewidth = 1)
plt.show()
x = signal.PSE_s_AM((2,1000))[0,:]
y = signal.PSE_s_AM((2,1000))[1,:]
plt.plot(x.T, y.T, 'r-', linewidth = 1)
plt.show()
''' 2D spatial power spectrum '''
mat = array([[random.uniform(0,100) for j in range(0,12)]for i in range(0,10)]) # creates a 2D random matrix
signal_2D = SignalMat(mat)
Z = signal_2D.PSE_2D_AM(array([[2,3000],[2,1008]]))
