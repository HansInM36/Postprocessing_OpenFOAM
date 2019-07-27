
import matplotlib.pyplot as plt
import outputReadClass
from outputReadClass import *

''' 建立字典C准备储存各个算例的结果 '''
C = {}
caseName = {0:'NBL.2T', 1:'NBL.2T.5D', 2:'NBL.2T.9D', 3:'CBL.2T',4:'CBL.2T.5D', 5:'CBL.2T.9D'}

''' case information '''
projDir = '/home/rao/myproject/Journal2019.6/' # directory of the project

for i in range(6):
    C[i] = Output(projDir_=projDir, caseName_=caseName[i], nTurbine_=2, deltat_=0.02)
    C[i].P = C[i].powerRotor()
    C[i].T = C[i].thrust()

''' plot power curve '''
cn = 2
plt.figure(figsize = (8, 4))
x = C[cn].P[0][12000:,0]-18240
y = C[cn].P[0][12000:,1]/1e6
plt.plot(x, y, 'r-', linewidth = 1)
plt.ylabel('Power(MW)')
plt.xlabel('t(s)')
plt.title('Power Time Series')
plt.xlim(0,600)
plt.ylim(0,8)
plt.grid()
plt.show()

''' plot average power bar '''
TNBL = [mean(C[0].T[0][12000:,1]), mean(C[1].T[1][12000:,1]), mean(C[0].T[1][12000:,1]), mean(C[2].T[1][12000:,1])]
TCBL = [mean(C[3].T[0][12000:,1]), mean(C[4].T[1][12000:,1]), mean(C[3].T[1][12000:,1]), mean(C[5].T[1][12000:,1])]

index = np.arange(4)+1
bar_width = 0.3
plt.figure(figsize = (8, 6))
plt.bar(index[0] - 0.5*bar_width, TNBL[0]/1e3, width=bar_width, color='darkblue', label='T1')
plt.bar(index[1] - 0.5*bar_width, TNBL[1]/1e3, width=bar_width, color='skyblue', label='T2-5D')
plt.bar(index[2] - 0.5*bar_width, TNBL[2]/1e3, width=bar_width, color='dodgerblue', label='T2-7D')
plt.bar(index[3] - 0.5*bar_width, TNBL[3]/1e3, width=bar_width, color='royalblue', label='T2-9D')
plt.bar(index[0] + 0.5*bar_width, TCBL[0]/1e3, width=bar_width, color='darkred', label='T1')
plt.bar(index[1] + 0.5*bar_width, TCBL[1]/1e3, width=bar_width, color='lightcoral', label='T2-5D')
plt.bar(index[2] + 0.5*bar_width, TCBL[2]/1e3, width=bar_width, color='tomato', label='T2-7D')
plt.bar(index[3] + 0.5*bar_width, TCBL[3]/1e3, width=bar_width, color='r', label='T2-9D')
# plt.legend()
plt.ylim(0,8e2)
plt.grid()
plt.show()

''' plot standard bar '''
stdNBL = [std(C[0].T[0][12000:,1]), std(C[1].T[1][12000:,1]), std(C[0].T[1][12000:,1]), std(C[2].T[1][12000:,1])]
stdCBL = [std(C[3].T[0][12000:,1]), std(C[4].T[1][12000:,1]), std(C[3].T[1][12000:,1]), std(C[5].T[1][12000:,1])]

index = np.arange(4)+1
bar_width = 0.3
plt.figure(figsize = (8, 6))

