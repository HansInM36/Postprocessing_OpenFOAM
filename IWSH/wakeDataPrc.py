import sys
from sys import path
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
import pickle  # for reading the original wake data

# add a specified path to the searching system for python
# sys.path.append(r'/home/rao/OpenFOAM/nx-2.3.1-winfarm-v3.0/clusterproject-hub/wakeMerge/code')

''' load original wake data '''
caseName = {0:'NBL.prec', 1:'CBL.prec', 2:'SBL.prec'}
wakeDataDict = {} # 存储所有 case 的尾流信息
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_ave = {} # 求出所有 case 中尾流的时均值并存入该字典
wake_TI = {} # 求出所有 case 中尾流的湍流强度并存入该字典
ave = {} # wake_ave 的网格化版本
TI = {} # wake_ave 的网格化版本

for i in range(0,3):
    f = open(caseName[i] + '_wakeData', 'rb')
    wakeDataDict[i] = pickle.load(f) # all wake information of the case
    f.close()

''' compute average wake data '''
for i in range(0,3):
    wake[i] = Wake(wakeDataDict[i])
    wake_ave[i] = wake[i].ave_wakeData() # wake_ave is a dict containing the average data of the wake
    wake_TI[i] = wake[i].intensity()

''' preparing mesh data for plot '''
secData_ave = {}
secData_TI = {}
for i in range(0,3):
    secData_ave[i] = dict(zip(wake[i].secList, wake[i].secList))
    secData_TI[i] = dict(zip(wake[i].secList, wake[i].secList))
    for sec in secData_ave[i].keys():
        secData_ave[i][sec] = WakeSec(wake_ave[i][sec])
        secData_TI[i][sec] = WakeSec(wake_TI[i][sec])
        secData_ave[i][sec].meshITP_Nx((0, 400, 200), (0, 400, 200))
        secData_TI[i][sec].meshITP_Nx((0, 400, 200), (0, 400, 200))
    # del wake_ave[i]
    # del wake[i]
    # del wakeDataDict[i]

''' plot Vx profile at specific height'''
height = 200
plt.figure(figsize = (8, 4))
x = secData_ave['Sec0'].z_cut(height)['Vx']
y = secData_ave['Sec0'].z_cut(height)['y']
plt.plot(x, y, 'ro-', linewidth = 1)
x = secData_ave['Sec3'].z_cut(height)['Vx']
y = secData_ave['Sec3'].z_cut(height)['y']
plt.plot(x, y, 'b*-', linewidth = 1)
plt.ylabel('y(m)')
plt.xlabel('v(m/s)')
plt.title('v profile')
plt.xlim(0, 15, 0.5)
plt.grid()
plt.show()

''' plot Vx vertical profile of different atmospheric stability'''
plt.figure(figsize = (8, 6))
x = secData_ave[0]['Sec0'].meshData_horizAve['Vx'][::5]
y = secData_ave[0]['Sec0'].meshData_horizAve['z'][::5]
plt.plot(x, y, 'go-', linewidth=1, label='NBL')
x = secData_ave[1]['Sec0'].meshData_horizAve['Vx'][::5]
y = secData_ave[1]['Sec0'].meshData_horizAve['z'][::5]
plt.plot(x, y, 'ro-', linewidth=1, label='CBL')
x = secData_ave[2]['Sec0'].meshData_horizAve['Vx'][::5]
y = secData_ave[2]['Sec0'].meshData_horizAve['z'][::5]
plt.plot(x, y, 'bo-', linewidth=1, label='SBL')
plt.ylabel('z(m)')
plt.xlabel('u(m/s)')
plt.title('u profile')
plt.xlim(0, 15, 0.5)
legend = plt.legend(loc='upper left', shadow=True, fontsize='x-large')
legend.get_frame().set_facecolor('C1')
plt.grid()
plt.show()

