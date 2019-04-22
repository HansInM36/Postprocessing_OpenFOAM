import os
import csv
import numpy as np
from numpy import *
import pickle

''' functions tools '''
def strToNum_list(List):
    List = list(map(float, List))
    return List

def ave(Mat, t0=200, tn=320, col=1):
    " a function that computes the average of the outPut "
    row0 = int(np.where(Mat[:,0]==t0)[0])
    rown = int(np.where(Mat[:,0]==tn)[0])
    Mat = Mat[row0:rown,col]
    return np.mean(Mat)

class Output:
    # case information
    projDir = 0 # directory of the project
    caseName = 0 # name of the case
    nTurbine = 0 # number of turbines
    P = 0
    T = 0

    def __init__(self, projDir_, caseName_, nTurbine_):
        " constructor "
        self.projDir = projDir_
        self.caseName = caseName_
        self.nTurbine = nTurbine_
        self.P = 0
        self.T = 0

    def powerRotor(self, startTime):
        " read powerRotor and return a dict "
        turbines = list(range(0,self.nTurbine))
        file_powerRotor = open(self.projDir + self.caseName + '/turbineOutputofWindFarm/' + str(startTime) + '/powerRotor', 'r')
        data_powerRotor = csv.reader(file_powerRotor, delimiter=' ')
        rows_powerRotor = [row for row in data_powerRotor]
        powerRotorDict = dict(zip(turbines, turbines))
        for i in turbines:
            powerRotorDict[i] = mat([[float(row[1]), float(row[3])] for row in rows_powerRotor[i+1::(self.nTurbine+1)]])
        return powerRotorDict

    def thrust(self, startTime):
        " read thrust and return a dict "
        turbines = list(range(0,self.nTurbine))
        file_thrust = open(self.projDir + self.caseName + '/turbineOutputofWindFarm/' + str(startTime) + '/thrust', 'r')
        data_thrust = csv.reader(file_thrust, delimiter=' ')
        rows_thrust = [row for row in data_thrust]
        thrustDict = dict(zip(turbines, turbines))
        for i in turbines:
            thrustDict[i] = mat([[float(row[1]), float(row[3])] for row in rows_thrust[i+1::(self.nTurbine+1)]])
        return thrustDict
