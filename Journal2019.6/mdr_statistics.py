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
cn = 0

probeData = {} # original probeDataDict of all cases

f = open(projDir + 'postProcessing_all/data.org/' + case[cn] + '_probeData', 'rb')
probeData[cn] = pickle.load(f) # all wake information of the case
f.close()
''' end '''

probes = ['probe-3Dy', 'probe-3Dz', 'probe2Dy', 'probe2Dz', 'probe3Dy', 'probe3Dz', 'probe4Dy', 'probe4Dz', 'probe5Dy', 'probe5Dz',
          'probe6Dy', 'probe6Dz', 'probe7Dy', 'probe7Dz', 'probe8Dy', 'probe8Dz', 'probe9Dy', 'probe9Dz', 'probe10Dy', 'probe10Dz',
          'probe11Dy', 'probe11Dz', 'probe12Dy', 'probe12Dz']
# wd = {0:-1.768, 1:40.896, 2:-41.115} # 三个算例在4D位置的时均wake deflection
# wd = {0:3.742, 1:58.423, 2:-48.857} # 三个算例在7D位置的时均wake deflection
# wd = {0:8.515, 1:64.777, 2:-55.987} # 三个算例在10D位置的时均wake deflection

''' meandering幅度均方根分布 nz '''
sec = 'PlaneZ'

prbs = ['probe2Dy', 'probe3Dy', 'probe4Dy', 'probe5Dy',
        'probe6Dy', 'probe7Dy', 'probe8Dy', 'probe9Dy', 'probe10Dy',
        'probe11Dy', 'probe12Dy']
timeList = {}
tNum = {}

timeList[cn] = list(probeData[cn][prbs[0]].keys())
timeList[cn].sort()
tNum[cn] = len(timeList[cn])

wcb = {}
wc_ave = {}


prbData_ft = {}

prbData_ft[cn] = {}
for prb in prbs:
    prbData_ft[cn][prb] = np.zeros((tNum[cn],probeData[cn][prb][timeList[cn][0]].shape[0]))
    for i in range(tNum[cn]):
        prbData_ft[cn][prb][i,:] = tM.trs(probeData[cn][prb][timeList[cn][i]])[:,3]
        # 出去坏点
        nulindex = where(prbData_ft[cn][prb][i,:] < -100)
        prbData_ft[cn][prb][i,:][nulindex] = 11.4
    for j in range(prbData_ft[cn][prb].shape[1]):
        prbData_ft[cn][prb][:,j] = flt_seq(prbData_ft[cn][prb][:,j],75)

p = tM.trs(probeData[cn][prbs[0]][timeList[cn][0]])[:,1]

# 读取 wc_ave
wc_ave_org = {}
f = open(projDir + 'postProcessing_all/data.processed/' + case[cn] + '_' + sec + '_wc_ave', 'rb')
wc_ave_org[cn] = pickle.load(f) # all wake information of the case
f.close()
wc_ave[cn] = {}
for i in range(2,13):
    wc_ave[cn][prbs[i-2]] = wc_ave_org[cn][i*126-1,1] # 根据具体情况调整


wcb[cn] = {}
for prb in prbs:
    wcb[cn][prb] = np.zeros((tNum[cn],3))
    wcb[cn][prb][:,0] = np.linspace(float(timeList[cn][0]), float(timeList[cn][-1]), tNum[cn])
    for i in range(tNum[cn]): # prbData_ft[cn][prb].shape[0]
        vd = 1 - prbData_ft[cn][prb][i,:]/11.4
        vd[where(vd<0)] = 0 # 拟合之前先要尽量排除尾流外的大气结构的影响!
        # fitting
        miu, sgm = ft.fit_gs((0,30),p[7:45],vd[7:45])
        wcb[cn][prb][i,1] = miu - wc_ave[cn][prb]
        wcb[cn][prb][i,2] = sgm

''' save wcb into a file with pickle '''
import pickle
f = open(projDir + 'postProcessing_all/data.processed/' + case[cn] + '_wcb.nz', 'wb')
pickle.dump(wcb[cn], f)
f.close()

# # 读取 wcb
# f = open(projDir + 'postProcessing_all/data.processed/' + case[cn] + '_wcb.nz', 'rb')
# wcb[cn] = pickle.load(f) # all wake information of the case
# f.close()

''' meandering幅度均方根分布 ny '''
sec = 'PlaneY'

prbs = ['probe2Dz', 'probe3Dz', 'probe4Dz', 'probe5Dz',
        'probe6Dz', 'probe7Dz', 'probe8Dz', 'probe9Dz', 'probe10Dz',
        'probe11Dz', 'probe12Dz']
