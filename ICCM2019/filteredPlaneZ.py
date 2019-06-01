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

projDir = '/home/rao/myproject/ICCM2019/'

''' load original wake data '''
caseName = {0:'NBL.succ.254deg.11.4.0.001', 1:'NBL.succ.0.001.30', 2:'NBL.succ.0.001.m30'}

'''
做图过程：首先提取该case下-3D截面的尾流信息作为来流速度，再依次获取2D、6D、10D处的尾流信息做图
'''
''' 读入 case0-Sec2D 的信息 '''
case = 2
sec = 'PlaneZ'


''' 读入 case2 的信息 '''
# wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
''' assemble all the data of different secs in wakeDataDict '''
# wakeDataDict = {} # 存储所有的原始尾流信息
f = open(projDir + 'postProcessing_all/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()
timeList = list(wakeData_org.keys())
timeList.sort()
for time in timeList:
    wakeSec[time] = wakeData_org[time][sec]

secData = Sec(wakeSec)
del wakeData_org

secData_fd = secData.fSec_t(6,'18380')
secData_fd[:,1:] = tM.trs(secData_fd[:,1:]) # 第2列到第7列转换矩阵处理
secData_fd = SecITP(secData_fd)
secData_fd.meshITP_Nz((-378, 1512, 1890), (-252, 252, 504))

''' u contour for PlaneZ'''
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
for row in secData_fd.meshData:
    i = int(row[0,1]/dx) # i是行，对应于y坐标
    j = int(row[0,0]/dy) # j是列，对应于x坐标
    z[case][i+int(252/dy),j+int(378/dy)] = row[0,3] # i和j是矩阵坐标，而不是计算与坐标，需要换算
# z[case] = (11.4 - z[case]) / 11.4 # 仅在获取下游尾流信息时使用该代码
z[case] = z[case] / 11.4
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

# min, max = 0, 14
min, max = 0.4, 1.2
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
# for i in [0,1,2]:
#     z[i][where(z[i]>max)] = max
#     z[i][where(z[i]<min)] = min
cmap = plt.get_cmap('hot') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

plt.figure(figsize = (16, 6))
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

''' wake center trajectory '''
z[case] = 1 - z[case]
# 使x，y，z三个矩阵维数一致，并将拟合范围缩小至以轮毂中心左右1D范围，以排除大气低速气团的影响
x[case] = x[case][:-1,:-1]
y[case] = y[case][:-1,:-1]
x[case] = x[case][126:379,378:]
y[case] = y[case][126:379,378:]
z[case] = z[case][126:379,378:]

# 过滤版wake center
import fitting as ft
wc = np.array(zeros((x[case][0].shape[0],2)))
for j in range(x[case][0].shape[0]):
    p = y[case][:,j]
    vd = z[case][:,j]
    cp = ft.fit_gs((0,30),p,vd)[0]
    wc[j,0] = x[case][0,j]
    wc[j,1] = cp
# 时均版wake center
wcx = [  30.,   60.,   90.,  120.,  150.,  180.,  210.,  240.,  270.,
        300.,  330.,  360.,  390.,  420.,  450.,  480.,  510.,  540.,
        570.,  600.,  630.,  660.,  690.,  720.,  750.,  780.,  810.,
        840.,  870.,  900.,  930.,  960.,  990., 1020., 1050., 1080.,
       1110., 1140., 1170., 1200., 1230., 1260., 1290., 1320., 1350.,
       1380., 1410., 1440., 1470., 1500.]
wc0 = [-2.2130883 , -2.15952668, -2.08443188, -1.8727173 , -1.8331203 ,
       -1.79625799, -1.95649934, -1.88879547, -1.79534621, -1.96818774,
       -2.17196474, -2.55167703, -2.94661827, -2.66513258, -2.18496007,
       -1.88406583, -1.73906791, -1.51700212, -0.69452023,  0.03032263,
        0.23989504,  0.40922311,  0.6475269 ,  0.80644424,  0.895413  ,
        1.15338843,  1.94305596,  2.75454303,  3.4865705 ,  4.12392036,
        4.74633065,  5.35843472,  6.07307665,  6.3741805 ,  6.46084673,
        6.60394292,  6.66368833,  6.85008869,  7.27268015,  7.68944467,
        8.13269232,  8.51489921,  9.26799946,  9.97932444, 10.5460164 ,
       10.9014275 , 11.55449621, 12.15933017, 13.03145848, 13.67319598]
wc1 = [ 4.18356999,  9.4607254 , 11.8047845 , 14.05592439, 16.35219391,
       18.87522371, 20.89771179, 22.78411789, 24.68584201, 26.85346867,
       29.34203636, 31.69948359, 33.82845984, 35.77160497, 37.64590253,
       39.53625443, 41.23617666, 42.81143448, 44.52612444, 46.14471813,
       47.73545535, 49.30378734, 50.74140819, 52.20347711, 53.54619781,
       54.85762292, 56.09412564, 56.9897196 , 57.92946024, 59.16323862,
       60.23641995, 61.07220566, 61.84672698, 62.16283496, 62.49167599,
       62.57902216, 62.73739122, 62.97180211, 63.02989276, 63.39055227,
       64.10775371, 64.77749722, 65.35217496, 65.90310306, 66.53710914,
       67.05679898, 67.83754317, 68.40848605, 69.16816868, 69.81132898]
wc2 = [ -8.86314226, -14.09338725, -16.93166858, -19.32863098,
       -21.45108911, -23.25220861, -25.09078859, -27.16272684,
       -29.54487127, -31.87453856, -34.1180194 , -36.13724763,
       -37.66778087, -38.93863199, -39.83778917, -40.55547764,
       -41.25549684, -42.25533711, -43.33964192, -44.19455226,
       -44.71875815, -45.15284274, -45.53001191, -45.78697444,
       -46.13317874, -46.61683153, -47.26368971, -47.91592491,
       -48.54372838, -49.32675746, -49.99885887, -50.88874092,
       -51.64127931, -52.56979832, -53.34257928, -53.82322656,
       -54.19686492, -54.38030448, -55.05688134, -55.69886611,
       -55.99057556, -55.98659592, -56.04559957, -55.70874995,
       -55.41660332, -55.24569171, -54.93894291, -54.98720582,
       -54.93516764, -55.02592745]
plt.plot(wc[::,0][31:], wc[::,1][31:], 'k-', linewidth=3)
plt.plot(wcx, wc2, 'k--', linewidth=3)

plt.show()
