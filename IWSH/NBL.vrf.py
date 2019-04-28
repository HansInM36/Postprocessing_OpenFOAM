import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
import fitting as fit

projDir = '/home/rao/myproject/IWSH2019/'

''' load original wake data '''
caseName = {0:'NBL.prec.newdomain.56cores'}

secList = ['Sec0','Sec6','Sec11']

wakeDataDict = {} # 存储所有的原始尾流信息

wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wake_ave = {} # 求出所有 case 中尾流的时均值并存入该字典
wake_TI = {} # 求出所有 case 中尾流的湍流强度并存入该字典
ave = {} # wake_ave 的网格化版本
TI = {} # wake_ave 的网格化版本

secDataDict = {}
for sec in secList:
    f = open(projDir + 'postProcessing_all/' + caseName[0] + '_' + sec + '_Data', 'rb')
    secDataDict[sec] = pickle.load(f) # all wake information of the case
    f.close()
timeList = list(secDataDict[secList[0]].keys())
for time in timeList:
    for sec in secList:
        wakeDataDict[time] = {}
for time in timeList:
    for sec in secList:
        wakeDataDict[time][sec] = secDataDict[sec][time][sec]


# x0 = [2,10,18.5,27,42.5,58.5,74,90,106,121.5,153,200,250,300,350,400,450,500,550,600,650,700,750,800]
# y0 = [3.2,6.3,8.4,9.1,9.9,10.4,11.0,11.3,11.5,11.7,12.3,12.8,13.0,13.45,13.96,14.49,14.92,15.13,15.43,15.81,16.3,16.99,18.16,17.52]
# x0 = np.array(x)
# y0 = np.array(y)
#
# from pylab import mpl
# from matplotlib.gridspec import GridSpec
#
# fig = plt.figure(1, figsize=(8, 6))
# fig.subplots_adjust(bottom=0.2)
# ax = {}
# gs = GridSpec(1,3)
# title = {0:'Vx profile (80m)', 1:'Vx profile (200m)', 2:'Vx profile (400m)', 3:'Vx profile (520m)'}
# for i in range(0,3):
#     ax[i] = plt.subplot(gs[0, int(i)])
#
# ax[0].plot(x, y, 'ro-', linewidth=1, label='')
# ax[1].plot(x, y, 'bo-', linewidth=1, label='')
# ax[2].plot(x, y, 'bo-', linewidth=1, label='')
# ax[i].set_ylabel('z(m)')
# ax[i].set_xlabel('Vx(m/s)')
# ax[i].set_title(title[i])
# ax[i].set_xlim(0, 15, 0.5)
# legend = ax[i].legend(loc='upper left', fontsize='x-large')
# ax[i].grid()
# plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
# plt.show()
