import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
import fitting as fit
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

projDir = '/media/nx/Ubuntu1/myproject/IWSH/'

''' load original wake data '''
caseName = {0:'uniIn', 1:'turbIn-0.1', 2:'turbIn-0.2', 3:'NBL.succ.newdomain.56cores'}

secList = ['PlaneY']

wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_ave = {} # 求出所有 case 中尾流的时均值并存入该字典
wake_TI = {} # 求出所有 case 中尾流的湍流强度并存入该字典
ave = {} # wake_ave 的网格化版本
TI = {} # wake_ave 的网格化版本

''' assemble all the data of different secs in wakeDataDict (ALMsolver)'''
wakeDataDict = {} # 存储所有的原始尾流信息
secDataDict = {}
for sec in secList:
    f = open(projDir + 'postProcessing_all/' + caseName[2] + '_' + sec + '_wakeData', 'rb')
    secDataDict[sec] = pickle.load(f) # all wake information of the case
    f.close()
timeList = list(secDataDict[secList[0]].keys())
for time in timeList:
    for sec in secList:
        wakeDataDict[time] = {}
for time in timeList:
    t0 = secDataDict['PlaneY'][time]['PlaneY']
    wakeDataDict[time]['PlaneY'] = np.delete(t0, np.where(t0[:,2]==99999), axis=0) # t0[:,2]==99999 for ALMsolver; t0[:,2]!=400.1 for SOWFA
del secDataDict


case = 2
del wakeDataDict['300'] # 不知为何300s的数据行数与其他时间点不匹配
wake[case] = Wake(wakeDataDict) # 记录case0信息后，重新回到上方录入case1的信息，以此类推，完成wake字典的初始化
wake_ave[case] = wake[case].ave_wakeData() # wake_ave is a dict containing the average data of the wake

secData_ave = {}

case = 2
secData_ave[case] = dict(zip(wake[case].secList, wake[case].secList))
del wake
sec = 'PlaneY'
secData_ave[case][sec] = WakeSec(wake_ave[case][sec])
secData_ave[case][sec].meshITP_Nx((0, 2016, 1008), (0, 800, 400)) # x: 1008 segments 1009 points y: 400 segments 401 points
del wake_ave


''' Vx contour for PlaneZ'''
x = {}
y = {}
z = {}

case = 3
sec = 'PlaneY'
dx, dy = 2, 2
y[case], x[case] = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y[case] = y[case].T
x[case] = x[case].T
z[case] = np.array(zeros(shape(x[case])))
for row in secData_ave[case][sec].meshData:
    i = int(row[0,2]/dx) # i = int(row[0,2]/dx) for ALMsolver; i = int(row[0,2]/dx) for SOWFA
    j = int(row[0,1]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
    z[case][i,j] = row[0,4] # row[0,4] for ALMsolver; row[0,3] for SOWFA
z[case] = z[case][:-1, :-1]

zbp = z.copy() # back up
xbp = x.copy() # back up
ybp = y.copy() # back up
x = xbp.copy()
y = ybp.copy()
z = zbp.copy()


for i in range(0,4):
    x[i] = x[i][:252,188:]
    y[i] = y[i][:252,188:]
    z[i] = z[i][:251,188:]


min, max = 4, 12
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
for i in range(4):
    z[i][where(z[i]>11.6)] = 11.4
    z[i][where(z[i]<min)] = min

cmap = plt.get_cmap('hot') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig, (ax0, ax2, ax3) = plt.subplots(nrows=3)

for i in [ax0, ax2, ax3]:
    i.set_xticks([376, 628, 880, 1132, 1384, 1636, 1888])
    i.set_xticklabels(['0D', '2D', '4D', '6D', '8D', '10D', '12D'])
    i.set_yticks([90, 216, 342, 468])
    i.set_yticklabels(['0D', '1D', '2D', '3D'])

cf = ax0.contourf(y[0][:-1, :-1] + dx/2.,
                  x[0][:-1, :-1] + dy/2., z[0], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax0)
cf = ax2.contourf(y[2][:-1, :-1] + dx/2.,
                  x[2][:-1, :-1] + dy/2., z[2], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax2)
cf = ax3.contourf(y[3][:-1, :-1] + dx/2.,
                  x[3][:-1, :-1] + dy/2., z[3], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax3)

# ax0.set_title('Vx profile for PlaneZ')
fig.tight_layout()
plt.show()
