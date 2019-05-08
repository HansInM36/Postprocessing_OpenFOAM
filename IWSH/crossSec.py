import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

projDir = '/media/nx/Ubuntu/myproject/IWSH/'

''' load original wake data '''
caseName = {0:'uniIn', 1:'turbIn-0.2', 2:'NBL.succ.newdomain.56cores'}

secList = ['Sec4D','Sec6D','Sec8D','Sec10D']

''' 设置整体图像参数 '''
# 图例最大最小值及分辨率设置
min, max = 0.6, 1.4
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 图例种类
cmap = plt.get_cmap('gist_rainbow') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig, ax = plt.subplots(nrows=3, ncols=4)
# 刻度标记设置
for i in range(3):
    for j in range(4):
        ax[i,j].set_xticks([148, 274, 400, 526, 650])
        ax[i,j].set_xticklabels(['-2D', '-1D', '0D', '1D', '2D'])
        ax[i,j].set_yticks([27,90,153,216,279,342])
        ax[i,j].set_yticklabels(['-0.5D', '0D', '0.5D', '1D', '1.5D', '2D'])

''' 读入 case0 的信息 '''
case = 0
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
for sec in secList:
    wakeSec[sec] = {}

''' assemble all the data of different secs in wakeDataDict '''
for sec in secList:
    wakeDataDict = {} # 存储所有的原始尾流信息
    f = open(projDir + 'postProcessing_all/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
    wakeData_org = pickle.load(f) # all wake information of the case
    f.close()
    timeList = list(wakeData_org.keys())
    for time in timeList:
        t1 = wakeData_org[time][sec]
        wakeDataDict[time] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
    del wakeData_org # 汇总完了删除这个临时字典
    wakeSec[sec] = Sec(wakeDataDict)
    del wakeDataDict

secData = {}
for sec in secList:
    secData[sec] = wakeSec[sec].fSec_t(6,'360')
    secData[sec] = SecITP(secData[sec])
    secData[sec].meshITP_Ny((0, 800, 400), (0, 800, 400))

''' Vx contour for PlaneZ'''
y = {}
z = {}
v = {}
pmin = {}
for sec in secList:
    dy, dz = 2, 2
    y[sec], z[sec] = np.mgrid[slice(0, 800 + dy, dy),
                    slice(0, 800 + dz, dz)]
    y[sec] = y[sec].T
    z[sec] = z[sec].T
    v[sec] = np.array(zeros(shape(z[sec])))
    vmin = 999999
    for row in secData[sec].meshData:
        i = int(row[0,0]/dy) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
        j = int(row[0,2]/dz) # j = int(row[0,2]/dy) for ALMsolver; j = int(row[0,2]/dy) for SOWFA
        v[sec][j,i] = row[0,4]/11.4 # row[0,4] for ALMsolver; row[0,3] for SOWFA
        if v[sec][j,i] < vmin:
            vmin = v[sec][j,i]
            pmin[sec] = (row[0,0], row[0,2]) # row[0,0], row[0,2] for ALMsolver; row[0,1], row[0,2] for SOWFA
    v[sec] = v[sec][:-1, :-1]

vbp = v.copy() # back up
ybp = y.copy() # back up
zbp = z.copy() # back up
y = ybp.copy()
z = zbp.copy()
v = vbp.copy()

# 修剪绘制范围，限制极值
for sec in secList:
    y[sec] = y[sec][:172,74:326]
    z[sec] = z[sec][:172,74:326]
    v[sec] = v[sec][:171,74:325]
    v[sec][where(v[sec]<min)] = min
    v[sec][where(v[sec]>max)] = max

for i in range(0,4):
    cf = ax[0,i].contourf(y[secList[i]][:-1, :-1] + dy/2.,
                      z[secList[i]][:-1, :-1] + dz/2., v[secList[i]], levels=levels,
                      cmap=cmap)
    fig.colorbar(cf, ax=ax[0,i])
    # ax[0,i].plot(pmin[secList[i]][0], pmin[secList[i]][1], 'rx', linewidth = 2)
    ax[0,i].plot(400, 90, 'k+', linewidth = 2)
    ax[0,i].set_xlim(148, 652)
    ax[0,i].set_ylim(27, 342)


''' 读入 case1 的信息 '''
case = 1
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
for sec in secList:
    wakeSec[sec] = {}

''' assemble all the data of different secs in wakeDataDict '''
for sec in secList:
    wakeDataDict = {} # 存储所有的原始尾流信息
    f = open(projDir + 'postProcessing_all/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
    wakeData_org = pickle.load(f) # all wake information of the case
    f.close()
    timeList = list(wakeData_org.keys())
    for time in timeList:
        t1 = wakeData_org[time][sec]
        wakeDataDict[time] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
    del wakeData_org # 汇总完了删除这个临时字典
    wakeSec[sec] = Sec(wakeDataDict)
    del wakeDataDict

secData = {}
for sec in secList:
    secData[sec] = wakeSec[sec].fSec_t(6,'360')
    secData[sec] = SecITP(secData[sec])
    secData[sec].meshITP_Ny((0, 800, 400), (0, 800, 400))

''' Vx contour for PlaneZ'''
y = {}
z = {}
v = {}
pmin = {}
for sec in secList:
    dy, dz = 2, 2
    y[sec], z[sec] = np.mgrid[slice(0, 800 + dy, dy),
                    slice(0, 800 + dz, dz)]
    y[sec] = y[sec].T
    z[sec] = z[sec].T
    v[sec] = np.array(zeros(shape(z[sec])))
    vmin = 999999
    for row in secData[sec].meshData:
        i = int(row[0,0]/dy) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
        j = int(row[0,2]/dz) # j = int(row[0,2]/dy) for ALMsolver; j = int(row[0,2]/dy) for SOWFA
        v[sec][j,i] = row[0,4]/11.4 # row[0,4] for ALMsolver; row[0,3] for SOWFA
        if v[sec][j,i] < vmin:
            vmin = v[sec][j,i]
            pmin[sec] = (row[0,0], row[0,2]) # row[0,0], row[0,2] for ALMsolver; row[0,1], row[0,2] for SOWFA
    v[sec] = v[sec][:-1, :-1]

vbp = v.copy() # back up
ybp = y.copy() # back up
zbp = z.copy() # back up
y = ybp.copy()
z = zbp.copy()
v = vbp.copy()

# 修剪绘制范围，限制极值
for sec in secList:
    y[sec] = y[sec][:172,74:326]
    z[sec] = z[sec][:172,74:326]
    v[sec] = v[sec][:171,74:325]
    v[sec][where(v[sec]<min)] = min
    v[sec][where(v[sec]>max)] = max

for i in range(0,4):
    cf = ax[1,i].contourf(y[secList[i]][:-1, :-1] + dy/2.,
                      z[secList[i]][:-1, :-1] + dz/2., v[secList[i]], levels=levels,
                      cmap=cmap)
    fig.colorbar(cf, ax=ax[1,i])
    # ax[1,i].plot(pmin[secList[i]][0], pmin[secList[i]][1], 'rx', linewidth = 2)
    ax[1,i].plot(400, 90, 'k+', linewidth = 2)
    ax[1,i].set_xlim(148, 652)
    ax[1,i].set_ylim(27, 342)

''' 读入 case2 的信息 '''
case = 2
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
for sec in secList:
    wakeSec[sec] = {}

''' assemble all the data of different secs in wakeDataDict '''
for sec in secList:
    wakeDataDict = {} # 存储所有的原始尾流信息
    f = open(projDir + 'postProcessing_all/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
    wakeData_org = pickle.load(f) # all wake information of the case
    f.close()
    timeList = list(wakeData_org.keys())
    for time in timeList:
        t1 = wakeData_org[time][sec]
        wakeDataDict[time] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
    del wakeData_org # 汇总完了删除这个临时字典
    wakeSec[sec] = Sec(wakeDataDict)
    del wakeDataDict

secData = {}
for sec in secList:
    secData[sec] = wakeSec[sec].fSec_t(6,'18280')
    secData[sec] = SecITP(secData[sec])
    secData[sec].meshITP_Nx((0, 800, 400), (0, 800, 400))

''' Vx contour for PlaneZ'''
y = {}
z = {}
v = {}
pmin = {}
for sec in secList:
    dy, dz = 2, 2
    y[sec], z[sec] = np.mgrid[slice(0, 800 + dy, dy),
                    slice(0, 800 + dz, dz)]
    y[sec] = y[sec].T
    z[sec] = z[sec].T
    v[sec] = np.array(zeros(shape(z[sec])))
    vmin = 999999
    for row in secData[sec].meshData:
        i = int(row[0,1]/dy) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
        j = int(row[0,2]/dz) # j = int(row[0,2]/dy) for ALMsolver; j = int(row[0,2]/dy) for SOWFA
        v[sec][j,i] = row[0,3]/11.4 # row[0,4] for ALMsolver; row[0,3] for SOWFA
        if v[sec][j,i] < vmin:
            vmin = v[sec][j,i]
            pmin[sec] = (row[0,1], row[0,2]) # row[0,0], row[0,2] for ALMsolver; row[0,1], row[0,2] for SOWFA
    v[sec] = v[sec][:-1, :-1]

vbp = v.copy() # back up
ybp = y.copy() # back up
zbp = z.copy() # back up
y = ybp.copy()
z = zbp.copy()
v = vbp.copy()

# 修剪绘制范围，限制极值
for sec in secList:
    y[sec] = y[sec][:172,74:326]
    z[sec] = z[sec][:172,74:326]
    v[sec] = v[sec][:171,74:325]
    v[sec][where(v[sec]<min)] = min
    v[sec][where(v[sec]>max)] = max

for i in range(0,4):
    cf = ax[2,i].contourf(y[secList[i]][:-1, :-1] + dy/2.,
                      z[secList[i]][:-1, :-1] + dz/2., v[secList[i]], levels=levels,
                      cmap=cmap)
    fig.colorbar(cf, ax=ax[2,i])
    # ax[2,i].plot(pmin[secList[i]][0], pmin[secList[i]][1], 'rx', linewidth = 2)
    ax[2,i].plot(400, 90, 'k+', linewidth = 2)
    ax[2,i].set_xlim(148, 652)
    ax[2,i].set_ylim(27, 342)


fig.tight_layout()
plt.subplots_adjust(wspace=0.5, hspace=0.2)
plt.show()
