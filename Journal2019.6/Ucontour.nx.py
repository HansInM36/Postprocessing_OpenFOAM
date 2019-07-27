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
case = 0
sec = 'Sec10D'


# 建立一些空字典
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_ave = {} # wake 的时均（剥离了第二层的key，wake_ave[case]直接就是sec的矩阵）
wake_mesh = {} # wake_ave 经转换矩阵处理后的网格化版本, SecITP 类
# wakeSec = {}
# secData = {}


''' assemble all the data of different secs in wakeDataDict '''
wakeDataDict = {} # 存储所有的原始尾流信息
f = open(projDir + 'postProcessing_all/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()
wake[case] = Wake(wakeData_org)
del wakeData_org # 汇总完了删除这个临时字典
wake_ave[case] = wake[case].ave_wakeData()[sec]
wake_ave[case][:,1:] = tM.trs(wake_ave[case][:,1:])
wake_mesh[case] = SecITP(wake_ave[case])
wake_mesh[case].meshITP_Nx((-252, 252, 504), (0, 342, 342))

''' u contour for sec'''
x = {}
y = {}
z = {}
# 编织网格
dx, dy = 1, 1
x[case], y[case] = np.mgrid[slice(-252, 252 + dx, dx),
                slice(0, 342 + dy, dy)]
x[case] = x[case].T
y[case] = y[case].T
# 向网格里填值
z[case] = np.array(zeros(shape(x[case])))
for row in wake_mesh[case].meshData:
    i = int(row[0,2]/dx) # i是行，对应于z坐标
    j = int(row[0,1]/dy) # j是列，对应于y坐标
    z[case][i,j+int(252/dy)] = row[0,3] # i和j是矩阵坐标，而不是计算与坐标，需要换算
# z0 = z[case] # 仅在获取来流信息时使用该代码
z[case] = (z0 - z[case]) / z0 # 仅在获取下游尾流信息时使用该代码
# 去边儿
z[case] = z[case][:-1, :-1]
# 镜面对称，使得视角是从上游到下游
zz = np.zeros(z[case].shape)
for i in range(zz.shape[1]):
    zz[:,i] = z[case][:,-i-1]


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
min, max = -0.2, 0.6
levels = MaxNLocator(nbins=40).tick_values(min, max)
# 处理一下z
# for i in [0,1,2]:
#     z[i][where(z[i]>max)] = max
#     z[i][where(z[i]<min)] = min
cmap = plt.get_cmap('jet') #'viridis'
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)

plt.figure(figsize = (5, 3))
plt.contourf(x[case][:-1, :-1] + dy/2.,
                  y[case][:-1, :-1] + dx/2., zz, levels=levels,
                  cmap=cmap)
plt.xlim(-200,200)
plt.ylim(16,300)
plt.xticks([-189, -126, -63, 0, 63, 126, 189], [-3, -2, -1, 0, 1, 2, 3])
plt.yticks([27, 90, 153, 216, 279], [-1, 0, 1, 2, 3])
plt.colorbar()
plt.plot(0, 90, 'k+', linewidth=2) # rotor center
# rotor circle
ag = np.linspace(0, 2*np.pi, 180)
plt.plot(63*np.cos(ag), 63*np.sin(ag)+90, 'k-', linewidth=2)
# mark probes
# prby0 = [-2.52006091e+02, -2.36043805e+02, -2.19958409e+02, -2.03969366e+02,
#        -1.87980323e+02, -1.71991280e+02, -1.56028995e+02, -1.40039952e+02,
#        -1.23954555e+02, -1.15973413e+02, -1.07965512e+02, -9.99843698e+01,
#        -9.19764696e+01, -8.39953269e+01, -7.59874268e+01, -6.80062841e+01,
#        -6.00251414e+01, -5.40085066e+01, -4.79918718e+01, -4.19484795e+01,
#        -3.60281984e+01, -3.00115636e+01, -2.39949288e+01, -1.79782940e+01,
#        -1.19616592e+01, -6.04137806e+00, -2.47432485e-02,  5.99189156e+00,
#         1.20085264e+01,  1.80251612e+01,  2.40417960e+01,  2.99620771e+01,
#         3.59787119e+01,  4.19953467e+01,  4.80119815e+01,  5.40286163e+01,
#         5.99488974e+01,  6.79567976e+01,  7.60342940e+01,  8.40421942e+01,
#         9.20233368e+01,  1.00004480e+02,  1.08012380e+02,  1.15993522e+02,
#         1.24001423e+02,  1.39963708e+02,  1.55952751e+02,  1.72038147e+02,
#         1.88027190e+02,  2.04016233e+02,  2.20005276e+02,  2.35967561e+02,
#         2.51956604e+02]
# prby1 = [90 for i in prby1]
# prbz1 = [  6.1,  12.1,  18.1,  24.1,  30.1,  36.1,  42.1,  48.1,  52.1,
#         60.1,  66.1,  72.1,  78.1,  84.1,  90.1,  96.1, 102.1, 108.1,
#        114.1, 120.1, 126.1, 132.1, 138.1, 144.1, 150.1, 158.1, 166.1,
#        174.1, 182.1, 190.1, 198.1, 206.1, 214.1, 230.1, 246.1, 262.1,
#        278.1, 294.1, 310.1, 326.1, 342.1]
# prbz0 = [0 for i in prbz1]
# plt.plot(prby0, prby1, 'k.', linewidth=1)
# plt.plot(prbz0, prbz1, 'k.', linewidth=1)
plt.show()
