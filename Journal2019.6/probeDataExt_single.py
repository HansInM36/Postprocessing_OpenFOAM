import os
import csv
import numpy as np
from numpy import *
import pickle

# the directory where the wake data locate
projDir = '/home/rao/myproject/Journal2019.6/'

caseName = 'NBL.1T'
caseDir = caseName + '/postProcessing/'

probeList = ['probe-3Dy', 'probe-3Dz', 'probe2Dy', 'probe2Dz', 'probe3Dy', 'probe3Dz', 'probe4Dy', 'probe4Dz', 'probe5Dy', 'probe5Dz',
             'probe6Dy', 'probe6Dz', 'probe7Dy', 'probe7Dz', 'probe8Dy', 'probe8Dz', 'probe9Dy', 'probe9Dz', 'probe10Dy', 'probe10Dz',
             'probe11Dy', 'probe11Dz', 'probe12Dy', 'probe12Dz']

for probe in probeList:
    # 对于NBL算例
    startT = {'18000':18240, '18600':18600}
    stopT = {'18000':18530, '18600':18840}
    # 对于CBL算例
    # startT = {'18000':18240, '18600':18240}
    # stopT = {'18000':18840, '18600':18840}
    # deltaT = 0.02

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
        while round(float(timeList[i]),2) < startT[startTime]:
            i += 1
        j = 0
        while round(float(timeList[j]),2) != stopT[startTime]:
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
            t = round(startT[startTime] + 0.02*(i-rstart),2)
            probeDataDict[str(t)] = probeData


    ''' save probeDataDict into a file with pickle '''
    f = open(projDir + 'postProcessing_all/data.org/' + caseName + '_' + probe + '_probeData', 'wb')
    pickle.dump(probeDataDict, f)
    f.close()
