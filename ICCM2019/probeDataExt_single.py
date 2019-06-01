import os
import csv
import numpy as np
from numpy import *
import pickle

# the directory where the wake data locate
projDir = '/home/rao/myproject/ICCM2019/'

caseName = 'NBL.succ.0.001.m30'
probe = 'probe10Dz'
caseDir = caseName + '/postProcessing/'
startT = 18240
stopT = 18600
deltaT = 0.02

startTimeList = os.listdir(projDir + caseDir + probe + '/' + '.')
startTimeList.sort()

# initialize a dict storing wake data in each section of each time step
probeDataDict = dict()

for startTime in startTimeList:
    # preprocessing of the original file: deleting all the ' ', '(', ')'
    file = open(projDir + caseDir + probe + '/' + startTime + '/' + 'U.csv', 'r')
    data = csv.reader(file, delimiter=' ')
    rows = [row for row in data]
    for row in rows:
        while '' in row:
            row.remove('')
        for index in range(len(row)):
            while '(' in row[index]:
                row[index] = row[index].replace('(','')
            while ')' in row[index]:
                row[index] = row[index].replace(')','')
    file = open(projDir + caseDir + probe + '/' + startTime + '/' + 'U.processed.csv', 'w') #create a new file named U.temp.csv
    writer = csv.writer(file)
    writer.writerows(rows)

    file = open(projDir + caseDir + probe + '/' + startTime + '/' + 'U.processed.csv', 'r')
    data = csv.reader(file)
    rows = [row for row in data]

    pNum = len(rows[0]) - 2
    timeList = [row[0] for row in rows[4:]]
    timeList.sort()
    i = 0
    while round(float(timeList[i]),2) < startT:
        i += 1
    j = 0
    while round(float(timeList[j]),2) != stopT:
        j += 1
    rstart = i
    rstop = j

    for i in range(rstart,rstop+1):
        probeData = array(zeros((pNum,6)))
        probeData[:,0] = array(rows[0][2:]) # record x coordinate
        probeData[:,1] = array(rows[1][2:]) # record y coordinate
        probeData[:,2] = array(rows[2][2:]) # record z coordinate
        for j in range(pNum):
            probeData[j,3:] = array(rows[i+4][j*3+1:j*3+4])
        t = round(startT + 0.02*(i-rstart),2)
        probeDataDict[str(t)] = probeData


''' save probeDataDict into a file with pickle '''
f = open(projDir + 'postProcessing_all/' + caseName + '_' + probe + '_probeData', 'wb')
pickle.dump(probeDataDict, f)
f.close()
