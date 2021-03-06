import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import signalClass as sgn

projDir = '/media/nx/Ubuntu1/myproject/IWSH/'

''' load original wake data '''
caseName = {0:'uniIn', 1:'turbIn-0.2', 2:'NBL.succ.newdomain.56cores'}

sec = 'PlaneZ'

x = {}
y = {}
z = {}

''' 读入 case2 的信息 '''
wake = {} # 把 wakeDataDict 中的信息以 Wake 类的形式储存
wakeSec = {}
secData = {}

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

wakeSec[2] = Sec(wakeDataDict)
del wakeDataDict

VSeq = {}
VSeq['4D'] = wakeSec[2].fSec_p(3,(880,400,90))
VSeq['6D'] = wakeSec[2].fSec_p(3,(1132,400,90))
VSeq['8D'] = wakeSec[2].fSec_p(3,(1384,400,90))
VSeq['10D'] = wakeSec[2].fSec_p(3,(1636,400,90))

seq = VSeq['6D'][:,0]
seqMean = np.mean(seq)
timeList = wakeSec[2].timeList
x = linspace(0,120,241)
y = seq -seqMean
plt.plot(x.T, y.T, 'r-', linewidth = 1)
plt.show()
signal = sgn.SignalSeq(seq-seqMean)
x = signal.PSE_t_AM(2)[0,:]
x = x*126/11.4
y = signal.PSE_t_AM(2)[1,:]
plt.semilogx(x.T[1:], y.T[1:], 'ro-', linewidth = 1)
plt.show()
