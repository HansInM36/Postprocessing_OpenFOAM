import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import trsMat as tM

projDir = '/home/rao/myproject/Journal2019.6/'

''' load original wake data '''
caseName = {0:'NBL.1T', 1:'CBL.1T'}

'''
做图过程：首先提取该case下-3D截面的尾流信息作为来流速度，再依次获取2D、6D、10D处的尾流信息做图
'''
''' 读入截面的信息 '''
case = 1
sec = 'PlaneZ'


# 建立一些空字典
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_ave = {} # wake 的时均（剥离了第二层的key，wake_ave[case]直接就是sec的矩阵）
wake_mesh = {} # wake_ave 经转换矩阵处理后的网格化版本, SecITP 类



''' assemble all the data of different secs in wakeDataDict '''
# wakeDataDict = {} # 存储所有的原始尾流信息
f = open(projDir + 'postProcessing_all/data.org/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()
wake[case] = Wake(wakeData_org)
del wakeData_org # 汇总完了删除这个临时字典
wake_ave[case] = wake[case].ave_wakeData()[sec]
wake_ave[case][:,1:] = tM.trs(wake_ave[case][:,1:]) # 第2列到第7列转换矩阵处理



timeList = list(wake[case].wakeData.keys())
timeList.sort()
TKE = np.zeros((wake_ave[case][:,3].shape))
for time in timeList:
    Utemp = tM.trs(wake[case].wakeData[time][sec][:,1:])[:,3]
    for i in range(TKE.shape[0]):
        TKE[i,0] += np.power(Utemp[i] - wake_ave[case][:,4][i],2)
TKE /= len(timeList) * np.power(11.4,2)
TKE = np.hstack((wake_ave[case][1:4], TKE))

''' save TKE into a file with pickle '''
import pickle
f = open(projDir + 'postProcessing_all/data.processed/' + caseName[case] + '_' + sec + '_TKE', 'wb')
pickle.dump(TKE, f)
f.close()

wake_mesh[case] = SecITP(wake_ave[case])
wake_mesh[case].meshITP_Nz((-378, 1512, 1890), (-252, 252, 504))
''' u_ave for PlaneZ'''
x = {}
y = {}
z = {}
# 编织网格
dx, dy = 1, 1
x[case], y[case] = np.mgrid[slice(-378, 1512 + dx, dx),
                slice(-252, 252 + dy, dy)]
x[case] = x[case].T
y[case] = y[case].T
# 向网格里填值
z[case] = np.array(zeros(shape(x[case])))
for row in TKE:
    i = int(row[0,1]/dx) # i是行，对应于y坐标
    j = int(row[0,0]/dy) # j是列，对应于x坐标
    z[case][i+int(252/dy),j+int(378/dy)] = row[0,3] # i和j是矩阵坐标，而不是计算与坐标，需要换算

# 去边儿
z[case] = z[case][:-1, :-1]
# 镜面对称，使得视角是从上游到下游
# zz = np.zeros(z[case].shape)
# for i in range(zz.shape[1]):
#     zz[:,i] = z[case][:,-i-1]


zbp = z.copy() # back up
xbp = x.copy() # back up
ybp = y.copy() # back up
# x = xbp.copy()
# y = ybp.copy()
# z = zbp.copy()

# 裁剪
# for i in [0,1,2]:
#     x[i] = x[i][74:326,188:]
#     y[i] = y[i][74:326,188:]
#     z[i] = z[i][74:325,188:]

min, max = -0.1, 0.5
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
# for i in [0,1,2]:
#     z[i][where(z[i]>max)] = max
#     z[i][where(z[i]<min)] = min
cmap = plt.get_cmap('jet') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

plt.figure(figsize = (16, 4))
plt.contourf(x[case][:-1, :-1] + dy/2.,
                  y[case][:-1, :-1] + dx/2., z[case], levels=levels,
                  cmap=cmap)
plt.xlim(-378,1512)
plt.ylim(-252,252)
plt.xticks([-378, -252, -126, 0 ,126, 252, 378, 504, 630, 756, 882, 1008, 1134, 1260, 1386, 1512],
           [-3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
plt.yticks([-252, -189, -126, -63, 0, 63, 126, 189, 252],
           [-2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2])
plt.colorbar()

plt.show()
