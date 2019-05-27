import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import signalClass
from signalClass import *

''' loads the probeData '''
# directories
projDir = '/media/nx/Ubuntu1/myproject/IWSH/'
caseDict = {0:'uniIn', 1:'turbIn-0.2', 2:'NBL.succ.newdomain.56cores'}

probeData = {} # original probeDataDict of all cases
probeData_ave = {}

pNum = 9

for case in [0,1,2]:
    f = open(projDir + 'postProcessing_all/' + caseDict[case] + '_probeData', 'rb')
    probeData[case] = pickle.load(f) # all wake information of the case
    f.close()

tseqDict = {}
for case in [2]:
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
        tseqDict[case] = tseq

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
tseqDict[case] = tseq

# p = 0
# for case in [0,1,2]:
#     for ax in ['x', 'y', 'z']:
#         tseqDict[case][p][ax] = tseqDict[case][p][ax] - mean(tseqDict[case][p][ax])
#         tseqDict[case][p][ax] = SignalSeq(tseqDict[case][p][ax])
# fseq0 = tseqDict[0][p]['x'].PSE_t_AM(50)[0,:]
# vxseq0 = tseqDict[0][p]['x'].PSE_t_AM(50)[1,:]
# fseq1 = tseqDict[1][p]['x'].PSE_t_AM(50)[0,:]
# vxseq1 = tseqDict[1][p]['x'].PSE_t_AM(50)[1,:]
# fseq2 = tseqDict[2][p]['x'].PSE_t_AM(50)[0,:]
# vxseq2 = tseqDict[2][p]['x'].PSE_t_AM(50)[1,:]
# # vyseq = tseq[p]['y'].PSE_t_AM(50)[1,:]
# # vzseq = tseq[p]['z'].PSE_t_AM(50)[1,:]
# fseq0[0] = fseq0[0] + 0.0001
# fseq1[0] = fseq1[0] + 0.0001
# fseq2[0] = fseq2[0] + 0.0001
# plt.semilogx(fseq0*126/11.4, vxseq0/126/11.4, 'g:', linewidth = 1, label='case0')
# plt.semilogx(fseq1*126/11.4, vxseq1/126/11.4, 'b-.', linewidth = 1, label='case1')
# plt.semilogx(fseq2*126/11.4, vxseq2/126/11.4, 'r--', linewidth = 1, label='case2')
# # plt.semilogx(fseq, vyseq, 'b-.', linewidth = 2)
# # plt.semilogx(fseq, vzseq, 'g:', linewidth = 2)
# plt.xlim(0.01,100)
# plt.ylim(0,0.8)
# plt.legend(loc='upper right', fontsize=12)
# plt.grid()
# plt.show()

p = 2
for case in [2]:
    for ax in ['x']:
        tseqDict[case][p][ax] = tseqDict[case][p][ax] - mean(tseqDict[case][p][ax])
        tseqDict[case][p][ax] = SignalSeq(tseqDict[case][p][ax])
fseq2 = tseqDict[2][p]['x'].PSE_t_AM(50)[0,:]
vxseq2 = tseqDict[2][p]['x'].PSE_t_AM(50)[1,:]
fseq2[0] = fseq2[0] + 0.0001
plt.semilogx(fseq2*126/11.4, vxseq2/126/11.4, 'g:', linewidth = 1, label='x=4D')
plt.semilogx(fseq2*126/11.4, vxseq2/126/11.4, 'b-.', linewidth = 1, label='x=6D')
plt.semilogx(fseq2*126/11.4, vxseq2/126/11.4, 'r--', linewidth = 1, label='x=8D')
plt.semilogx(fseq2*126/11.4, vxseq2/126/11.4, 'y-', linewidth = 1, label='x=10D')
# plt.semilogx(fseq, vyseq, 'b-.', linewidth = 2)
# plt.semilogx(fseq, vzseq, 'g:', linewidth = 2)
plt.xlim(0.01,100)
plt.ylim(0,0.8)
plt.legend(loc='upper right', fontsize=12)
plt.grid()
plt.show()

# test
y = tseqDict[2][0]['x'].X
x = np.linspace(0,120,6001)
plt.plot(x,y, 'r-', linewidth = 1)
plt.grid()
plt.show()
