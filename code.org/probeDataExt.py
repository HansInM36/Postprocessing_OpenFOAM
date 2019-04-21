import os
import csv
import numpy as np
from numpy import *
import pickle

# the directory where the wake data locate
projDir = '/media/nx/Ubuntu1/case/IWSH/'

caseName = 'NBL.succ.newdomain.56cores'
caseDir = caseName + '/postProcessing/sampleP/'

timeList = os.listdir(projDir + caseDir + '.')
timeList.sort()

# initialize a dict storing wake data in each section of each time step
probeDataDict = dict(zip(timeList,timeList))

for time in timeList:
    # preprocessing of the original file: deleting all the ' ', '(', ')'
    file = open(projDir + caseDir + time + '/U.csv', 'r')
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
    file = open(projDir + caseDir + time + '/U.processed.csv', 'w') #create a new file named U.temp.csv
    writer = csv.writer(file)
    writer.writerows(rows)

    file = open(projDir + caseDir + time + '/U.processed.csv', 'r')
    data = csv.reader(file)
    rows = [row for row in data]

    pNum = len(rows[0]) - 2
    stepNum =

    probeData = array(zeros())
