import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import fitting as fit
import trsMat as tM
import signalClass as sgn
import wakeDataClass as wdc

''' loads the probeData '''
# directories
projDir = '/home/rao/myproject/Journal2019.6/'
case = {0:'NBL', 1:'CBL'}

probeData = {} # original probeDataDict of all cases
for cn in range(2):
    f = open(projDir + 'postProcessing_all/data.org/' + case[cn] + '_probeData', 'rb')
    probeData[cn] = pickle.load(f) # all wake information of the case
    f.close()
''' end '''

wd = 15.52*np.pi/180

probeList = ['probe0', 'probe1', 'probe2']

wv = {}
wd = {}
" 平均风速风向廓线 "
for cn in range(2):
    wv_ave = 0
    wd_ave = 0
    for probe in probeList:
        timeList = list(probeData[cn][probe].keys())
        timeList.sort()
        tNum = len(timeList)

        pNum = np.shape(probeData[cn][probe][timeList[0]])[0]

        vx_ave = np.zeros((pNum,1))
        vy_ave = np.zeros((pNum,1))
        vz_ave = np.zeros((pNum,1))
        for t in timeList:
            vx_ave = vx_ave + probeData[cn][probe][t][:,3].reshape(vx_ave.shape, order='C')
            vy_ave = vy_ave + probeData[cn][probe][t][:,4].reshape(vy_ave.shape, order='C')
            vz_ave = vz_ave + probeData[cn][probe][t][:,5].reshape(vz_ave.shape, order='C')
        vx_ave = vx_ave / tNum
        vy_ave = vy_ave / tNum
        vz_ave = vz_ave / tNum
        wd_ave += np.arcsin(vy_ave/vx_ave)
        wv_ave += (vx_ave**2 + vy_ave**2)**0.5
    wd[cn] = wd_ave / len(probeList)
    wv[cn] = wv_ave / len(probeList)

z = probeData[cn][probeList[0]][timeList[0]][:,2].reshape(vx_ave.shape, order='C')
# 拟合大气边界普朗特层对数率
z = z.reshape((z.shape[0]), order='C')
for cn in range(2):
    wv[cn] = wv[cn].reshape((wv[cn].shape[0]), order='C')
# pp = fit.fit_ABL(0.7,0.4,0.001,z[:13],wv[:13]) # u*=0.4075
# xp = fit.func_ABL(pp,0.4,0.001,z)


plt.figure(figsize = (6, 6))
plt.plot(wv[0]/11.35, z, 'bo-', linewidth = 2, label='NBL')
plt.plot(wv[1]/11.35, z, 'ro-', linewidth = 2, label='CBL')
# plt.plot(xp/11.4, z, 'k--', linewidth = 2, label='logarithmic law')
plt.ylabel('z(m)')
plt.xlabel('u/u0')
plt.xlim(0.6, 1.2, 0.2)
plt.ylim(0, 300, 50)
legend = plt.legend(loc='upper left', shadow=False, fontsize='x-large')
plt.grid()
plt.show()

plt.figure(figsize = (6, 6))
plt.plot(wd[0]*180/np.pi - 15.52, z, 'bx-', linewidth = 2)
plt.plot(wd[1]*180/np.pi - 15.52, z, 'rx-', linewidth = 2)
plt.ylabel('z(m)')
plt.xlabel('deg')
plt.xlim(-10, 4, 2)
plt.grid()
plt.show()

" 湍流强度廓线 "
TI = {}
for cn in range(2):
    timeList = list(probeData[cn]['probe0'].keys())
    timeList.sort()
    tNum = len(timeList)
    pNum = np.shape(probeData[cn]['probe0'][timeList[0]])[0]
    TI[cn] = np.zeros((pNum,1))
    for probe in probeList:
        for t in timeList:
            vx = probeData[cn][probe][t][:,3].reshape(TI[cn].shape, order='C')
            vy = probeData[cn][probe][t][:,4].reshape(TI[cn].shape, order='C')
            TI[cn] = TI[cn] + (vx * np.cos(wd[cn]) + vy * np.sin(wd[cn]) - wv[cn].reshape(TI[cn].shape, order='C'))**2
            # TI[cn] = TI[cn] + (vx * np.cos(wd) + vy * np.sin(wd) - wv[cn].reshape(TI[cn].shape, order='C'))**2
    TI[cn] /= len(probeList)
    TI[cn] = (TI[cn] / tNum)**0.5 / wv[cn].reshape(TI[cn].shape, order='C')

plt.figure(figsize = (6, 6))
plt.plot(TI[0]*100, z, 'bs-', linewidth = 2, label='NBL')
plt.plot(TI[1]*100, z, 'rs-', linewidth = 2, label='CBL')
plt.ylabel('z(m)')
plt.xlabel('TI(%)')
plt.xlim(2, 14, 2)
# plt.ylim(0, 300, 2)
legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
plt.grid()
plt.show()

" 轮毂处速度时序 "
probeData_ = probeData # 转换坐标系
for t in timeList:
    for p in probeList:
        probeData_[0][t][p] = tM.trs(probeData[0][t][p])
v = np.zeros((tNum,1))
for i in range(tNum):
    v[i,0] = probeData_[0][timeList[i]][probe][7,3]

v = v[3000:-2996]
t = np.linspace(0,480,v.shape[0])
v = v.reshape(t.shape, order='C')


plt.figure(figsize = (8, 6))
plt.plot(t, v/11.2, 'k-', linewidth = 2)
plt.ylabel('u/u0')
plt.xlabel('t(s)')
plt.xlim(0, 500, 50)
plt.ylim(0.8, 1.2, 0.2)
plt.grid()
plt.show()

" 功率谱 "
v = v - np.mean(v)
seq = sgn.SignalSeq(v)
ps = seq.PSE_t_AM(50)
# 5/3律
x = np.linspace(0.01, 10, 2000)
y = x**(-5/3)
# Kaimal谱
n = ps[0,1:]
S = 0.4**2*105*n*90.1/11.4 / (n*(1+33*n*90.1/11.4)**(5/3))

from scipy import signal
# welch 法估计
f, p = signal.welch(v, 50, 'flattop', len(v), scaling='spectrum')
# fft 法估计
pf = np.abs(np.fft.fft(v))**2
pf = pf[:len(f)]
# periodogram 法估计
ff, pp = signal.periodogram(v, 50, 'flattop', scaling='spectrum')

num = 11000
plt.figure(figsize = (8, 6))
plt.loglog(ff[1:-num]*63/11.4, pp[1:-num]/(11.4*63)*1e3, 'k--', linewidth = 1)
plt.loglog(x, y/10000*1e3, 'k-', linewidth = 1)
plt.xlim(0.01,10)
plt.ylim(1e-12,1e1)
plt.grid()
plt.show()
