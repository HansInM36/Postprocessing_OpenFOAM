import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import fitting as ft

projDir = '/media/nx/Ubuntu1/myproject/IWSH/'

''' load original wake data '''
caseName = {0:'uniIn', 1:'turbIn-0.2', 2:'NBL.succ.newdomain.56cores'}

sec = 'PlaneZ'

wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
secData = {}

''' 读入 case2 的信息 '''
case = 2
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
wakeSec[case] = Sec(wakeDataDict)
del wakeDataDict
''' 读入 case1 的信息 '''
case = 1
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
''' 读入 case0 的信息 '''
case = 0
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

''' 计算case0的meanderingdelta '''
wc = {}
for i in [0,1,2]:
    wc[i] = {}
x = {}
y = {}
z = {}

case=0
timeList = list(wakeSec[case].secData.keys())
for time in timeList:
    wc[case][time] = {}
for time in timeList:
    secData[case] = wakeSec[case].fSec_t(6,time)
    secData[case] = SecITP(secData[case])
    secData[case].meshITP_Nz((0, 800, 400), (0, 2016, 1008)) # ((0, 2016, 1008), (0, 800, 400)) for SOWFA
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
    x[case] = x[case][74:326,188:]
    y[case] = y[case][74:326,188:]
    z[case] = z[case][74:325,188:]
    x[case] = x[case][:-1,:-1]
    y[case] = y[case][:-1,:-1]
    x[case] = x[case][63:190,:]
    y[case] = y[case][63:190,:]
    z[case] = z[case][63:190,:]
    wc[case][time] = np.array(zeros((y[case][0].shape[0],1)))
    for j in range(y[case][0].shape[0]):
        p = x[case][:,j]
        vd = z[case][:,j]
        vd = 1 - vd/11.4
        cp = ft.fit_gs((400,20),p,vd)[0]
        wc[case][time][j,0] = abs(cp-400)
wc_ave = {}
sum_temp = {}
sum_temp[case] = np.array(zeros((y[case][0].shape[0],1)))
for time in timeList:
    sum_temp[case] += wc[case][time]**2
wc_ave[case] = (sum_temp[case] / len(timeList))**0.5
wc_ave[case] = np.hstack((y[case][0].T,wc_ave[case]))

case=1
timeList = list(wakeSec[case].secData.keys())
for time in timeList:
    wc[case][time] = {}
for time in timeList:
    secData[case] = wakeSec[case].fSec_t(6,time)
    secData[case] = SecITP(secData[case])
    secData[case].meshITP_Nz((0, 800, 400), (0, 2016, 1008)) # ((0, 2016, 1008), (0, 800, 400)) for SOWFA
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
    x[case] = x[case][74:326,188:]
    y[case] = y[case][74:326,188:]
    z[case] = z[case][74:325,188:]
    x[case] = x[case][:-1,:-1]
    y[case] = y[case][:-1,:-1]
    x[case] = x[case][63:190,:]
    y[case] = y[case][63:190,:]
    z[case] = z[case][63:190,:]
    wc[case][time] = np.array(zeros((y[case][0].shape[0],1)))
    for j in range(y[case][0].shape[0]):
        p = x[case][:,j]
        vd = z[case][:,j]
        vd = 1 - vd/11.4
        cp = ft.fit_gs((400,20),p,vd)[0]
        wc[case][time][j,0] = abs(cp-400)
wc_ave = {}
sum_temp = {}
sum_temp[case] = np.array(zeros((y[case][0].shape[0],1)))
for time in timeList:
    sum_temp[case] += wc[case][time]**2
wc_ave[case] = (sum_temp[case] / len(timeList))**0.5
wc_ave[case] = np.hstack((y[case][0].T,wc_ave[case]))

case=2
timeList = list(wakeSec[case].secData.keys())
for time in timeList:
    wc[case][time] = {}
for time in timeList:
    secData[case] = wakeSec[case].fSec_t(6,time)
    secData[case] = SecITP(secData[case])
    secData[case].meshITP_Nz((0, 2016, 1008), (0, 800, 400)) # ((0, 2016, 1008), (0, 800, 400)) for SOWFA
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
    x[case] = x[case][74:326,188:]
    y[case] = y[case][74:326,188:]
    z[case] = z[case][74:325,188:]
    x[case] = x[case][:-1,:-1]
    y[case] = y[case][:-1,:-1]
    x[case] = x[case][63:190,:]
    y[case] = y[case][63:190,:]
    z[case] = z[case][63:190,:]
    wc[case][time] = np.array(zeros((y[case][0].shape[0],1)))
    for j in range(y[case][0].shape[0]):
        p = x[case][:,j]
        vd = z[case][:,j]
        vd = 1 - vd/11.4
        cp = ft.fit_gs((400,20),p,vd)[0]
        wc[case][time][j,0] = abs(cp-400)
wc_ave = {}
sum_temp = {}
sum_temp[case] = np.array(zeros((y[case][0].shape[0],1)))
for time in timeList:
    sum_temp[case] += wc[case][time]**2
wc_ave[case] = (sum_temp[case] / len(timeList))**0.5
wc_ave[case] = np.hstack((y[case][0].T,wc_ave[case]))
