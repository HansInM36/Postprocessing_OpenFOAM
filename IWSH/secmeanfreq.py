import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt

''' loads the probeData '''
# directories
projDir = '/media/nx/Ubuntu/myproject/IWSH/'
caseDict = {0:'uniIn', 1:'turbIn-0.2', 2:'NBL.succ.newdomain.56cores'}

probeData = {} # original probeDataDict of all cases
probeData_ave = {}

case = 0
f = open(projDir + 'postProcessing_all/' + caseDict[case] + '_probeData', 'rb')
probeData[case] = pickle.load(f) # all wake information of the case
f.close()
case = 1
f = open(projDir + 'postProcessing_all/' + caseDict[case] + '_probeData', 'rb')
probeData[case] = pickle.load(f) # all wake information of the case
f.close()
case = 2
f = open(projDir + 'postProcessing_all/' + caseDict[case] + '_probeData', 'rb')
probeData[case] = pickle.load(f) # all wake information of the case
f.close()
