import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import fitting as ft
import trsMat as tM
import wakeDataClass
from wakeDataClass import *
import signalClass as sgn

''' 获取meandering速度序列 '''
# directories
projDir = '/home/rao/myproject/Journal2019.6/'
case = {0:'NBL.1T', 1:'CBL.1T'}


# # meandering 时历序列
# cn = 0
# prb = 'probe5Dy'
# # plt.figure(figsize = (7, 4))
# # cl = {0:'b-', 1:'r-', 2:'b-', 3:'r-'}
# # lb = {0:'NBL', 1:'CBL', 2:'NBL', 3:'CBL'}
# # for cn in [2,3]:
# #     plt.plot(wcb[cn][prb][:,0]-18240, wcb[cn][prb][:,1]/63, cl[cn], linewidth = 1, label=lb[cn])
# # plt.xlim(0, 600)
# # legend = plt.legend(loc='upper right', shadow=False, fontsize='x-large')
# # plt.grid()
# # plt.show()
# mdrSeq = wcb[cn][prb][:,1]
# tSeq = wcb[cn][prb][:,0]-18240
# mdrvSeq = sgn.drv_seq(mdrSeq,tSeq)

cn = 1

''' 获取湍流入流横向速度序列 '''
sec = 'Sec-3D'

# 建立一些空字典
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存

