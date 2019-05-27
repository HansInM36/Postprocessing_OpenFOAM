import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

projDir = '/media/nx/Ubuntu1/myproject/IWSH/'

''' load original wake data '''
caseName = {0:'uniIn', 1:'turbIn-0.2', 2:'NBL.succ.newdomain.56cores'}

sec = 'PlaneZ'

x = {}
y = {}
z = {}

''' 读入 case2 的信息 '''
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
secData = {}

''' assemble all the data of different secs in wakeDataDict '''
wakeDataDict = {} # 存储所有的原始尾流信息
f = open(projDir + 'postProcessing_all/' + caseName[2] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()
timeList = list(wakeData_org.keys())
for time in timeList:
    t1 = wakeData_org[time][sec]
    wakeDataDict[time] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
del wakeData_org # 汇总完了删除这个临时字典
wakeSec = Sec(wakeDataDict)
del wakeDataDict

ttDict = {0:'18207.5', 1:'18235', 2:'18262.5', 3:'18290'}
for tt in [0,1,2,3]:
    secData[tt] = wakeSec.fSec_t(6, ttDict[tt])
    secData[tt] = SecITP(secData[tt])
    secData[tt].meshITP_Nz((0, 2016, 1008), (0, 800, 400))

''' Vx contour for PlaneZ'''
for tt in [0,1,2,3]:
    sec = 'PlaneZ'
    dx, dy = 2, 2
    y[tt], x[tt] = np.mgrid[slice(0, 2016 + dy, dy),
                    slice(0, 800 + dx, dx)]
    y[tt] = y[tt].T
    x[tt] = x[tt].T
    z[tt] = np.array(zeros(shape(x[tt])))
    for row in secData[tt].meshData:
        i = int(row[0,1]/dx) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
        j = int(row[0,0]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
        z[tt][i,j] = row[0,3] # row[0,4] for ALMsolver; row[0,3] for SOWFA
    z[tt] = z[tt][:-1, :-1]

zbp = z.copy() # back up
xbp = x.copy() # back up
ybp = y.copy() # back up
x = xbp.copy()
y = ybp.copy()
z = zbp.copy()

for i in [0,1,2,3]:
    x[i] = x[i][74:326,188:]
    y[i] = y[i][74:326,188:]
    z[i] = z[i][74:325,188:]
    z[i] = z[i] / 11.4

min, max = 4/11.4, 12/11.4
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
for i in [0,1,2,3]:
    z[i][where(z[i]>max)] = max
    z[i][where(z[i]<min)] = min

cmap = plt.get_cmap('magma') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4)

for i in [ax0, ax1, ax2, ax3]:
    i.set_xticks([376, 628, 880, 1132, 1384, 1636, 1888])
    i.set_xticklabels(['0D', '2D', '4D', '6D', '8D', '10D', '12D'])
    i.set_yticks([148, 274, 400, 526, 650])
    i.set_yticklabels(['-2D', '-1D', '0D', '1D', '2D'])

cf = ax0.contourf(y[0][:-1, :-1] + dx/2.,
                  x[0][:-1, :-1] + dy/2., z[0], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax0)

cf = ax1.contourf(y[1][:-1, :-1] + dx/2.,
                  x[1][:-1, :-1] + dy/2., z[1], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax1)

cf = ax2.contourf(y[2][:-1, :-1] + dx/2.,
                  x[2][:-1, :-1] + dy/2., z[2], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax2)
cf = ax3.contourf(y[3][:-1, :-1] + dx/2.,
                  x[3][:-1, :-1] + dy/2., z[3], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax3)



''' 计算尾流中心 '''
for tt in [0,1,2,3]: # 使x，y，z三个矩阵维数一致，并将拟合范围缩小至以轮毂中心左右1D范围，以排除大气低速气团的影响
    x[tt] = x[tt][:-1,:-1]
    y[tt] = y[tt][:-1,:-1]
    x[tt] = x[tt][79:174,:]
    y[tt] = y[tt][79:174,:]
    z[tt] = z[tt][79:174,:]

import fitting as ft
wc = {}

for tt in [0,1,2,3]:
    wc[tt] = np.array(zeros((y[tt][0].shape[0],2)))
    for j in range(y[tt][0].shape[0]):
        p = x[tt][:,j]
        vd = z[tt][:,j]
        vd = 1 - vd
        cp = ft.fit_gs((400,20),p,vd)[0]
        wc[tt][j,0] = y[tt][0,j]
        wc[tt][j,1] = cp

# 检测fit_gs函数的正确性, 顺便也能做某截面的拟合图像
# p = x[2][:,252]
# vd = z[2][:,252]
# vd = 1 - vd/11.4
# cp = ft.fit_gs((400,20),p,vd)
# xx = p
# yy = vd
# delta = (np.max(xx) - np.min(xx)) / (np.shape(xx)[0] - 1)
# S = sum(yy)*delta - 0.5*(yy[np.where(xx==np.min(xx))] + yy[np.where(xx==np.max(xx))])
# yyp = ft.func_gs(cp,xx)*S
# plt.figure(figsize = (8, 4))
# plt.plot(xx, yy, 'ro-', linewidth = 1, label='velocity deficit')
# plt.plot(xx, yyp, 'b-', linewidth = 1, label='gaussian fitting curve')
# plt.xlabel('r/R')
# plt.ylabel('1-Vx/V0')
# plt.ylim(-0.1,0.4,0.1)
# plt.xlim(274,526,63)
# plt.xticks([274,337,400,463,526],['-2','-1','0','1','2'])
# legend = plt.legend(loc='upper right', shadow=False, fontsize=10)
# plt.grid()
# plt.show()

ax0.plot(wc[0][:,0], wc[0][:,1], 'k-', linewidth = 2)
ax0.set_xlim(376, 2016)
ax1.plot(wc[1][:,0], wc[1][:,1], 'k-', linewidth = 2)
ax1.set_xlim(376, 2016)
ax2.plot(wc[2][:,0], wc[2][:,1], 'k-', linewidth = 2)
ax2.set_xlim(376, 2016)
ax3.plot(wc[3][:,0], wc[3][:,1], 'k-', linewidth = 2)
ax3.set_xlim(376, 2016)

fig.tight_layout()
plt.show()

import signalClass as sgn
seqorg = {}
seq = {}
wp = {}
k = {}
for i in [0,1,2,3]:
    seqorg[i] = wc[i][126:,1] - 400
    seqorg[i] = seqorg[i] - mean(seqorg[i])
    seq[i] = sgn.SignalSeq(seqorg[i])
    k[i] = seq[i].SE_s(2)[0,:]
    wp[i] = seq[i].SE_s(2)[1,:]
plt.plot(wc[1][126:,0], seqorg[1], 'r-', linewidth = 1)
plt.show()
plt.semilogx(k[0][1:]*126, wp[0][1:]/126**2, 'g:', linewidth = 1, label='t=18207.5s')
plt.semilogx(k[1][1:]*126, wp[1][1:]/126**2, 'b-.', linewidth = 1, label='t=18235s')
plt.semilogx(k[2][1:]*126, wp[2][1:]/126**2, 'r--', linewidth = 1, label='t=18262.5s')
plt.semilogx(k[3][1:]*126, wp[3][1:]/126**2, 'y-', linewidth = 1, label='t=18290s')
plt.xlim(0.1,1000)
legend = plt.legend(loc='upper right', shadow=False, fontsize=10)
plt.grid()
plt.show()

kmax = {}
for i in [0,1,2,3]:
    kmax[i] = k[i][where(wp[i]==np.max(wp[i]))[0][0]]
