import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import trsMat as tM

''' loads the probeData '''
# directories
projDir = '/home/rao/myproject/ICCM2019/'
case = {0:'NBL.succ.254deg.11.4.0.001', 1:'NBL.succ.0.001.30', 2:'NBL.succ.0.001.m30'}
# probe = {0:'probe0', 1:'probe0Dy', 2:'probe0Dz', 3:'probe2Dy', 4:'probe2Dz',\
# 5:'probe4Dy', 6:'probe4Dz', 7:'probe6Dy', 8:'probe6Dz', 9:'probe8Dy', 9:'probe8Dz',\
# 10:'probe10Dy', 11:'probe10Dz'}

probe = {0:'probe0Dy', 1:'probe2Dy', 2:'probe4Dy', 3:'probe6Dy', 4:'probe8Dy', 5:'probe10Dy'}

probeData = {} # original probeDataDict of all cases

for i in range(3):
    f = open(projDir + 'postProcessing_all/' + case[i] + '_probeData', 'rb')
    probeData[i] = pickle.load(f) # all wake information of the case
    f.close()
''' end '''

M_ = tM.trs(probeData[0][probe[1]]['18240.0'])
y = M_[:,1]
u_ave = {} # 负责记录每个算例每个橫截面的速度廓线
tNum = {}
timeList = {}
for i in range(3):
    u_ave[i] = {}
    tNum[i] = {}
    timeList[i] = {}
    for j in range(6):
        u_ave[i][j] = np.zeros(y.shape)
        timeList[i][j] = list(probeData[i][probe[j]].keys())
        timeList[i][j].sort()
        tNum[i][j] = len(timeList[i][j])
for i in range(3):
    for j in range(6):
        for time in timeList[i][j]:
            M_ = tM.trs(probeData[i][probe[j]][time])
            u_ave[i][j] += M_[:,3]
        u_ave[i][j] /= tNum[i][j]

cn = 2
plt.figure(figsize = (14, 6))
for j in range(6):
    plt.plot((11.4 - u_ave[cn][j])/11.4 + j, y, 'ko-', linewidth = 2)
plt.xticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5], [0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0 ,0.5])
plt.yticks([-252, -189, -126, -63, 0, 63, 126, 189, 252],[-4, -3, -2, -1, 0, 1, 2, 3, 4])
plt.ylabel('r/R')
plt.grid()
plt.show()
