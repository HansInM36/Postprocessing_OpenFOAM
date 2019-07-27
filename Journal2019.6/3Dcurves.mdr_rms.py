import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import fitting as ft
import trsMat as tM
import wakeDataClass
from wakeDataClass import *
import math
from mpl_toolkits.mplot3d import Axes3D

''' loads the probeData '''
# directories
projDir = '/home/rao/myproject/Journal2019.6/'
case = {0:'NBL.1T', 1:'CBL.1T'}

wcb = {}
# 读取 wcb (二维字典，一级key是probe，二级key是时刻)
f = open(projDir + 'postProcessing_all/data.processed/' + case[0] + '_wcb.nz', 'rb')
wcb[0] = pickle.load(f) # all wake information of the case
f.close()
f = open(projDir + 'postProcessing_all/data.processed/' + case[1] + '_wcb.nz', 'rb')
wcb[1] = pickle.load(f) # all wake information of the case
f.close()
f = open(projDir + 'postProcessing_all/data.processed/' + case[0] + '_wcb.ny', 'rb')
wcb[2] = pickle.load(f) # all wake information of the case
f.close()
f = open(projDir + 'postProcessing_all/data.processed/' + case[1] + '_wcb.ny', 'rb')
wcb[3] = pickle.load(f) # all wake information of the case
f.close()

# mdr概率曲线
cn = 1
prbs = ['probe2Dy', 'probe3Dy', 'probe4Dy', 'probe5Dy',
        'probe6Dy', 'probe7Dy', 'probe8Dy', 'probe9Dy', 'probe10Dy',
        'probe11Dy', 'probe12Dy']

# 估计范围
min = 1*126
max = 0.2*126
for prb in prbs:
    min_ = np.min(abs(wcb[cn][prb][:,1]))
    max_ = np.max(abs(wcb[cn][prb][:,1]))
    if min_ < min:
        min = min_
    if max_ > max:
        max = max_

N = 20 # 分成 N 个区间
M = 1 # 最大值为 M
delta = np.linspace(0,M,N+1)
deltan = {}
for prb in prbs:
    deltan[prb] = np.zeros((delta.shape[0]-1,1))
    tNum = wcb[cn][prb].shape[0]
    for j in range(tNum):
        dlt = abs(wcb[cn][prb][j,1])/126
        if dlt > M: # 除去坏点
            dlt = M-0.001
        index = math.floor(dlt/(M/N))
        deltan[prb][index] += 1
    deltan[prb] = deltan[prb] / np.sum(deltan[prb])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

color = ['firebrick','red','tomato','orange','yellow','lawngreen','green','cyan','dodgerblue','deeppink','purple']
yticks = [2,3,4,5,6,7,8,9,10,11,12] #[12,11,10,9,8,7,6,5,4,3,2]
for i in range(11):
    xs = delta[:-1]
    ys = deltan[prbs[i]]

    # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
    ax.plot(xs, ys, yticks[i], color=color[i], linestyle='-', zdir='y', alpha=0.8)

ax.set_zlim(0,0.6)
ax.set_zticks([0.0,0.1,0.2,0.3,0.4,0.5,0.6],[0.0,0.1,0.2,0.3,0.4,0.5,0.6])
ax.set_xlim(0,1.0)
ax.set_xticks([0.0,0.2,0.4,0.6,0.8,1.0],[0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# On the y axis let's only label the discrete values that we have data for.
ax.set_yticks(yticks)

plt.show()



# mdr概率曲线
cn = 0
prbsy = ['probe2Dy', 'probe3Dy', 'probe4Dy', 'probe5Dy',
        'probe6Dy', 'probe7Dy', 'probe8Dy', 'probe9Dy', 'probe10Dy',
        'probe11Dy', 'probe12Dy']
prbsz = ['probe2Dz', 'probe3Dz', 'probe4Dz', 'probe5Dz',
        'probe6Dz', 'probe7Dz', 'probe8Dz', 'probe9Dz', 'probe10Dz',
        'probe11Dz', 'probe12Dz']

# 估计范围
min = 1*126
max = 1*126
for prb in prbs:
    min_ = np.min(abs(wcb[cn][prb][:,2])*1.665)
    max_ = np.max(abs(wcb[cn][prb][:,2])*1.665)
    if min_ < min:
        min = min_
    if max_ > max:
        max = max_

N = 40 # 分成 N 个区间
Min = 0
Max = 1 # 最大值为 M
delta = np.linspace(Min,Max,N+1)
deltan = {}
for i in range(11): # 11个prb
    deltan[i] = np.zeros((delta.shape[0]-1,1))
    tNum = wcb[cn][prbsy[i]].shape[0]
    for j in range(tNum):
        dlty = abs(wcb[cn][prbsy[i]][j,1])/126
        dltz = abs(wcb[cn+2][prbsz[i]][j,1])/126
        dlt = np.power(dlty**2+dltz**2,0.5)
        if dlt > Max: # 除去坏点
            continue
        if dlt < Min:
            continue
        index = math.floor(dlt/((Max-Min)/N) - Min/((Max-Min)/N))
        deltan[i][index] += 1
    deltan[i] = deltan[i] / np.sum(deltan[i])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

color = ['firebrick','red','tomato','orange','yellow','lawngreen','green','cyan','dodgerblue','deeppink','purple']
yticks = [2,3,4,5,6,7,8,9,10,11,12] #[12,11,10,9,8,7,6,5,4,3,2]
for i in range(11):
    xs = delta[:-1]
    # ys = deltan[prbs[i]]
    ys = flt_seq(deltan[i],3)

    # Plot the bar graph given by xs and ys on the plane y=k with 80% opacity.
    ax.plot(xs, ys, yticks[i], color=color[i], linestyle='-', zdir='y', alpha=0.8)

ax.set_zlim(0,0.12)
# ax.set_zticks([0.0,0.1,0.2,0.3,0.4,0.5,0.6],[0.0,0.1,0.2,0.3,0.4,0.5,0.6])
ax.set_xlim(0.0,6.0)
# ax.set_xticks([0.0,0.2,0.4,0.6,0.8,1.0],[0.0,0.2,0.4,0.6,0.8,1.0])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# On the y axis let's only label the discrete values that we have data for.
ax.set_yticks(yticks)

plt.show()
