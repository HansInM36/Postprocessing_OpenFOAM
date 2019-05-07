import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

projDir = '/home/rao/myproject/IWSH2019/'

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

wakeSec[2] = Sec(wakeDataDict)
del wakeDataDict

secData[2] = wakeSec[2].fSec_t(6,'18240')
secData[2] = SecITP(secData[2])
secData[2].meshITP_Nz((0, 2016, 1008), (0, 800, 400))

''' Vx contour for PlaneZ'''
case = 2
sec = 'PlaneZ'
dx, dy = 2, 2
y[case], x[case] = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y[case] = y[case].T
x[case] = x[case].T
z[case] = np.array(zeros(shape(x[case])))
for row in secData[case].meshData:
    i = int(row[0,1]/dx) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
    j = int(row[0,0]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
    z[case][i,j] = row[0,3] # row[0,4] for ALMsolver; row[0,3] for SOWFA
z[case] = z[case][:-1, :-1]

''' 读入 case1 的信息 '''
case = 1
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
secData = {}

''' assemble all the data of different secs in wakeDataDict '''
wakeDataDict = {} # 存储所有的原始尾流信息
f = open(projDir + 'postProcessing_all/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()
timeList = list(wakeData_org.keys())
for time in timeList:
    t1 = wakeData_org[time][sec]
    wakeDataDict[time] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
del wakeData_org # 汇总完了删除这个临时字典
del wakeDataDict['300']

wakeSec[case] = Sec(wakeDataDict)
del wakeDataDict

secData[case] = wakeSec[case].fSec_t(6,'360')
secData[case] = SecITP(secData[case])
secData[case].meshITP_Nz((0, 800, 400), (0, 2016, 1008))

sec = 'PlaneZ'
dx, dy = 2, 2
y[case], x[case] = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y[case] = y[case].T
x[case] = x[case].T
z[case] = np.array(zeros(shape(x[case])))
for row in secData[case].meshData:
    i = int(row[0,0]/dx) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
    j = int(row[0,1]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
    z[case][i,j] = row[0,4] # row[0,4] for ALMsolver; row[0,3] for SOWFA
z[case] = z[case][:-1, :-1]

''' 读入 case0 的信息 '''
case = 0
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
secData = {}

''' assemble all the data of different secs in wakeDataDict '''
wakeDataDict = {} # 存储所有的原始尾流信息
f = open(projDir + 'postProcessing_all/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()
timeList = list(wakeData_org.keys())
for time in timeList:
    t1 = wakeData_org[time][sec]
    wakeDataDict[time] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
del wakeData_org # 汇总完了删除这个临时字典
del wakeDataDict['300']

wakeSec[case] = Sec(wakeDataDict)
del wakeDataDict

secData[case] = wakeSec[case].fSec_t(6,'360')
secData[case] = SecITP(secData[case])
secData[case].meshITP_Nz((0, 800, 400), (0, 2016, 1008))

sec = 'PlaneZ'
dx, dy = 2, 2
y[case], x[case] = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y[case] = y[case].T
x[case] = x[case].T
z[case] = np.array(zeros(shape(x[case])))
for row in secData[case].meshData:
    i = int(row[0,0]/dx) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
    j = int(row[0,1]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
    z[case][i,j] = row[0,4] # row[0,4] for ALMsolver; row[0,3] for SOWFA
z[case] = z[case][:-1, :-1]

zbp = z.copy() # back up
xbp = x.copy() # back up
ybp = y.copy() # back up
x = xbp.copy()
y = ybp.copy()
z = zbp.copy()

for i in [0,1,2]:
    x[i] = x[i][74:326,188:]
    y[i] = y[i][74:326,188:]
    z[i] = z[i][74:325,188:]

min, max = 4, 12
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
for i in [0,1,2]:
    z[i][where(z[i]>11.6)] = 11.6
    z[i][where(z[i]<min)] = min

cmap = plt.get_cmap('magma') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)

for i in [ax0, ax1, ax2]:
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



''' 计算尾流中心 '''
for case in [0,1,2]: # 使x，y，z三个矩阵维数一致，并将拟合范围缩小至以轮毂中心左右1D范围，以排除大气低速气团的影响
    x[case] = x[case][:-1,:-1]
    y[case] = y[case][:-1,:-1]
    x[case] = x[case][63:190,:]
    y[case] = y[case][63:190,:]
    z[case] = z[case][63:190,:]

import fitting as ft
wc = {}

case = 0
wc[case] = np.array(zeros((y[case][0].shape[0],2)))
for j in range(y[case][0].shape[0]):
    p = x[case][:,j]
    vd = z[case][:,j]
    vd = 1 - vd/11.4
    cp = ft.fit_gs((400,20),p,vd)[0]
    wc[case][j,0] = y[case][0,j]
    wc[case][j,1] = cp

case = 1
wc[case] = np.array(zeros((y[case][0].shape[0],2)))
for j in range(y[case][0].shape[0]):
    p = x[case][:,j]
    vd = z[case][:,j]
    vd = 1 - vd/11.4
    cp = ft.fit_gs((400,20),p,vd)[0]
    wc[case][j,0] = y[case][0,j]
    wc[case][j,1] = cp

case = 2
wc[case] = np.array(zeros((y[case][0].shape[0],2)))
for j in range(y[case][0].shape[0]):
    p = x[case][:,j]
    vd = z[case][:,j]
    vd = 1 - vd/11.4
    cp = ft.fit_gs((400,20),p,vd)[0]
    wc[case][j,0] = y[case][0,j]
    wc[case][j,1] = cp

# 检测fit_gs函数的正确性, 顺便也能做某截面的拟合图像
p = x[2][:,252]
vd = z[2][:,252]
vd = 1 - vd/11.4
cp = ft.fit_gs((400,20),p,vd)
xx = p
yy = vd
delta = (np.max(xx) - np.min(xx)) / (np.shape(xx)[0] - 1)
S = sum(yy)*delta - 0.5*(yy[np.where(xx==np.min(xx))] + yy[np.where(xx==np.max(xx))])
yyp = ft.func_gs(cp,xx)*S
plt.figure(figsize = (8, 4))
plt.plot(xx, yy, 'ro-', linewidth = 1, label='velocity deficit')
plt.plot(xx, yyp, 'b-', linewidth = 1, label='gaussian fitting curve')
plt.xlabel('r/R')
plt.ylabel('1-Vx/V0')
plt.ylim(-0.1,0.4,0.1)
plt.xlim(274,526,63)
plt.xticks([274,337,400,463,526],['-2','-1','0','1','2'])
legend = plt.legend(loc='upper right', shadow=False, fontsize=10)
plt.grid()
plt.show()

ax0.plot(wc[0][:,0], wc[0][:,1], 'k-', linewidth = 2)
ax0.set_xlim(376, 2016)
ax1.plot(wc[1][:,0], wc[1][:,1], 'k-', linewidth = 2)
ax1.set_xlim(376, 2016)
ax2.plot(wc[2][:,0], wc[2][:,1], 'k-', linewidth = 2)
ax2.set_xlim(376, 2016)

fig.tight_layout()
plt.show()