timeList = {}
tNum = {}

timeList[cn] = list(probeData[cn][prbs[0]].keys())
timeList[cn].sort()
tNum[cn] = len(timeList[cn])

wcb = {}
wc_ave = {}


prbData_ft = {}

prbData_ft[cn] = {}
for prb in prbs:
    prbData_ft[cn][prb] = np.zeros((tNum[cn],probeData[cn][prb][timeList[cn][0]].shape[0]))
    for i in range(tNum[cn]):
        prbData_ft[cn][prb][i,:] = tM.trs(probeData[cn][prb][timeList[cn][i]])[:,3]
        # # 出去坏点
        # nulindex = where(prbData_ft[cn][prb][i,:] < -100)
        # prbData_ft[cn][prb][i,:][nulindex] = 11.4
    for j in range(prbData_ft[cn][prb].shape[1]):
        prbData_ft[cn][prb][:,j] = flt_seq(prbData_ft[cn][prb][:,j],75)

p = tM.trs(probeData[cn][prbs[0]][timeList[cn][0]])[:,2]

# 读取 wc_ave
wc_ave_org = {}
f = open(projDir + 'postProcessing_all/data.processed/' + case[cn] + '_' + sec + '_wc_ave', 'rb')
wc_ave_org[cn] = pickle.load(f) # all wake information of the case
f.close()
wc_ave[cn] = {}
for i in range(2,13):
    wc_ave[cn][prbs[i-2]] = wc_ave_org[cn][i*126-1,1] # 根据具体情况调整

wcb[cn] = {}
u0 = np.zeros((prbData_ft[cn][prb][0,:].shape))
for i in range(u0.shape[0]):
    u0[i] = u0_org[int(p[i])]

for prb in prbs:
    wcb[cn][prb] = np.zeros((tNum[cn],3))
    wcb[cn][prb][:,0] = np.linspace(float(timeList[cn][0]), float(timeList[cn][-1]), tNum[cn])
    for i in range(tNum[cn]): # prbData_ft[cn][prb].shape[0]
        vd = 1 - prbData_ft[cn][prb][i,:]/u0
        vd[where(vd<0)] = 0 # 拟合之前先要尽量排除尾流外的大气结构的影响!
        # fitting
        miu, sgm = ft.fit_gs((0,30),p,vd)
        wcb[cn][prb][i,1] = miu - wc_ave[cn][prb]
        wcb[cn][prb][i,2] = sgm


''' save wcb into a file with pickle '''
import pickle
f = open(projDir + 'postProcessing_all/data.processed/' + case[cn] + '_wcb.ny', 'wb')
pickle.dump(wcb[cn], f)
f.close()
# # 读取 wcb
# wc_ave_org = {}
# f = open(projDir + 'postProcessing_all/data.processed/' + case[cn] + '_wcb.ny', 'rb')
# wc_ave_org[cn] = pickle.load(f) # all wake information of the case
# f.close()

''' meandering 均方根曲线 '''
plt.figure(figsize = (10, 6))
cn = 0
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = np.power(wcb[cn][prbs[i]][:,1], 2)
    yy[i] = np.power(np.sum(temp) / temp.shape[0], 0.5)
plt.plot(xx, yy, 'bs-', linewidth = 2, label='NBL')
cn = 1
xx = [i for i in range(2,13)]
yy = np.zeros((len(xx),1))
for i in range(len(xx)):
    temp = np.power(wcb[cn][prbs[i]][:,1], 2)
    yy[i] = np.power(np.sum(temp) / temp.shape[0], 0.5)
plt.plot(xx, yy, 'rs-', linewidth = 2, label='CBL')
plt.xlim(0, 14)
# plt.ylim(-1.5, 1.5)
# plt.xticks([240,270,300,330,360,390,420,450,480], [240,270,300,330,360,390,420,450,480])
# plt.ylabel('wm/R')
# plt.xlabel('t(s)')
legend = plt.legend(loc='upper left', shadow=False, fontsize='x-large')
plt.grid()
plt.show()








# meandering 时历曲线
prb = prbs[10]
plt.figure(figsize = (10, 6))
plt.plot(wc[1][prb][:,0]-18240, wc[1][prb][:,1]/63, 'r-', linewidth = 1, label='CBL')
plt.xlim(0, 600)
# plt.ylim(-1.5, 1.5)
# plt.xticks([240,270,300,330,360,390,420,450,480], [240,270,300,330,360,390,420,450,480])
# plt.ylabel('wm/R')
# plt.xlabel('t(s)')
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
