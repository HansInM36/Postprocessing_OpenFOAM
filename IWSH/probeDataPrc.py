import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt

''' loads the probeData '''
# directories
projDir = '/home/rao/myproject/IWSH2019/'
case = {0:'NBL.prec.newdomain.56cores'}

probeData = {} # original probeDataDict of all cases
probeData_ave = {}

f = open(projDir + 'postProcessing_all/' + case[0] + '_probeData', 'rb')
probeData[0] = pickle.load(f) # all wake information of the case
f.close()
''' end '''

''' Vx vertical profile '''
caseNo = 0
timeList = list(probeData[caseNo].keys())
tNum = len(timeList)
probeData_ave[caseNo] = None
for time in timeList:
    if type(probeData_ave[caseNo]) != type(probeData[caseNo][time]):
        probeData_ave[caseNo] = probeData[caseNo][time]
    else:
        probeData_ave[caseNo][:,3:] += probeData[caseNo][time][:,3:]
probeData_ave[caseNo][:,3:] /= tNum

plt.figure(figsize = (8, 4))
x = probeData_ave[caseNo][0:7,3]
y = probeData_ave[caseNo][0:7,2]
plt.plot(x, y, 'ro-', linewidth = 1)
plt.ylabel('z(m)')
plt.xlabel('Vx(m/s)')
plt.title('Vx vertical profile')
plt.xlim(0, 18, 0.5)
plt.grid()
plt.show()
