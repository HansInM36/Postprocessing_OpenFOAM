import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np

''' directories '''
projDir = '/home/rao/myproject/ICCM2019/'
probes = ['probe4Dy', 'probe7Dy', 'probe10Dy']
caseName = 'NBL.succ.0.001.m30'
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
