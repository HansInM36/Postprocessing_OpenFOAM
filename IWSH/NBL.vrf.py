import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
import fitting as fit

projDir = '/home/rao/myproject/IWSH2019/'

''' load original wake data '''
caseName = {0:'NBL.prec.newdomain.56cores'}

secList = ['Sec0','Sec6','Sec11']

wakeDataDict = {} # 存储所有的原始尾流信息

wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_ave = {} # 求出所有 case 中尾流的时均值并存入该字典
wake_TI = {} # 求出所有 case 中尾流的湍流强度并存入该字典
ave = {} # wake_ave 的网格化版本
TI = {} # wake_ave 的网格化版本

''' assemble all the data of different secs in wakeDataDict '''
secDataDict = {}
for sec in secList:
    f = open(projDir + 'postProcessing_all/' + caseName[0] + '_' + sec + '_wakeData', 'rb')
    secDataDict[sec] = pickle.load(f) # all wake information of the case
    f.close()
timeList = list(secDataDict[secList[0]].keys())
for time in timeList:
    for sec in secList:
        wakeDataDict[time] = {}
for time in timeList:
    t0 = secDataDict['Sec0'][time]['Sec0']
    t1 = secDataDict['Sec6'][time]['Sec6']
    t2 = secDataDict['Sec11'][time]['Sec11']
    wakeDataDict[time]['Sec0'] = np.delete(t0, np.where(t0[:,1]!=376), axis=0)
    wakeDataDict[time]['Sec6'] = np.delete(t1, np.where(t1[:,1]!=1008), axis=0)
    wakeDataDict[time]['Sec11'] = np.delete(t2, np.where(t2[:,1]!=1640), axis=0)

wake = Wake(wakeDataDict)
wake_ave = wake.ave_wakeData() # wake_ave is a dict containing the average data of the wake
wake_TI = wake.intensity()

secData_ave = {}
secData_TI = {}

secData_ave = dict(zip(wake.secList, wake.secList))
secData_TI = dict(zip(wake.secList, wake.secList))
for sec in secData_ave.keys():
    secData_ave[sec] = WakeSec(wake_ave[sec])
    secData_TI[sec] = WakeSec(wake_TI[sec])
    secData_ave[sec].meshITP_Nx((0, 800, 400), (0, 800, 400))
    secData_TI[sec].meshITP_Nx((0, 800, 400), (0, 800, 400))

''' Vx vertical profile '''
# data for Vx profile
x0 = secData_ave['Sec0'].y_cut(400)['Vx']
y0 = secData_ave['Sec0'].y_cut(400)['z']
x1 = secData_ave['Sec6'].y_cut(400)['Vx']
y1 = secData_ave['Sec6'].y_cut(400)['z']
x2 = secData_ave['Sec11'].y_cut(400)['Vx']
y2 = secData_ave['Sec11'].y_cut(400)['z']
x = np.ravel((x0+x1+x2)/3)
y = np.ravel((y0+y1+y2)/3)
pp = fit.fit_ABL(0.7,0.4,0.15,y,x)
xp = fit.func_ABL(pp,0.4,0.15,y)
y = y/0.15
xp = xp*0.4/pp
x = x*0.4/pp
# data for TI profile
x3 = secData_TI['Sec0'].y_cut(400)['Vx']*100
y3 = secData_TI['Sec0'].y_cut(400)['z']
x4 = secData_TI['Sec6'].y_cut(400)['Vx']*100
y4 = secData_TI['Sec6'].y_cut(400)['z']
x5 = secData_TI['Sec11'].y_cut(400)['Vx']*100
y5 = secData_TI['Sec11'].y_cut(400)['z']

# Vx profile and TIx profile 画在一张图
from pylab import mpl
from matplotlib.gridspec import GridSpec
fig = plt.figure(1, figsize=(12, 6))
fig.subplots_adjust(bottom=0.2)
ax = {}
gs = GridSpec(1,3)
ax[0] = plt.subplot(gs[0, 0])
ax[1] = plt.subplot(gs[0, 1])
ax[2] = plt.subplot(gs[0, 2])
ax[0].plot(x0[::10], y0[::10], 'ro-', linewidth=1, label='x=3D')
ax[0].plot(x1[::10], y1[::10], 'bo-', linewidth=1, label='x=8D')
ax[0].plot(x2[::10], y2[::10], 'go-', linewidth=1, label='x=13D')
ax[1].semilogy(xp[::10], y[::10], 'k-', linewidth=1, label='logarithmic law')
ax[1].semilogy(x[::10], y[::10], 'ks', linewidth=1, label='measured')
ax[2].plot(x3[::10], y3[::10], 'r*-', linewidth=1, label='x=3D')
ax[2].plot(x4[::10], y4[::10], 'b*-', linewidth=1, label='x=8D')
ax[2].plot(x5[::10], y5[::10], 'g*-', linewidth=1, label='x=13D')
ax[0].set_ylabel('z(m)')
ax[0].set_xlabel('Vx(m/s)')
ax[0].set_xlim(0, 20, 0.5)
ax[0].set_ylim(0, 850, 100)
ax[1].set_ylabel('z/z0')
# ax[1].set_xlabel()
ax[1].set_xlim(0, 20)
ax[1].set_ylim(0, 8000)
ax[2].set_ylabel('z(m)')
ax[2].set_xlabel('ITx')
ax[2].set_xlim(0, 60, 1.5)
ax[2].set_ylim(0, 850, 100)
legend = ax[0].legend(loc='upper left', fontsize=12)
ax[0].grid()
legend = ax[1].legend(loc='lower right', fontsize=12)
legend = ax[2].legend(loc='upper right', fontsize=12)
ax[2].grid()
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()
