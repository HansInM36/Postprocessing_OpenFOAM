import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np

''' directories '''
projDir = '/home/rao/myproject/Journal2019.6/'
probes = ['probe-3Dy', 'probe-3Dz', 'probe2Dy', 'probe2Dz', 'probe3Dy', 'probe3Dz', 'probe4Dy', 'probe4Dz', 'probe5Dy', 'probe5Dz',
          'probe6Dy', 'probe6Dz', 'probe7Dy', 'probe7Dz', 'probe8Dy', 'probe8Dz', 'probe9Dy', 'probe9Dz', 'probe10Dy', 'probe10Dz',
          'probe11Dy', 'probe11Dz', 'probe12Dy', 'probe12Dz']
caseName = 'NBL.1T'
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
