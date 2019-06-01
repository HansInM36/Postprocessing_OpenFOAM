import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np

''' directories '''
projDir = '/home/rao/myproject/ICCM2019/'
probes = ['probe0', 'probe0Dy', 'probe0Dz','probe2Dy', 'probe2Dz', 'probe4Dy', 'probe4Dz',\
'probe6Dy', 'probe6Dz','probe8Dy', 'probe8Dz', 'probe10Dy', 'probe10Dz']
caseName = 'NBL.succ.254deg.11.4.0.001'
probeDataDict_temp = {}
probeDataDict = dict(zip(probes,probes))

for probe in probes:
    f = open(projDir + 'postProcessing_all/' + caseName + '_' + probe +'_probeData', 'rb')
    probeDataDict_temp[probe] = pickle.load(f) # all wake information of the case
    f.close()

''' save probeDataDict into a file with pickle '''
f = open(projDir + 'postProcessing_all/' + caseName + '_probeData', 'wb')
pickle.dump(probeDataDict_temp, f)
f.close()
