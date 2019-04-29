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

projDir = '/home/rao/myproject/IWSH2019/'

''' load original wake data '''
caseName = {0:'uniIn', 1:'turbIn-0.1', 2:'turbIn-0.2', 3:'NBL.succ.newdomain.56cores'}

secList = ['PlaneY', 'PlaneZ']

wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_ave = {} # 求出所有 case 中尾流的时均值并存入该字典
wake_TI = {} # 求出所有 case 中尾流的湍流强度并存入该字典
ave = {} # wake_ave 的网格化版本
TI = {} # wake_ave 的网格化版本

''' assemble all the data of different secs in wakeDataDict (ALMsolver)'''
wakeDataDict = {} # 存储所有的原始尾流信息
secDataDict = {}
for sec in secList:
    f = open(projDir + 'postProcessing_all/' + caseName[3] + '_' + sec + '_wakeData', 'rb')
    secDataDict[sec] = pickle.load(f) # all wake information of the case
    f.close()
timeList = list(secDataDict[secList[0]].keys())
for time in timeList:
    for sec in secList:
        wakeDataDict[time] = {}
for time in timeList:
    t0 = secDataDict['PlaneY'][time]['PlaneY']
    t1 = secDataDict['PlaneZ'][time]['PlaneZ']
    wakeDataDict[time]['PlaneY'] = np.delete(t0, np.where(t0[:,1]==99999), axis=0)
    wakeDataDict[time]['PlaneZ'] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
del secDataDict

''' assemble all the data of different secs in wakeDataDict (SOWFA)'''
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
    t0 = secDataDict['PlaneY'][time]['PlaneY']
    t1 = secDataDict['PlaneZ'][time]['PlaneZ']
    wakeDataDict[time]['PlaneY'] = np.delete(t0, np.where(t0[:,2]!=400.1), axis=0)
    wakeDataDict[time]['PlaneZ'] = np.delete(t1, np.where(t1[:,3]!=90.1), axis=0)
del secDataDict


case = 3
# del wakeDataDict['300'] # 不知为何300s的数据行数与其他时间点不匹配
wake[case] = Wake(wakeDataDict) # 记录case0信息后，重新回到上方录入case1的信息，以此类推，完成wake字典的初始化
wake_ave[case] = wake[case].ave_wakeData() # wake_ave is a dict containing the average data of the wake
# wake_TI[case] = wake[case].intensity()

secData_ave = {}
# secData_TI = {}

case = 3
secData_ave[case] = dict(zip(wake[case].secList, wake[case].secList))
# secData_TI[case] = dict(zip(wake[case].secList, wake[case].secList))
sec = 'PlaneY'
secData_ave[case][sec] = WakeSec(wake_ave[case][sec])
# secData_TI[case][sec] = WakeSec(wake_TI[case][sec])
secData_ave[case][sec].meshITP_Ny((0, 2016, 1008), (0, 800, 400))
# secData_TI[case][sec].meshITP_Ny((0, 2016, 1008), (0, 800, 400))
sec = 'PlaneZ'
secData_ave[case][sec] = WakeSec(wake_ave[case][sec])
# secData_TI[case][sec] = WakeSec(wake_TI[case][sec])
secData_ave[case][sec].meshITP_Nz((0, 2016, 1008), (0, 800, 400))
# secData_TI[case][sec].meshITP_Nz((0, 2016, 1008), (0, 800, 400))

''' Vx contour for PlaneZ'''
case = 3
sec = 'PlaneZ'
dx, dy = 2, 2
y, x = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y = y.T
x = x.T
z = np.array(zeros(shape(x)))
for row in secData_ave[case][sec].meshData:
    i = int(row[0,1]/dx) # i = int(row[0,0]/dx) for ALMsolver
    j = int(row[0,0]/dy) # j = int(row[0,1]/dy) for ALMsolver
    z[i,j] = row[0,4]
z = z[:-1, :-1]

levels = MaxNLocator(nbins=40).tick_values(4, 12)
cmap = plt.get_cmap('rainbow')
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4)

cf = ax3.contourf(y[:-1, :-1] + dx/2.,
                  x[:-1, :-1] + dy/2., z, levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax3)

# ax0.set_title('Vx profile for PlaneZ')

fig.tight_layout()
plt.show()