''' plot Vx vertical profile of different positions downstream'''
stability = 0
plt.figure(figsize = (8, 6))
x = secData_ave[stability]['Sec0'].meshData_horizAve['Vx'][::5]
y = secData_ave[stability]['Sec0'].meshData_horizAve['z'][::5]
plt.plot(x, y, 'g1-', linewidth=1, label='80m')
x = secData_ave[stability]['Sec1'].meshData_horizAve['Vx'][::5]
y = secData_ave[stability]['Sec1'].meshData_horizAve['z'][::5]
plt.plot(x, y, 'g2--', linewidth=1, label='200m')
x = secData_ave[stability]['Sec2'].meshData_horizAve['Vx'][::5]
y = secData_ave[stability]['Sec2'].meshData_horizAve['z'][::5]
plt.plot(x, y, 'g3-.', linewidth=1, label='400m')
x = secData_ave[stability]['Sec3'].meshData_horizAve['Vx'][::5]
y = secData_ave[stability]['Sec3'].meshData_horizAve['z'][::5]
plt.plot(x, y, 'g4:', linewidth=1, label='520m')
plt.ylabel('z(m)')
plt.xlabel('u(m/s)')
plt.title('u profile')
plt.xlim(0, 15, 0.5)
legend = plt.legend(loc='upper left', shadow=True, fontsize='x-large')
legend.get_frame().set_facecolor('C1')
plt.grid()
plt.show()

''' Vx profiles different stabilities and downstream positions '''
from pylab import mpl
from matplotlib.gridspec import GridSpec

