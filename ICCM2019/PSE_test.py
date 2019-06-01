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
projDir = '/home/rao/myproject/ICCM2019/'
case = {0:'NBL.prec.254deg.11.4.0.001'}

probeData = {} # original probeDataDict of all cases

f = open(projDir + 'postProcessing_all/' + case[0] + '_probeData', 'rb')
probeData[0] = pickle.load(f) # all wake information of the case
f.close()
''' end '''

timeList = list(probeData[0].keys())
timeList.sort()
tNum = len(timeList)

probeList = ['probe0', 'probe1', 'probe2']

pNum = np.shape(probeData[0][timeList[0]][probeList[0]])[0]

probe = 'probe0'
" 平均风速风向廓线 "
vx_ave = np.zeros((pNum,1))
vy_ave = np.zeros((pNum,1))
vz_ave = np.zeros((pNum,1))
for t in timeList:
    vx_ave = vx_ave + probeData[0][t][probe][:,3].reshape(vx_ave.shape, order='C')
    vy_ave = vy_ave + probeData[0][t][probe][:,4].reshape(vy_ave.shape, order='C')
    vz_ave = vz_ave + probeData[0][t][probe][:,5].reshape(vz_ave.shape, order='C')
vx_ave = vx_ave / tNum
vy_ave = vy_ave / tNum
vz_ave = vz_ave / tNum
wv = (vx_ave**2 + vy_ave**2)**0.5
wd_rad = np.arcsin(vy_ave/vx_ave)
wd = wd_rad * 180/np.pi
z = probeData[0][timeList[0]][probeList[0]][:,2].reshape(vx_ave.shape, order='C')
# 拟合大气边界普朗特层对数率
z = z.reshape((z.shape[0]), order='C')
wv = wv.reshape((wv.shape[0]), order='C')
pp = fit.fit_ABL(0.7,0.4,0.001,z[:13],wv[:13]) # u*=0.4075
xp = fit.func_ABL(pp,0.4,0.001,z)

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
# plt.loglog(ps[0]*63/11.4, ps[1]/(11.4*63), 'k-', linewidth = 1)
# plt.loglog(f*63/11.4, p/(11.4*63), 'r-', linewidth = 1)
plt.loglog(ff[1:-num]*63/11.4, pp[1:-num]/(11.4*63)*1e3, 'k--', linewidth = 1)
# plt.loglog(f*63/11.4, pp/(11.4*63), 'k-.', linewidth = 1)
# plt.loglog(n*90.1/11.4, S/(11.4*63), 'k--', linewidth = 1)
plt.loglog(x, y/10000*1e3, 'k-', linewidth = 1)
plt.xlim(0.01,10)
plt.ylim(1e-12,1e1)
plt.grid()
plt.show()
