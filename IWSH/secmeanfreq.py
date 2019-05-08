import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import signalClass
from signalClass import *

''' loads the probeData '''
# directories
projDir = '/media/nx/Ubuntu/myproject/IWSH/'
caseDict = {0:'uniIn', 1:'turbIn-0.2', 2:'NBL.succ.newdomain.56cores'}

probeData = {} # original probeDataDict of all cases
probeData_ave = {}

pNum = 9

for case in [0,1,2]:
    f = open(projDir + 'postProcessing_all/' + caseDict[case] + '_probeData', 'rb')
    probeData[case] = pickle.load(f) # all wake information of the case
    f.close()

case = 2
pn = list(range(pNum))
tseq = {}
for p in pn:
    timeList = list(probeData[case].keys())
    timeList.sort()
    N = len(timeList)
    # tseq[p] = np.zeros(N)
    tseq[p] = {}
    for axis in ['x', 'y', 'z']:
        tseq[p][axis] = np.zeros(N)
    axisDict = {'x':3, 'y':4, 'z':5} # {'x':3, 'y':4, 'z':5} for SOWFA; {'x':4, 'y':3, 'z':5} for ALMSolver
    for axis in ['x', 'y', 'z']:
        for i in range(N):
            tseq[p][axis][i] = probeData[case][timeList[i]][p,axisDict[axis]]

p = 8
for ax in ['x', 'y', 'z']:
    tseq[p][ax] = tseq[p][ax] - mean(tseq[p][ax])
    tseq[p][ax] = SignalSeq(tseq[p][ax])
fseq = tseq[p]['x'].PSE_t_AM(50)[0,:]
vxseq = tseq[p]['x'].PSE_t_AM(50)[1,:]
vyseq = tseq[p]['y'].PSE_t_AM(50)[1,:]
vzseq = tseq[p]['z'].PSE_t_AM(50)[1,:]
fseq[0] = fseq[0] + 0.001
plt.semilogx(fseq, vxseq, 'r--', linewidth = 2)
plt.semilogx(fseq, vyseq, 'b-.', linewidth = 2)
plt.semilogx(fseq, vzseq, 'g:', linewidth = 2)
plt.xlim(0.001,100)
plt.show()
