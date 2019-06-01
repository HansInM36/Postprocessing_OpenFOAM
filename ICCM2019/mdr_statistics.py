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
projDir = '/home/rao/myproject/ICCM2019/'
case = {0:'NBL.succ.254deg.11.4.0.001', 1:'NBL.succ.0.001.30', 2:'NBL.succ.0.001.m30'}

probeData = {} # original probeDataDict of all cases
for cn in range(3):
    f = open(projDir + 'postProcessing_all/' + case[cn] + '_probeData', 'rb')
    probeData[cn] = pickle.load(f) # all wake information of the case
    f.close()
''' end '''

prb = 'probe4Dy'
wd = {0:-1.768, 1:40.896, 2:-41.115} # 三个算例在4D位置的时均wake deflection
# wd = {0:3.742, 1:58.423, 2:-48.857} # 三个算例在7D位置的时均wake deflection
# wd = {0:8.515, 1:64.777, 2:-55.987} # 三个算例在10D位置的时均wake deflection

timeList = {}
tNum = {}
for cn in range(3):
    timeList[cn] = list(probeData[cn][prb].keys())
    timeList[cn].sort()
    tNum[cn] = len(timeList[cn])
    for i in range(12001,tNum[cn]): # 删掉 480s 以后的时刻
        del timeList[cn][12001]
    tNum[cn] = len(timeList[cn])

wc = {}

prbData_ft = {}
for cn in range(3):
    prbData_ft[cn] = np.zeros((tNum[cn],probeData[cn][prb]['18240.0'].shape[0]))
    for i in range(tNum[cn]):
        prbData_ft[cn][i,:] = tM.trs(probeData[cn][prb][timeList[cn][i]])[:,3]
    for j in range(prbData_ft[cn].shape[1]):
        prbData_ft[cn][:,j] = flt_seq(prbData_ft[cn][:,j],75)

p = tM.trs(probeData[cn][prb]['18240.0'])[:,1]

for cn in range(3):
    wc[cn] = np.zeros((tNum[cn],2))
    wc[cn][:,0] = np.linspace(float(timeList[cn][0]), float(timeList[cn][-1]), tNum[cn])
    for i in range(prbData_ft[cn].shape[0]):
        vd = 1 - prbData_ft[cn][i,:]/11.4
        vd[where(vd<0)] = 0 # 拟合之前先要尽量排除尾流外的大气结构的影响!
        # fitting
        cp = ft.fit_gs((0,30),p[7:45],vd[7:45])[0] - wd[cn]
        wc[cn][i,1] = cp

plt.figure(figsize = (10, 6))
plt.plot(wc[0][:,0]-18000, wc[0][:,1]/63, 'r-', linewidth = 1, label='yaw 0')
plt.plot(wc[1][:,0]-18000, wc[1][:,1]/63, 'b-', linewidth = 1, label='yaw 30')
plt.plot(wc[2][:,0]-18000, wc[2][:,1]/63, 'g-', linewidth = 1, label='yaw -30')
plt.xlim(240, 480)
plt.ylim(-1.5, 1.5)
plt.xticks([240,270,300,330,360,390,420,450,480], [240,270,300,330,360,390,420,450,480])
plt.ylabel('wm/R')
plt.xlabel('t(s)')
legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
plt.grid()
plt.show()

# 储存拟合好的wake center数据
# wc10D = wc
# wc7D = wc
# wc4D = wc

# # 检查某时刻的分布
# cn = 1
# time = '18400.0'
# i = 8000
# x = p
# y = 1 - prbData_ft[cn][i]/11.4
# y[where(y<0)] = 0
# pp = ft.fit_gs((0,30),x[7:45],y[7:45])
# cp = pp[0] - wd[cn]
# yy = ft.func_gs(pp,x)
# delta = (np.max(x) - np.min(x)) / (np.shape(x)[0] - 1)
# S = sum(y)*delta - 0.5*(y[np.where(x==np.min(x))] + y[np.where(x==np.max(x))])
# yy = yy*S
#
# plt.figure(figsize = (10, 6))
# plt.plot(x, y, 'o-', linewidth = 1)
# plt.plot(x, yy, 'o-', linewidth = 1)
# plt.grid()
# plt.show()

# wake meandering rms
rms4D = {}
rms7D = {}
rms10D = {}
for cn in range(3):
    rms4D[cn] = np.power(sum(np.power(wc4D[cn][:,1],2)) / wc4D[cn][:,1].shape[0], 0.5)
    rms7D[cn] = np.power(sum(np.power(wc7D[cn][:,1],2)) / wc7D[cn][:,1].shape[0], 0.5)
    rms10D[cn] = np.power(sum(np.power(wc10D[cn][:,1],2)) / wc10D[cn][:,1].shape[0], 0.5)

plt.figure(figsize = (10, 6))
width = 2
ind = np.linspace(width*1, width*(1+(1+3)*2), 3)  # the x locations for the groups
plt.bar(ind - width/2, [rms4D[0]/63, rms7D[0]/63, rms10D[0]/63], width, color='#FF0000', label='yaw 0')
plt.bar(ind - width/2 + width*1, [rms4D[1]/63, rms7D[1]/63, rms10D[1]/63], width, color='#0000FF', label='yaw 30')
plt.bar(ind - width/2 + width*2, [rms4D[2]/63, rms7D[2]/63, rms10D[2]/63], width, color='#008000', label='yaw -30')
plt.xticks(ind + width/2, ['4D', '7D', '10D'])
plt.yticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
legend = plt.legend(loc='upper left', shadow=False, fontsize='x-large')
plt.grid(ls='--')
plt.show()


# wake meandering频谱
fs = 50
f = {}
ps4D = {}
ps7D = {}
ps10D = {}

for cn in range(3):
    f[cn] = np.linspace(0, fs, tNum[cn])
    ps4D[cn] = abs(fft.fft(wc4D[cn][:,1]/63))
    ps7D[cn] = abs(fft.fft(wc7D[cn][:,1]/63))
    ps10D[cn] = abs(fft.fft(wc10D[cn][:,1]/63))

plt.figure(figsize = (10, 6))
cn = 0
plt.semilogx(f[cn][range(1,int(tNum[cn]/2))] * 126/11.4, ps10D[cn][range(1,int(tNum[cn]/2))]/(60/12.1), 'r-', linewidth = 1, label='yaw 0')
cn = 1
plt.semilogx(f[cn][range(1,int(tNum[cn]/2))] * 126/11.4, ps10D[cn][range(1,int(tNum[cn]/2))]/(60/12.1), 'b-', linewidth = 1, label='yaw 30')
cn = 2
plt.semilogx(f[cn][range(1,int(tNum[cn]/2))] * 126/11.4, ps10D[cn][range(1,int(tNum[cn]/2))]/(60/12.1), 'g-', linewidth = 1, label='yaw -30')
plt.xlim(1e-2, 1e2)
# plt.ylim(-1.5, 1.5)
# plt.xticks([240,270,300,330,360,390,420,450,480], [240,270,300,330,360,390,420,450,480])
plt.ylabel('Sf/T')
plt.xlabel('f(Hz)')
legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
plt.grid()
plt.show()
