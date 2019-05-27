import sys
from sys import path
import pickle  # for reading the original wake data
import numpy as np
import matplotlib.pyplot as plt
import fitting as fit

''' loads the probeData '''
# directories
projDir = '/media/nx/Ubuntu/myproject/ICCM2019/'
case = {0:'NBL.prec.254deg.11.4.0.001'}

probeData = {} # original probeDataDict of all cases
probeData_ave = {}

f = open(projDir + 'postProcessing_all/' + case[0] + '_probeData', 'rb')
probeData[0] = pickle.load(f) # all wake information of the case
f.close()
''' end '''
