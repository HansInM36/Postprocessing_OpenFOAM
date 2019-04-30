import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import wakeDataClass
from wakeDataClass import *

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

sec_18200_fd = secNz.fSec_t(6,'18200')
