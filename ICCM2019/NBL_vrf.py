import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import fitting as fit
import trsMat as tM

''' loads the probeData '''
# directories
projDir = '/media/nx/Ubuntu/myproject/ICCM2019/'
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

probe = 'probe1'
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

plt.figure(figsize = (5, 6))
plt.plot(wv/11.4, z, 'ko-', linewidth = 2, label='measured')
plt.plot(xp/11.4, z, 'k--', linewidth = 2, label='logarithmic law')
plt.ylabel('z(m)')
plt.xlabel('u/u0')
plt.xlim(0.4, 1.6, 0.2)
legend = plt.legend(loc='upper left', shadow=False, fontsize='x-large')
plt.grid()
plt.show()

plt.figure(figsize = (5, 6))
plt.plot(wd - 15.52, z, 'kx-', linewidth = 2)
plt.ylabel('z(m)')
plt.xlabel('deg')
plt.xlim(-10, 4, 2)
plt.grid()
plt.show()

" 湍流强度廓线 "
TI = np.zeros((pNum,1))
for t in timeList:
    vx = probeData[0][t][probe][:,3].reshape(TIx.shape, order='C')
    vy = probeData[0][t][probe][:,4].reshape(TIy.shape, order='C')
    TI = TI + (vx * np.cos(wd_rad) + vy * np.sin(wd_rad) - wv.reshape(TI.shape, order='C'))**2
TI = (TI / tNum)**0.5 / wv.reshape(TI.shape, order='C')

plt.figure(figsize = (5, 6))
plt.plot((TI0+TI1+TI2)/3*100, z, 'ks-', linewidth = 2)
plt.ylabel('z(m)')
plt.xlabel('TI(%)')
plt.xlim(0, 12, 2)
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

v = v[3000:-2995]
t = np.linspace(0,480,v.shape[0])

plt.figure(figsize = (8, 6))
plt.plot(t, v/11.2, 'k-', linewidth = 2)
plt.ylabel('u/u0')
plt.xlabel('t(s)')
plt.xlim(0, 500, 50)
plt.ylim(0.8, 1.2, 0.2)
plt.grid()
plt.show()

" 功率谱 "
