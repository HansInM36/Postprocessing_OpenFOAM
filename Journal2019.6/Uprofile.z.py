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

probe = {0:'probe0Dz', 1:'probe2Dz', 2:'probe4Dz', 3:'probe6Dz', 4:'probe8Dz', 5:'probe10Dz'}

probeData = {} # original probeDataDict of all cases

for i in range(3):
    f = open(projDir + 'postProcessing_all/' + case[i] + '_probeData', 'rb')
    probeData[i] = pickle.load(f) # all wake information of the case
    f.close()
''' end '''

z = probeData[0][probe[1]]['18240.0'][:,2]
u0_ave = [ 8.87959837,  9.57736733,  9.9876305 , 10.27930275, 10.50578773,
       10.69096625, 10.84760629, 10.98334084, 11.06472259, 11.21024793,
       11.30719247, 11.39570815, 11.47714414, 11.55254955, 11.62275629,
       11.68843519, 11.75013506, 11.8083106 , 11.86334277, 11.91555393,
       11.96521923, 12.01257546, 12.05782782, 12.10115532, 12.14271504,
       12.19561543, 12.24590397, 12.29382649, 12.33959566, 12.3833967 ,
       12.42539192, 12.46572434, 12.50452064, 12.57794383, 12.64642923,
       12.71059934, 12.77096589, 12.82795466, 12.8819237 , 12.933177  ,
       12.98197482]
u0_ave = np.array(u0_ave) # 入流速度廓线
u_ave = {} # 负责记录每个算例每个橫截面的速度廓线
tNum = {}
timeList = {}
for i in range(3):
    u_ave[i] = {}
    tNum[i] = {}
    timeList[i] = {}
    for j in range(6):
        u_ave[i][j] = np.zeros(z.shape)
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
    plt.plot((u0_ave - u_ave[cn][j])/u0_ave + j, z, 'ko-', linewidth = 2)
plt.xticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5], [0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0, 0.5, 0 ,0.5])
plt.yticks([27, 90, 153, 216, 279, 342],[-1, 0, 1, 2, 3, 4])
plt.ylabel('r/R')
plt.grid()
plt.show()