plt.bar(index[0] - 0.5*bar_width, stdNBL[0]/1e3, width=bar_width, color='darkblue', label='T1')
plt.bar(index[1] - 0.5*bar_width, stdNBL[1]/1e3, width=bar_width, color='skyblue', label='T2-5D')
plt.bar(index[2] - 0.5*bar_width, stdNBL[2]/1e3, width=bar_width, color='dodgerblue', label='T2-7D')
plt.bar(index[3] - 0.5*bar_width, stdNBL[3]/1e3, width=bar_width, color='royalblue', label='T2-9D')
plt.bar(index[0] + 0.5*bar_width, stdCBL[0]/1e3, width=bar_width, color='darkred', label='T1')
plt.bar(index[1] + 0.5*bar_width, stdCBL[1]/1e3, width=bar_width, color='lightcoral', label='T2-5D')
plt.bar(index[2] + 0.5*bar_width, stdCBL[2]/1e3, width=bar_width, color='tomato', label='T2-7D')
plt.bar(index[3] + 0.5*bar_width, stdCBL[3]/1e3, width=bar_width, color='r', label='T2-9D')
plt.ylim(0,50)
plt.grid()
plt.show()


''' plot average power bar '''
P_T1 = [ave(C[1].P[0])/1e6, ave(C[2].P[0])/1e6, ave(C[3].P[0])/1e6, ave(C[4].P[0])/1e6, ave(C[5].P[0])/1e6, ave(C[6].P[0])/1e6]
P_T2 = [ave(C[1].P[1])/1e6, ave(C[2].P[1])/1e6, ave(C[3].P[1])/1e6, ave(C[4].P[1])/1e6, 0, 0]
P_T3 = [ave(C[1].P[2])/1e6, ave(C[2].P[2])/1e6, ave(C[3].P[2])/1e6, ave(C[4].P[2])/1e6, 0, ave(C[6].P[1])/1e6] # 注意这里case6中的T3对应的是P[1]
index = np.arange(6)+1
bar_width = 0.3
plt.bar(index + bar_width*-1, P_T1, width=0.3, color='r', label='T1')
plt.bar(index + bar_width*0, P_T2, width=0.3, color='g', label='T2')
plt.bar(index + bar_width*1, P_T3, width=0.3, color='b', label='T3')
for x,y in zip(index, P_T1):
    plt.text(x + bar_width*-1, y + 0.04, '%.2f' % y, ha='center', va='bottom', fontsize=7)
for x,y in zip(index, P_T2):
    plt.text(x + bar_width*0, y + 0.04, '%.2f' % y, ha='center', va='bottom', fontsize=7)
for x,y in zip(index, P_T3):
    plt.text(x + bar_width*1, y + 0.04, '%.2f' % y, ha='center', va='bottom', fontsize=7)
plt.legend()
plt.xlabel('case number')
plt.ylabel('aeroPower(MW)')
plt.show()

''' plot average thrust bar '''
T_T1 = [ave(C[1].T[0])/1e3, ave(C[2].T[0])/1e3, ave(C[3].T[0])/1e3, ave(C[4].T[0])/1e3, ave(C[5].T[0])/1e3, ave(C[6].T[0])/1e3]
T_T2 = [ave(C[1].T[1])/1e3, ave(C[2].T[1])/1e3, ave(C[3].T[1])/1e3, ave(C[4].T[1])/1e3, 0, 0]
T_T3 = [ave(C[1].T[2])/1e3, ave(C[2].T[2])/1e3, ave(C[3].T[2])/1e3, ave(C[4].T[2])/1e3, 0, ave(C[6].T[1])/1e3] # 注意这里case6中的T3对应的是P[1]
index = np.arange(6)+1
bar_width = 0.2
plt.bar(index + bar_width*-1, T_T1, width=0.2, color='r', label='T1')
plt.bar(index + bar_width*0, T_T2, width=0.2, color='g', label='T2')
plt.bar(index + bar_width*1, T_T3, width=0.2, color='b', label='T3')
font = {'family':'DejaVuSans', 'weight':'normal', 'size':12}
plt.legend(font)
plt.xlabel('case number', font)
plt.xticks(index, [1,2,3,4,5,6]) # index 指出了对应位置，后面的列表中写对应位置的标注
plt.ylabel('aeroThrust(kN)', font)
plt.title('Power Bars')
plt.show()
