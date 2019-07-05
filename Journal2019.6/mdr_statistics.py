import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import fitting as ft
import trsMat as tM
import wakeDataClass
from wakeDataClass import *

''' loads the probeData '''
# directories
projDir = '/home/rao/myproject/Journal2019.6/'
case = {0:'NBL.1T', 1:'CBL.1T'}

wcb = {}
# 读取 wcb (二维字典，一级key是probe，二级key是时刻)
f = open(projDir + 'postProcessing_all/data.processed/' + case[0] + '_wcb.nz', 'rb')
wcb[0] = pickle.load(f) # all wake information of the case
f.close()
f = open(projDir + 'postProcessing_all/data.processed/' + case[1] + '_wcb.nz', 'rb')
wcb[1] = pickle.load(f) # all wake information of the case
f.close()
f = open(projDir + 'postProcessing_all/data.processed/' + case[0] + '_wcb.ny', 'rb')
wcb[2] = pickle.load(f) # all wake information of the case
f.close()
f = open(projDir + 'postProcessing_all/data.processed/' + case[1] + '_wcb.ny', 'rb')
wcb[3] = pickle.load(f) # all wake information of the case
f.close()




''' meandering 均方根曲线 '''
plt.figure(figsize = (10, 6))

prbs = ['probe2Dy', 'probe3Dy', 'probe4Dy', 'probe5Dy',
        'probe6Dy', 'probe7Dy', 'probe8Dy', 'probe9Dy', 'probe10Dy',
        'probe11Dy', 'probe12Dy']


# for cn in [0,1]:
#     for prb in prbs:
#         for i in range(wcb[cn][prb].shape[0]):
#             if (abs(wcb[cn][prb][i,1]-0) > 1.5*126 or 1.665*wcb[cn][prb][i,2] > 2*63):
#                 np.delete(wcb[cn][prb],i,axis=0)

# 水平面
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = np.power(wcb[0][prbs[i]][:,1], 2)
    yy[i] = np.power(np.sum(temp) / temp.shape[0], 0.5)
plt.plot(xx, yy, 'bs-', linewidth = 2, label='NBL-H')

xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = np.power(wcb[1][prbs[i]][:,1], 2)
    yy[i] = np.power(np.sum(temp) / temp.shape[0], 0.5)
plt.plot(xx, yy, 'rs-', linewidth = 2, label='CBL-H')


prbs = ['probe2Dz', 'probe3Dz', 'probe4Dz', 'probe5Dz',
        'probe6Dz', 'probe7Dz', 'probe8Dz', 'probe9Dz', 'probe10Dz',
        'probe11Dz', 'probe12Dz']

# for cn in [2,3]:
#     for prb in prbs:
#         for i in range(wcb[cn][prb].shape[0]):
#             if (abs(wcb[cn][prb][i,1]-90) > 1.5*126 or 1.665*wcb[cn][prb][i,2] > 2*63):
#                 np.delete(wcb[cn][prb],i,axis=0)

# 垂直面
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = np.power(wcb[2][prbs[i]][:,1], 2)
    yy[i] = np.power(np.sum(temp) / temp.shape[0], 0.5)
plt.plot(xx, yy, 'bo--', linewidth = 2, label='NBL-V')
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = np.power(wcb[3][prbs[i]][:,1], 2)
    yy[i] = np.power(np.sum(temp) / temp.shape[0], 0.5)
plt.plot(xx, yy, 'ro--', linewidth = 2, label='CBL-V')
plt.xlim(1, 13)
# plt.xticks([240,270,300,330,360,390,420,450,480], [240,270,300,330,360,390,420,450,480])
plt.ylim(0, 63)
plt.yticks([0,12.6,25.2,37.8,50.4,63], [0.0,0.1,0.2,0.3,0.4,0.5])
legend = plt.legend(loc='upper left', shadow=False, fontsize='x-large')
plt.grid()
plt.show()


''' wake width 平均曲线 '''
plt.figure(figsize = (10, 6))

prbs = ['probe2Dy', 'probe3Dy', 'probe4Dy', 'probe5Dy',
        'probe6Dy', 'probe7Dy', 'probe8Dy', 'probe9Dy', 'probe10Dy',
        'probe11Dy', 'probe12Dy']


# for cn in [0,1]:
#     for prb in prbs:
#         for i in range(wcb[cn][prb].shape[0]):
#             if (abs(wcb[cn][prb][i,1]-0) > 1.5*126 or 1.665*wcb[cn][prb][i,2] > 2*63):
#                 np.delete(wcb[cn][prb],i,axis=0)

# 水平面
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = wcb[0][prbs[i]][:,2]
    yy[i] = np.mean(temp)*2*1.665
plt.plot(xx, yy, 'bs-', linewidth = 2, label='NBL-H')

xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = wcb[1][prbs[i]][:,2]
    yy[i] = np.mean(temp)*2*1.665
plt.plot(xx, yy, 'rs-', linewidth = 2, label='CBL-H')


prbs = ['probe2Dz', 'probe3Dz', 'probe4Dz', 'probe5Dz',
        'probe6Dz', 'probe7Dz', 'probe8Dz', 'probe9Dz', 'probe10Dz',
        'probe11Dz', 'probe12Dz']

# for cn in [2,3]:
#     for prb in prbs:
#         for i in range(wcb[cn][prb].shape[0]):
#             if (abs(wcb[cn][prb][i,1]-90) > 1.5*126 or 1.665*wcb[cn][prb][i,2] > 2*63):
#                 np.delete(wcb[cn][prb],i,axis=0)

# 垂直面
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    # temp = wcb[2][prbs[i]][:,2]
    # yy[i] = np.mean(temp)*1.665 + 90
    ww = np.zeros((wcb[2][prbs[i]].shape[0],1))
    temp = wcb[2][prbs[i]]
    for j in range(wcb[2][prbs[i]].shape[0]):
        if temp[j,1]+90-temp[j,2]*1.665 > 0:
            ww[j,0] = temp[j,2]*1.665*2
        else:
            ww[j,0] = temp[j,2]*1.665 + 90
    yy[i] = np.mean(ww)
plt.plot(xx, yy, 'bo--', linewidth = 2, label='NBL-V')
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    # temp = wcb[3][prbs[i]][:,2]
    # yy[i] = np.mean(temp)*1.665 + 90
    ww = np.zeros((wcb[3][prbs[i]].shape[0],1))
    temp = wcb[3][prbs[i]]
    for j in range(wcb[3][prbs[i]].shape[0]):
        if temp[j,1]+90-temp[j,2]*1.665 > 0:
            ww[j,0] = temp[j,2]*1.665*2
        else:
            ww[j,0] = temp[j,2]*1.665 + 90
    yy[i] = np.mean(ww)
plt.plot(xx, yy, 'ro--', linewidth = 2, label='CBL-V')
plt.xlim(1, 13)
plt.ylim(126, 252)
plt.yticks([126,157.5,189,220.5,252], [1.0,1.25,1.5,1.75,2.0])
legend = plt.legend(loc='upper left', shadow=False, fontsize='x-large')
plt.grid()
plt.show()
