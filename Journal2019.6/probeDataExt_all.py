import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np

''' directories '''
projDir = '/home/rao/myproject/Journal2019.6/'
probes = ['probe0', 'probe1', 'probe2']
caseName = 'CBL'
probeDataDict_temp = {}
probeDataDict = dict(zip(probes,probes))

for probe in probes:
    f = open(projDir + 'postProcessing_all/data.org/' + caseName + '_' + probe +'_probeData', 'rb')
    probeDataDict_temp[probe] = pickle.load(f) # all wake information of the case
    f.close()

''' save probeDataDict into a file with pickle '''
f = open(projDir + 'postProcessing_all/data.org/' + caseName + '_probeData', 'wb')
pickle.dump(probeDataDict_temp, f)
f.close()
