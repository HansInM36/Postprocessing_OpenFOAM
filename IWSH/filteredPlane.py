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

wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存

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

secNz = Sec(wakeDataDict)
del wakeDataDict

sec_test = secNz.fSec_t(6,'18300')
sec_test = SecITP(sec_test)
sec_test.meshITP_Nz((0, 2016, 1008), (0, 800, 400))

''' Vx contour for PlaneZ'''
x = {}
y = {}
z = {}

case = 2
sec = 'PlaneZ'
dx, dy = 2, 2
y[case], x[case] = np.mgrid[slice(0, 2016 + dy, dy),
                slice(0, 800 + dx, dx)]
y[case] = y[case].T
x[case] = x[case].T
z[case] = np.array(zeros(shape(x[case])))
for row in sec_test.meshData:
    i = int(row[0,1]/dx) # i = int(row[0,0]/dx) for ALMsolver; i = int(row[0,1]/dx) for SOWFA
    j = int(row[0,0]/dy) # j = int(row[0,1]/dy) for ALMsolver; j = int(row[0,0]/dy) for SOWFA
    z[case][i,j] = row[0,3] # row[0,4] for ALMsolver; row[0,3] for SOWFA
z[case] = z[case][:-1, :-1]

# zbp = z.copy() # back up
# xbp = x.copy() # back up
# ybp = y.copy() # back up
# x = xbp.copy()
# y = ybp.copy()
# z = zbp.copy()
#
# for i in range(0,4):
#     x[i] = x[i][74:326,188:]
#     y[i] = y[i][74:326,188:]
#     z[i] = z[i][74:325,188:]

min, max = 4, 12
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
for i in range(2,3):
    z[i][where(z[i]>11.6)] = 11.6
    z[i][where(z[i]<min)] = min

cmap = plt.get_cmap('gnuplot2') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3)

for i in [ax0, ax1, ax2]:
    i.set_xticks([376, 628, 880, 1132, 1384, 1636, 1888])
    i.set_xticklabels(['0D', '2D', '4D', '6D', '8D', '10D', '12D'])
    i.set_yticks([148, 274, 400, 526, 650])
    i.set_yticklabels(['-2D', '-1D', '0D', '1D', '2D'])

cf = ax2.contourf(y[2][:-1, :-1] + dx/2.,
                  x[2][:-1, :-1] + dy/2., z[2], levels=levels,
                  cmap=cmap)
fig.colorbar(cf, ax=ax2)

fig.tight_layout()
plt.show()
