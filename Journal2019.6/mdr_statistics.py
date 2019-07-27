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
yy = flt_seq(yy,1)
plt.plot(xx, yy, 'bs-', linewidth = 2, label='NBL-H')

xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = np.power(wcb[1][prbs[i]][:,1], 2)
    yy[i] = np.power(np.sum(temp) / temp.shape[0], 0.5)
yy = flt_seq(yy,1)
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
yy = flt_seq(yy,1)
plt.plot(xx, yy, 'bo--', linewidth = 2, label='NBL-V')
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = np.power(wcb[3][prbs[i]][:,1], 2)
    yy[i] = np.power(np.sum(temp) / temp.shape[0], 0.5)
yy = flt_seq(yy,1)
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
yy = flt_seq(yy,1)
plt.plot(xx[3:], yy[3:], 'bs-', linewidth = 2, label='NBL-H')

xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = wcb[1][prbs[i]][:,2]
    yy[i] = np.mean(temp)*2*1.665
yy = flt_seq(yy,1)
plt.plot(xx[3:], yy[3:], 'rs-', linewidth = 2, label='CBL-H')


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
        if temp[j,1]-temp[j,2]*1.665 > 0:
            ww[j,0] = temp[j,2]*1.665*2
        else:
            # ww[j,0] = temp[j,2]*1.665*2
            ww[j,0] = temp[j,2]*1.665 + temp[j,1]
    yy[i] = np.mean(ww)
yy = flt_seq(yy,1)
plt.plot(xx[3:], yy[3:], 'bo--', linewidth = 2, label='NBL-V')
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    # temp = wcb[3][prbs[i]][:,2]
    # yy[i] = np.mean(temp)*1.665 + 90
    ww = np.zeros((wcb[3][prbs[i]].shape[0],1))
    temp = wcb[3][prbs[i]]
    for j in range(wcb[3][prbs[i]].shape[0]):
        if temp[j,1]-temp[j,2]*1.665 > 0:
            ww[j,0] = temp[j,2]*1.665*2
        else:
            # ww[j,0] = temp[j,2]*1.665*2
            ww[j,0] = temp[j,2]*1.665 + temp[j,1]
    yy[i] = np.mean(ww)
yy = flt_seq(yy,1)
plt.plot(xx[3:], yy[3:], 'ro--', linewidth = 2, label='CBL-V')
plt.xlim(4.5, 12.5)
plt.ylim(75.6, 226.8)
# plt.yticks([75.6,88.2,100.8,113.4,126,138.6,151.2,163.8,176.4,189,201.6,214.2,226.8], [0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8])
plt.yticks([75.6,100.8,126,151.2,176.4,201.6,226.8], [0.6,0.8,1.0,1.2,1.4,1.6,1.8])
legend = plt.legend(loc='upper left', shadow=False, fontsize='x-large')
plt.grid()
plt.show()


# wake meandering频谱 (1) NBL,CBL
# fs = 50
# prb = 'probe9Dz'
#
# plt.figure(figsize = (8, 4))
# # cl = {0:'bo-', 1:'ro-', 2:'bo-', 3:'ro-'}
# cl = {0:'b-', 1:'r-', 2:'b-', 3:'r-'}
# lb = {0:'NBL', 1:'CBL', 2:'NBL', 3:'CBL'}
# for cn in [2,3]:
#     tNum = wcb[cn][prb].shape[0]
#     f = np.linspace(0, fs, tNum)
#     ps = abs(fft.fft(wcb[cn][prb][:,1])/63)
#     plt.semilogx(f[range(1,int(tNum/2))] * 126/11.4, ps[range(1,int(tNum/2))]/(60/12.1), cl[cn], linewidth = 1, label=lb[cn])
# plt.ylabel('Sf/T')
# plt.xlabel('f(Hz)')
# plt.xlim(1e-2, 1e2)
# legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
# plt.grid()
# plt.show()


# meandering 时历曲线
prb = 'probe5Dz'
plt.figure(figsize = (7, 4))
cl = {0:'b-', 1:'r-', 2:'b-', 3:'r-'}
lb = {0:'NBL', 1:'CBL', 2:'NBL', 3:'CBL'}
for cn in [2,3]:
    plt.plot(wcb[cn][prb][:,0]-18240, wcb[cn][prb][:,1]/63, cl[cn], linewidth = 1, label=lb[cn])
plt.xlim(0, 600)
# plt.ylim(-1.5, 1.5)
# plt.xticks([240,270,300,330,360,390,420,450,480], [240,270,300,330,360,390,420,450,480])
# plt.ylabel('wm/R')
# plt.xlabel('t(s)')
legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
plt.grid()
plt.show()

# wake meandering频谱 (2) 5,7,9D
fs = 50
cn = 2
# prbs = ['probe5Dy', 'probe7Dy', 'probe9Dy']
prbs = ['probe5Dz', 'probe7Dz', 'probe9Dz']

plt.figure(figsize = (8, 5))
cl = {0:'gold', 1:'darkorange', 2:'firebrick'} # CBL
# cl = {0:'green', 1:'darkcyan', 2:'blue'} # NBL
ls = {0:'-.', 1:'--', 2:'-'}
lso = {0:'o', 1:'s', 2:'D'}
lb = {0:'5D', 1:'7D', 2:'9D'}
for i in [0,1,2]:
    tNum = wcb[cn][prbs[i]].shape[0]
    f = np.linspace(0, fs, tNum)[range(1,int(tNum/2))]
    ps = abs(fft.fft(wcb[cn][prbs[i]][:,1]))[range(1,int(tNum/2))]
    plt.semilogx(f * 126/11.4, ps / (126*60/12.1), color=cl[i], linestyle=ls[i], linewidth=1, label=lb[i])
    # rk = np.argsort(-ps)
    # pks = np.zeros((6,2))
    # for r in range(6):
    #     pks[r,0] = f[where(rk==r)]
    #     pks[r,1] = ps[where(rk==r)]
    rNum = 5
    pks = np.zeros((rNum,2))
    psr = np.sort(ps)
    for r in range(rNum):
        pks[r:,1] = psr[-r-1]
        pks[r:,0] = f[np.where(ps==psr[-r-1])]
    plt.scatter(pks[:,0] * 126/11.4, pks[:,1] / (126*60/12.1), color=cl[i], marker=lso[i])
plt.ylabel('Sf/T')
plt.xlabel('f(Hz)')
plt.xlim(1e-2, 1e1)
legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
plt.grid()
plt.show()
