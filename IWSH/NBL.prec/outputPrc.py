
import matplotlib.pyplot as plt
import outputReadClass
from outputReadClass import *

''' 建立字典C准备储存各个算例的结果 '''
C = {}
caseName = {1:'1-3t-0D', 2:'2-3t-0.25D', 3:'3-3t-0.5D', 4:'4-3t-0.75D', 5:'5-3t-1t', 6:'6-3t-2t'}
''' case information '''
projDir = '/home/rao/OpenFOAM/nx-2.3.1-winfarm-v3.0/clusterproject-hub/wakeMerge/' # directory of the project
C[1] = Output(projDir_=projDir, caseName_=caseName[1], nTurbine_=3)
C[2] = Output(projDir_=projDir, caseName_=caseName[2], nTurbine_=3)
C[3] = Output(projDir_=projDir, caseName_=caseName[3], nTurbine_=3)
C[4] = Output(projDir_=projDir, caseName_=caseName[4], nTurbine_=3)
C[5] = Output(projDir_=projDir, caseName_=caseName[5], nTurbine_=1)
C[6] = Output(projDir_=projDir, caseName_=caseName[6], nTurbine_=2)

for i in range(1,7):
    C[i].P = C[i].powerRotor(200) # C[i].P[i] now is a dict containing powerRotor data of all the turbines
    C[i].T = C[i].thrust(200)

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


''' plot power curve '''
case = 2
plt.figure(figsize = (8, 4))
x = C[case].P[0][::10,0]
y = C[case].P[0][::10,1]/1e6
plt.plot(x, y, 'r-', linewidth = 1)
x = C[case].P[1][::10,0]
y = C[case].P[1][::10,1]/1e6
plt.plot(x, y, 'g-', linewidth = 1)
x = C[case].P[2][::10,0]
y = C[case].P[2][::10,1]/1e6
plt.plot(x, y, 'b-', linewidth = 1)
plt.ylabel('Power(MW)')
plt.xlabel('T(s)')
plt.title('Power Time Series')
plt.xlim(200,320)
plt.ylim(0,8)
plt.grid()
plt.show()
