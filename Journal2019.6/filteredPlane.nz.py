import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
import trsMat as tM
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

projDir = '/home/rao/myproject/Journal2019.6/'

''' load original wake data '''
caseName = {0:'NBL.1T', 1:'CBL.1T'}
case = 1
sec = 'PlaneZ'

x = {}
y = {}
z = {}

''' 读入 case 的信息 '''
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
secData = {}

''' assemble all the data of different secs in wakeDataDict '''
# # NBL case:
# f = open(projDir + 'postProcessing_all/data.org/' + caseName[case] + '_' + sec + '_wakeData_part1', 'rb')
# wakeData_org_part1 = pickle.load(f) # all wake information of the case
# f.close()
# f = open(projDir + 'postProcessing_all/data.org/' + caseName[case] + '_' + sec + '_wakeData_part2', 'rb')
# wakeData_org_part2 = pickle.load(f) # all wake information of the case
# f.close()
# wakeData_org = {**wakeData_org_part1, **wakeData_org_part2}
# del wakeData_org_part1
# del wakeData_org_part2

# CBL case:
f = open(projDir + 'postProcessing_all/data.org/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()

# 目的是剥离二级key
wakeDataDict = {}
timeList = list(wakeData_org.keys())
for time in timeList:
    wakeDataDict[time] = wakeData_org[time][sec]
del wakeData_org # 汇总完了删除这个临时字典

wakeSec[case] = Sec(wakeDataDict)
del wakeDataDict

# 过滤并网格化数据
secData_fd = wakeSec[case].fSec_t(3,'18540')
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

plt.figure(figsize = (14, 2.8))
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

import fitting as ft
wc = np.array(zeros((x[case][0].shape[0],3)))
for j in range(x[case][0].shape[0]):
    p = y[case][:,j]
    vd = z[case][:,j]
    miu, sgm = ft.fit_gs((0,30),p,vd)
    wc[j,0] = x[case][0,j]
    wc[j,1] = miu
    wc[j,2] = sgm

plt.plot(wc[::,0][251:], wc[::,1][251:], 'k-', linewidth=2)
plt.plot(wc[::,0][251:], wc[::,1][251:] + 1.665*wc[::,2][251:], 'k--', linewidth=2)
plt.plot(wc[::,0][251:], wc[::,1][251:] - 1.665*wc[::,2][251:], 'k--', linewidth=2)
# plt.plot(wcx, wc2, 'k--', linewidth=3)

plt.show()

# 检测fit_gs函数的正确性, 顺便也能做某截面的拟合图像
p = y[case][:,126*8]
vd = z[case][:,126*8]
miu, sgm = ft.fit_gs((0,30),p,vd)
xx = p
yy = vd
delta = (np.max(xx) - np.min(xx)) / (np.shape(xx)[0] - 1)
S = sum(yy)*delta - 0.5*(yy[np.where(xx==np.min(xx))] + yy[np.where(xx==np.max(xx))])
yyp = ft.func_gs((miu,sgm),xx)*S
plt.figure(figsize = (9, 4))
# plt.plot(xx, yy, 'bo:', linewidth = 1, label='velocity deficit - NBL')
# plt.plot(xx, yyp, 'k-', linewidth = 1, label='gaussian fitting curve')
plt.plot(xx, yy, 'ro:', linewidth = 1, label='velocity deficit - CBL')
plt.plot(xx, yyp, 'k-', linewidth = 1, label='gaussian fitting curve')
plt.xlabel('r/R')
plt.ylabel('1-u/u0')
plt.xlim(-126, 126)
plt.ylim(-0.1, 0.5)
plt.xticks([-126,-63,0,63,126],['-2','1','0','1','2'])
legend = plt.legend(loc='upper right', shadow=False, fontsize=10)
plt.grid()
plt.show()
