import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np

''' directories '''
projDir = '/media/nx/Ubuntu/myproject/IWSH/'
probes = ['probe1']
caseName = 'NBL.succ.newdomain.56cores'
probeDataDict_temp = {}

for probe in probes:
    f = open(projDir + 'postProcessing_all/' + caseName + '_' + probe +'_probeData', 'rb')
    probeDataDict_temp[probe] = pickle.load(f) # all wake information of the case
    f.close()

timeList = list(probeDataDict_temp[probes[0]].keys()) # find the timeList (for every probe, the timeList should be the same)

probeDataDict = dict(zip(timeList,timeList))
for t in timeList:
    probeDataDict[t] = None
for t in timeList:
    for probe in probes:
        if type(probeDataDict[t]) != type(probeDataDict_temp[probe][t]):
            probeDataDict[t] = probeDataDict_temp[probe][t]
        else:
            probeDataDict[t] = np.vstack(probeDataDict[t],probeDataDict_temp[probe][t])

''' save probeDataDict into a file with pickle '''
f = open(projDir + 'postProcessing_all/' + caseName + '_probeData', 'wb')
pickle.dump(probeDataDict, f)
f.close()