''' assemble all the data of different secs in wakeDataDict '''
wakeDataDict = {} # 存储所有的原始尾流信息
f = open(projDir + 'postProcessing_all/data.org/' + case[cn] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()

wake[cn] = Wake(wakeData_org)
del wakeData_org # 汇总完了删除这个临时字典
secData = wake[cn].wakeData

timeList = list(wake[cn].wakeData.keys())
timeList.sort()

N = len(timeList)

drvV = np.zeros(N)
drvW = np.zeros(N)

for i in range(N):
    print(round(i/N*100,2), '%', ' finished ......')
    secData[timeList[i]][sec][:,1:] = tM.trs(secData[timeList[i]][sec][:,1:])
    pNum = secData[timeList[i]][sec].shape[0]
    count = 0
    v_ave = 0
    w_ave = 0
    for j in range(pNum):
        if np.power((secData[timeList[i]][sec][j,2]-0)**2 + (secData[timeList[i]][sec][j,3]-90)**2,0.5) < 1.0*126:
            count += 1
            v_ave += secData[timeList[i]][sec][j,5]
            w_ave += secData[timeList[i]][sec][j,6]
    drvV[i] = v_ave / count
    drvW[i] = w_ave / count

drvV = flt_seq(drvV, 3)
drvW = flt_seq(drvW, 3)

''' 获取meandering速度序列 '''
sec = 'Sec12D'

# 建立一些空字典
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存

''' assemble all the data of different secs in wakeDataDict '''
# 读取 u0
f = open(projDir + 'postProcessing_all/data.processed/' + case[cn] + '_' + 'PlaneY' + '_u0', 'rb')
u0_org = pickle.load(f) # all wake information of the case
f.close()

wakeDataDict = {} # 存储所有的原始尾流信息
f = open(projDir + 'postProcessing_all/data.org/' + case[cn] + '_' + sec + '_wakeData', 'rb')
wakeData_org = pickle.load(f) # all wake information of the case
f.close()

wake[cn] = Wake(wakeData_org)
del wakeData_org # 汇总完了删除这个临时字典
secData_org = wake[cn].wakeData

timeList = list(wake[cn].wakeData.keys())
timeList.sort()

N = len(timeList)

mdrsh = np.zeros(N)
mdrsv = np.zeros(N)
mdrV = np.zeros(N)
mdrW = np.zeros(N)

secData = {}
for n in range(N):
    secData[timeList[n]] = secData_org[timeList[n]][sec]
    secData[timeList[n]][:,1:] = tM.trs(secData[timeList[n]][:,1:])
secData = Sec(secData)

for n in range(N):
    print(round(n/N*100,2), '%', ' finished ......')
    # secData[timeList[n]][sec][:,1:] = tM.trs(secData[timeList[n]][sec][:,1:])

    secdata = SecITP(secData.fSec_t(3,timeList[n]))
    secdata.meshITP_Nx((-252, 252, 504), (0, 378, 378))

    x = {}
    y = {}
    u = {}
    # 编织网格
    dx, dy = 1, 1
    x[cn], y[cn] = np.mgrid[slice(-252, 252 + dx, dx), slice(0, 378 + dy, dy)]
    x[cn] = x[cn].T
    y[cn] = y[cn].T
    # 向网格里填值
    u[cn] = np.array(zeros(shape(x[cn])))
    for row in secdata.meshData:
        i = int(row[0,2]/dx) # i是行，对应于z坐标
        j = int(row[0,1]/dy) # j是列，对应于y坐标
        u[cn][i,j+int(252/dy)] = row[0,3] # i和j是矩阵坐标，而不是计算与坐标，需要换算


    xx = x[cn][90,63:252+189+1]
    yy = u[cn][90,63:252+189+1]
    yy = 1 - yy/11.4
    miu, sgm = ft.fit_gs((0,30),xx,yy)
    # delta = (np.max(xx) - np.min(xx)) / (np.shape(xx)[0] - 1)
    # S = sum(yy)*delta - 0.5*(yy[np.where(xx==np.min(xx))] + yy[np.where(xx==np.max(xx))])
    # yyp = ft.func_gs((miu,sgm),xx)*S
    # plt.figure(figsize = (4, 9))
    # plt.plot(yy, xx, 'ro:', linewidth = 1, label='velocity deficit')
    # plt.plot(yyp, xx, 'k-', linewidth = 1, label='gaussian fitting curve')
    # plt.grid()
    # plt.show()
    mdrsh[n] = miu

    xx = y[cn][:90+189+1,252]
    yy = u[cn][:,252] / u0_org
    yy = (1 - yy)[:90+189+1]
    miu, sgm = ft.fit_gs((90,30),xx,yy)
    # delta = (np.max(xx) - np.min(xx)) / (np.shape(xx)[0] - 1)
    # S = sum(yy)*delta - 0.5*(yy[np.where(xx==np.min(xx))] + yy[np.where(xx==np.max(xx))])
    # yyp = ft.func_gs((miu,sgm),xx)*S
    # plt.figure(figsize = (4, 9))
    # plt.plot(yy, xx, 'ro:', linewidth = 1, label='velocity deficit')
    # plt.plot(yyp, xx, 'k-', linewidth = 1, label='gaussian fitting curve')
    # plt.grid()
    # plt.show()
    mdrsv[n] = miu - 90

tSeq = np.linspace(0,0.5*(N-1),N)
mdrV = sgn.drv_seq(mdrsh,tSeq)
mdrW = sgn.drv_seq(mdrsv,tSeq)

mdrsh_nrm = sgn.nrm_seq(mdrsh,tSeq)
mdrsv_nrm = sgn.nrm_seq(mdrsv,tSeq)
drvV_nrm = sgn.nrm_seq(drvV,tSeq)
drvW_nrm = sgn.nrm_seq(drvW,tSeq)

Rh = sgn.corr_seqs(drvV_nrm,mdrsh_nrm)
Rv = sgn.corr_seqs(drvW_nrm,mdrsv_nrm)

plt.figure(figsize = (8, 2.4))
# plt.plot(tSeq, mdrsh, 'r-', linewidth = 1, label='horizontal')
# plt.plot(tSeq, mdrsh_nrm, 'b-', linewidth = 1, label='vertical')
# plt.plot(tSeq, drvV_nrm, 'r-', linewidth = 1, label='horizontal')
# plt.plot(tSeq, mdrV, 'b-', linewidth = 1, label='vertical')
plt.plot(Rh[0,:]*0.5, Rh[1,:]*1e6, color='salmon', linestyle='-', linewidth = 1, label='horizontal')
plt.plot(Rv[0,:]*0.5, Rv[1,:]*1e6, color='firebrick', linestyle='-.', linewidth = 1, label='vertical')
legend = plt.legend(loc='upper right', shadow=False, fontsize=10)
plt.title('x=12D')
plt.grid()
plt.show()