fig = plt.figure(1, figsize=(8, 6))
fig.subplots_adjust(bottom=0.2)
ax = {}
gs = GridSpec(2,2)
title = {0:'Vx profile (80m)', 1:'Vx profile (200m)', 2:'Vx profile (400m)', 3:'Vx profile (520m)'}
for i in range(0,4):
    ax[i] = plt.subplot(gs[int(i//2), int(i%2)])

    # x = secData_ave[0]['Sec'+str(i)].meshData_horizAve['Vx'][::8]
    # y = secData_ave[0]['Sec'+str(i)].meshData_horizAve['z'][::8]
    # ax[i].plot(x, y, 'go-', linewidth=1, label='NBL')
    x = secData_ave[1]['Sec'+str(i)].meshData_horizAve['Vx'][::8]
    y = secData_ave[1]['Sec'+str(i)].meshData_horizAve['z'][::8]
    ax[i].plot(x, y, 'ro-', linewidth=1, label='CBL')
    x = secData_ave[2]['Sec'+str(i)].meshData_horizAve['Vx'][::8]
    y = secData_ave[2]['Sec'+str(i)].meshData_horizAve['z'][::8]
    ax[i].plot(x, y, 'bo-', linewidth=1, label='SBL')
    ax[i].set_ylabel('z(m)')
    ax[i].set_xlabel('Vx(m/s)')
    ax[i].set_title(title[i])
    ax[i].set_xlim(0, 15, 0.5)
    legend = ax[i].legend(loc='upper left', fontsize='x-large')
    ax[i].grid()
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()

''' TIx profiles different stabilities and downstream positions '''
from pylab import mpl
from matplotlib.gridspec import GridSpec

fig = plt.figure(1, figsize=(8, 6))
fig.subplots_adjust(bottom=0.2)
ax = {}
gs = GridSpec(2,2)
title = {0:'TIx profile (80m)', 1:'TIx profile (200m)', 2:'TIx profile (400m)', 3:'TIx profile (520m)'}
for i in range(0,4):
    ax[i] = plt.subplot(gs[int(i//2), int(i%2)])

    # x = secData_TI[0]['Sec'+str(i)].meshData_horizAve['Vx'][::8]
    # y = secData_TI[0]['Sec'+str(i)].meshData_horizAve['z'][::8]
    # ax[i].plot(x, y, 'gs-', linewidth=1, label='NBL')
    x = secData_TI[1]['Sec'+str(i)].meshData_horizAve['Vx'][::6]
    y = secData_TI[1]['Sec'+str(i)].meshData_horizAve['z'][::6]
    ax[i].plot(x, y, 'rs-', linewidth=1, label='CBL')
    x = secData_TI[2]['Sec'+str(i)].meshData_horizAve['Vx'][::6]
    y = secData_TI[2]['Sec'+str(i)].meshData_horizAve['z'][::6]
    ax[i].plot(x, y, 'bs-', linewidth=1, label='SBL')
    ax[i].set_ylabel('z(m)')
    ax[i].set_xlabel('TIx')
    ax[i].set_title(title[i])
    ax[i].set_xlim(0, 0.4, 0.02)
    legend = ax[i].legend(loc='upper right', fontsize='x-large')
    ax[i].grid()
plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
plt.show()

''' velocity history curve of a certain point in a certain sec'''
sec = 'Sec0'
pCoor={'y':200, 'z':17} #coordinate of the point in certain sec whose normal vector is aligned with xaxis
t = {}
tList = {}
Vx = {}
Vy = {}
Vz = {}
for i in range(0,3):
    # get time series for case i
    tList_str = list(wake[i].wakeData.keys())
    tList[i] = [float(x) for x in tList_str]
    t[i] = mat(sorted(tList[i]))
    # get V series for case i
    coorMat = wake[i].wakeData[str(t[i][0,0])][sec][:,[0,2,3]] # 3 colume mat, representing ID,y,z
    rowNum = 0
    deltaM = 9999
    for row in coorMat:
        delta = (row[0,1] - pCoor['y'])**2 + (row[0,2] - pCoor['z'])**2
        if delta < deltaM :
            deltaM = delta
            rowNum = row[0,0]
    Vx[i] = mat(zeros(shape(t[i]))) # initialize a mat for Vx series
    for time in tList[i]:
        index = np.argwhere(t[i]==time)[0,1]
        Vx[i][0,index] = wake[i].wakeData[str('{:g}'.format(time))][sec][int(rowNum-1),4]
    Vy[i] = mat(zeros(shape(t[i]))) # initialize a mat for Vx series
    for time in tList[i]:
        index = np.argwhere(t[i]==time)[0,1]
        Vy[i][0,index] = wake[i].wakeData[str('{:g}'.format(time))][sec][int(rowNum-1),5]
    Vz[i] = mat(zeros(shape(t[i]))) # initialize a mat for Vx series
    for time in tList[i]:
        index = np.argwhere(t[i]==time)[0,1]
        Vz[i][0,index] = wake[i].wakeData[str('{:g}'.format(time))][sec][int(rowNum-1),6]

# Vx history curve
plt.figure(figsize = (8, 4))
plt.plot(t[1].T, Vx[1].T, 'r-', linewidth = 1, label='CBL')
plt.plot(t[2].T, Vx[2].T, 'b-', linewidth = 1, label='SBL')
plt.ylabel('Vx(m/s)')
plt.xlabel('t(s)')
plt.title('Vx history curve (rotor bottom)')
plt.xlim(18000, 18200, 20)
plt.ylim(4, 14, 2)
plt.legend(loc='lower right', shadow=True, fontsize='x-large')
plt.grid()
plt.show()

# Vz history curve
plt.figure(figsize = (8, 4))
plt.plot(t[1].T, Vz[1].T, 'r-', linewidth = 1, label='CBL')
plt.plot(t[2].T, Vz[2].T, 'b-', linewidth = 1, label='SBL')
plt.ylabel('Vz(m/s)')
plt.xlabel('t(s)')
plt.title('Vz history curve (rotor bottom)')
plt.xlim(18000, 18200, 20)
plt.ylim(-2, 2, 0.2)
plt.legend(loc='lower right', shadow=True, fontsize='x-large')
plt.grid()
plt.show()
