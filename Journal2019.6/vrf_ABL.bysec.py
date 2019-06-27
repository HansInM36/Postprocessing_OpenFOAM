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
import fitting as fit

projDir = '/home/rao/myproject/Journal2019.6/'

''' load original wake data '''
caseName = {0:'NBL.1T', 1:'CBL.1T'}

'''
做图过程：首先提取该case下-3D截面的尾流信息作为来流速度，再依次获取2D、6D、10D处的尾流信息做图
'''
''' 读入 case0-Sec2D 的信息 '''
# case = 1
sec = 'Sec-3D'


# 建立一些空字典
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_ave = {} # wake 的时均（剥离了第二层的key，wake_ave[case]直接就是sec的矩阵）
wake_TI = {}
wake_ave_mesh = {} # wake_ave 经转换矩阵处理后的网格化版本, SecITP 类
wake_TI_mesh = {} # wake_TI 经转换矩阵处理后的网格化版本, SecITP 类
# wakeSec = {}
# secData = {}


''' assemble all the data of different secs in wakeDataDict '''
for case in range(2):
    wakeDataDict = {} # 存储所有的原始尾流信息
    f = open(projDir + 'postProcessing_all/data.org/' + caseName[case] + '_' + sec + '_wakeData', 'rb')
    wakeData_org = pickle.load(f) # all wake information of the case
    f.close()
    for t in list(wakeData_org.keys()): # 将原始的流场信息转换到新坐标系
        wakeData_org[t][sec][:,1:] = tM.trs(wakeData_org[t][sec][:,1:])
    wake[case] = Wake(wakeData_org)
    del wakeData_org # 汇总完了删除这个临时字典

for case in range(2):
    wake_ave[case] = wake[case].ave_wakeData()[sec]
    wake_TI[case] = wake[case].intensity()[sec]

    wake_ave_mesh[case] = SecITP(wake_ave[case])
    wake_ave_mesh[case].meshITP_Nx((-252, 252, 504), (0, 342, 342))
    wake_TI_mesh[case] = SecITP(wake_TI[case])
    wake_TI_mesh[case].meshITP_Nx((-252, 252, 504), (0, 342, 342))

''' u profile'''
x = {}
y = {}
u = {}
# 编织网格
for case in range(2):
    dx, dy = 1, 1
    x[case], y[case] = np.mgrid[slice(-252, 252 + dx, dx),
                    slice(0, 342 + dy, dy)]
    x[case] = x[case].T
    y[case] = y[case].T
    # 向网格里填值
    u[case] = np.array(zeros(shape(x[case])))
    for row in wake_ave_mesh[case].meshData:
        i = int(row[0,2]/dx) # i是行，对应于z坐标
        j = int(row[0,1]/dy) # j是列，对应于y坐标
        u[case][i,j+int(252/dy)] = row[0,3] # i和j是矩阵坐标，而不是计算与坐标，需要换算

z = y[case][:,0]
plt.figure(figsize = (6, 6))
us = np.zeros((z.shape))
for i in range(z.shape[0]):
    us[i] = np.mean(u[0][i,:])
us = flt_seq(us,10)
pp = fit.fit_ABL(0.7,0.4,0.001,z[27:153],us[27:153]) # u*=0.4075
xp = fit.func_ABL(pp,0.4,0.001,z)
plt.plot(us/11.4, z, 'b-', linewidth = 2, label='NBL')
plt.plot(xp[1:]/11.4, z[1:], 'k--', linewidth = 2, label='logarithmic law')
for i in range(z.shape[0]):
    us[i] = np.mean(u[1][i,:])
us = flt_seq(us,10)
plt.plot(us/11.4, z, 'r-', linewidth = 2, label='CBL')
plt.ylabel('z(m)')
plt.xlabel('u/u0')
plt.xlim(0.6, 1.2, 0.2)
plt.ylim(0, 300, 50)
legend = plt.legend(loc='upper left', shadow=False, fontsize='x-large')
plt.grid()
plt.show()



''' TI profile'''
x = {}
y = {}
TIx = {}
TIy = {}
TIz = {}
# 编织网格
for case in range(2):
    dx, dy = 1, 1
    x[case], y[case] = np.mgrid[slice(-252, 252 + dx, dx),
                    slice(0, 342 + dy, dy)]
    x[case] = x[case].T
    y[case] = y[case].T
    # 向网格里填值
    TIx[case] = np.array(zeros(shape(x[case])))
    TIy[case] = np.array(zeros(shape(x[case])))
    TIz[case] = np.array(zeros(shape(x[case])))
    for row in wake_TI_mesh[case].meshData:
        i = int(row[0,2]/dx) # i是行，对应于z坐标
        j = int(row[0,1]/dy) # j是列，对应于y坐标
        TIx[case][i,j+int(252/dy)] = row[0,3] # i和j是矩阵坐标，而不是计算与坐标，需要换算
        TIy[case][i,j+int(252/dy)] = row[0,4] # i和j是矩阵坐标，而不是计算与坐标，需要换算
        TIz[case][i,j+int(252/dy)] = row[0,5] # i和j是矩阵坐标，而不是计算与坐标，需要换算

z = y[case][:,0]
plt.figure(figsize = (6, 6))

tix = np.zeros((z.shape))
tiy = np.zeros((z.shape))
tiz = np.zeros((z.shape))
for i in range(z.shape[0]):
    tix[i] = np.mean(TIx[0][i,:])
    tiy[i] = np.mean(TIy[0][i,:])
    tiz[i] = np.mean(TIz[0][i,:])
# ti = np.power(np.power(tix,2) + np.power(tiy,2) + np.power(tiz,2) ,0.5)
tix = flt_seq(tix,20)
tiy = flt_seq(tiy,20)
tiz = flt_seq(tiz,20)
plt.plot(tix[::12]*100, z[::12], 'b-', linewidth = 2, label='NBL-TIx')
plt.plot(tiy[::12]*100, z[::12], 'b--', linewidth = 2, label='NBL-TIy')
plt.plot(tiz[::12]*100, z[::12], 'b:', linewidth = 2, label='NBL-TIz')

tix = np.zeros((z.shape))
tiy = np.zeros((z.shape))
tiz = np.zeros((z.shape))
for i in range(z.shape[0]):
    tix[i] = np.mean(TIx[1][i,:])
    tiy[i] = np.mean(TIy[1][i,:])
    tiz[i] = np.mean(TIz[1][i,:])
# ti = np.power(np.power(tix,2) + np.power(tiy,2) + np.power(tiz,2) ,0.5)
tix = flt_seq(tix,20)
tiy = flt_seq(tiy,20)
tiz = flt_seq(tiz,20)
plt.plot(tix[::12]*100, z[::12], 'r-', linewidth = 2, label='CBL-TIx')
plt.plot(tiy[::12]*100, z[::12], 'r--', linewidth = 2, label='CBL-TIy')
plt.plot(tiz[::12]*100, z[::12], 'r:', linewidth = 2, label='CBL-TIz')

plt.ylabel('z(m)')
plt.xlabel('TI(%)')
plt.xlim(0, 14, 2)
plt.ylim(0, 300, 2)
legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
plt.grid()
plt.show()
