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

secList = ['PlaneZ']

''' Vz contour for PlaneZ'''
x = {}
y = {}
z = {}

''' 读入case3的数据 '''
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_RS = {} # 求出所有 case 中尾流的时均值并存入该字典


''' assemble all the data of different secs in wakeDataDict '''
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
    t1 = secDataDict['PlaneZ'][time]['PlaneZ']
    wakeDataDict[time]['PlaneZ'] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
del secDataDict

case = 3
wake[case] = Wake(wakeDataDict) # 记录case0信息后，重新回到上方录入case1的信息，以此类推，完成wake字典的初始化
wake_RS[case] = wake[case].ReStr((0,1)) # wake_ave is a dict containing the average data of the wake
secData_RS = {}

case = 3
secData_RS[case] = dict(zip(wake[case].secList, wake[case].secList))
del wake
sec = 'PlaneZ'
secData_RS[case][sec] = SecITP(wake_RS[case][sec])
del wake_RS

secData_RS[case][sec].meshITP_Nz((0, 2016, 1008), (0, 800, 400)) # ((0, 800, 400), (0, 2016, 1008)) for ALMsolver; ((0, 2016, 1008), (0, 800, 400)) for SOWFA

case = 3
sec = 'PlaneZ'
dx, dy = 2, 2
y[case], x[case] = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y[case] = y[case].T
x[case] = x[case].T
z[case] = np.array(zeros(shape(x[case])))
for row in secData_RS[case][sec].meshData:
    i = int(row[0,1]/dx) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
    j = int(row[0,0]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
    z[case][i,j] = row[0,3]
z[case] = z[case][:-1, :-1]

''' 读入case2的数据 '''
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_RS = {} # 求出所有 case 中尾流的时均值并存入该字典


''' assemble all the data of different secs in wakeDataDict '''
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
    t1 = secDataDict['PlaneZ'][time]['PlaneZ']
    wakeDataDict[time]['PlaneZ'] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
del secDataDict

case = 2
del wakeDataDict['300'] # 不知为何300s的数据行数与其他时间点不匹配
wake[case] = Wake(wakeDataDict) # 记录case0信息后，重新回到上方录入case1的信息，以此类推，完成wake字典的初始化
wake_RS[case] = wake[case].ReStr((0,1)) # wake_ave is a dict containing the average data of the wake
secData_RS = {}

case = 2
secData_RS[case] = dict(zip(wake[case].secList, wake[case].secList))
del wake
sec = 'PlaneZ'
secData_RS[case][sec] = SecITP(wake_RS[case][sec])
del wake_RS

secData_RS[case][sec].meshITP_Nz((0, 800, 400), (0, 2016, 1008)) # ((0, 800, 400), (0, 2016, 1008)) for ALMsolver; ((0, 2016, 1008), (0, 800, 400)) for SOWFA

case = 2
sec = 'PlaneZ'
dx, dy = 2, 2
y[case], x[case] = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y[case] = y[case].T
x[case] = x[case].T
z[case] = np.array(zeros(shape(x[case])))
for row in secData_RS[case][sec].meshData:
    i = int(row[0,0]/dx) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
    j = int(row[0,1]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
    z[case][i,j] = row[0,3]
z[case] = z[case][:-1, :-1]

''' 读入case0的数据 '''
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_RS = {} # 求出所有 case 中尾流的时均值并存入该字典


''' assemble all the data of different secs in wakeDataDict '''
wakeDataDict = {} # 存储所有的原始尾流信息
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
    t1 = secDataDict['PlaneZ'][time]['PlaneZ']
    wakeDataDict[time]['PlaneZ'] = np.delete(t1, np.where(t1[:,3]==99999), axis=0)
del secDataDict

case = 0
del wakeDataDict['300'] # 不知为何300s的数据行数与其他时间点不匹配
wake[case] = Wake(wakeDataDict) # 记录case0信息后，重新回到上方录入case1的信息，以此类推，完成wake字典的初始化
wake_RS[case] = wake[case].ReStr((0,1)) # wake_ave is a dict containing the average data of the wake
secData_RS = {}

case = 0
secData_RS[case] = dict(zip(wake[case].secList, wake[case].secList))
del wake
sec = 'PlaneZ'
secData_RS[case][sec] = SecITP(wake_RS[case][sec])
del wake_RS

secData_RS[case][sec].meshITP_Nz((0, 800, 400), (0, 2016, 1008)) # ((0, 800, 400), (0, 2016, 1008)) for ALMsolver; ((0, 2016, 1008), (0, 800, 400)) for SOWFA

case = 0
sec = 'PlaneZ'
dx, dy = 2, 2
y[case], x[case] = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y[case] = y[case].T
x[case] = x[case].T
z[case] = np.array(zeros(shape(x[case])))
for row in secData_RS[case][sec].meshData:
    i = int(row[0,0]/dx) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
    j = int(row[0,1]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
    z[case][i,j] = row[0,3]
z[case] = z[case][:-1, :-1]

zbp = z.copy() # back up
xbp = x.copy() # back up
ybp = y.copy() # back up
x = xbp.copy()
y = ybp.copy()
z = zbp.copy()


for i in [0,2,3]:
    x[i] = x[i][74:326,188:]
    y[i] = y[i][74:326,188:]
    z[i] = z[i][74:325,188:]
    z[i] = abs(z[i]) / 11.4**2


min, max = 0, 0.004
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
for i in [0,2]:
    z[i][where(z[i]>max)] = max
    z[i][where(z[i]<min)] = min

cmap = plt.get_cmap('viridis') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig, (ax0, ax2, ax3) = plt.subplots(nrows=3)

for i in [ax0, ax2, ax3]:
    i.set_xticks([376, 628, 880, 1132, 1384, 1636, 1888])
    i.set_xticklabels(['0D', '2D', '4D', '6D', '8D', '10D', '12D'])
    i.set_yticks([148, 274, 400, 526, 650])
    i.set_yticklabels(['-2D', '-1D', '0D', '1D', '2D'])

cf = ax0.contourf(y[0][:-1, :-1] + dx/2.,
                  x[0][:-1, :-1] + dy/2., z[0], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax0)
cf = ax2.contourf(y[2][:-1, :-1] + dx/2.,
                  x[2][:-1, :-1] + dy/2., z[2], levels=levels,
                  cmap=cmap)

min, max = 0, 0.008
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
for i in [3]:
    z[i][where(z[i]>max)] = max
    z[i][where(z[i]<min)] = min

fig.colorbar(cf, ax=ax2)
cf = ax3.contourf(y[3][:-1, :-1] + dx/2.,
                  x[3][:-1, :-1] + dy/2., z[3], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax3)

# ax0.set_title('Vx profile for PlaneZ')
fig.tight_layout()
plt.show()
