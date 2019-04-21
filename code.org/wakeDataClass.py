import numpy as np
from numpy import *

class WakeSec:
    """ members """
    secData = 0
    meshData = 0
    meshData_horizAve = 0

    ''' constructor '''
    def __init__(self, wakeMat): # constructor
        self.secData = wakeMat # wakeMat is a mat of pNum*7 (the first column is the pointID)

    ''' functions '''
    def get_wakeData(self, wakeMat): # function for reassigning
        self.secData = wakeMat

    def segmentSum(self, inMat, segNum, uNumOfSeg):
        """ this function is for the compute of horizontal averaging mesh data """
        outMat = mat(zeros((segNum,1)))
        for i in range(0,segNum):
            outMat[i,0] = sum(inMat[i*uNumOfSeg:(i+1)*uNumOfSeg,0])
        outMat = outMat / uNumOfSeg
        return outMat

    def meshITP_Ny(self,x_axis,z_axis): # interpolate the original wake data and project it onto a structral mesh
        """ x_axis should be a tuple indicating the min, max value and the number of segments, like x_axis = (-240, 240, 60), and similarly the z_axis """
        pNum_x = x_axis[2] + 1
        pNum_z = z_axis[2] + 1
        delta_x = (x_axis[1] - x_axis[0])/x_axis[2]
        delta_z = (z_axis[1] - z_axis[0])/z_axis[2]
        coor_x = range(int(x_axis[0]), int(x_axis[1] + delta_x), int(delta_x))
        coor_z = range(int(z_axis[0]), int(z_axis[1] + delta_z), int(delta_z))
        coor_y = sum(self.secData[:,2])/shape(self.secData[:,2])[0] # all y coordinate are the same, because this is a section of yNormal
        coors_org = self.secData[:,1:4] # build the original points mat

        # compute mesh coordinates and velocities
        from scipy.interpolate import griddata
        [Xmesh, Zmesh] = meshgrid(coor_x, coor_z)
        Ymesh = mat(ones((shape(Xmesh)))) * coor_y
        Xmesh = Xmesh.ravel()
        Ymesh = Ymesh.ravel()
        Zmesh = Zmesh.ravel()
        coors_mesh = (vstack((Xmesh,Ymesh,Zmesh))).T # build the mesh points mat

        Vx = griddata(coors_org, self.secData[:,4], coors_mesh, method = 'nearest')
        Vy = griddata(coors_org, self.secData[:,5], coors_mesh, method = 'nearest')
        Vz = griddata(coors_org, self.secData[:,6], coors_mesh, method = 'nearest')
        V_mesh = hstack((Vx,Vy,Vz)) # interpolated velocity mat

        meshData = mat(zeros((pNum_x * pNum_z,6))) # initialize a mat storing interpolated meshData
        meshData[:,0:3] = coors_mesh
        meshData[:,3:6] = V_mesh
        self.meshData = meshData

        # compute the horizontally averaged mesh Data (only valid for Ny section)
        z_horizAve = self.segmentSum(meshData[:,2], pNum_z, pNum_x[2]+1)
        Vx_horizAve = self.segmentSum(meshData[:,3], pNum_z, pNum_x[2]+1)
        Vy_horizAve = self.segmentSum(meshData[:,4], pNum_z, pNum_x[2]+1)
        Vz_horizAve = self.segmentSum(meshData[:,5], pNum_z, pNum_x[2]+1)
        self.meshData_horizAve = {'z':z_horizAve, 'Vx':Vx_horizAve, 'Vy':Vy_horizAve, 'Vz':Vz_horizAve}

    def meshITP_Nx(self,y_axis,z_axis): # interpolate the original wake data and project it onto a structral mesh
        """ y_axis should be a tuple indicating the min, max value and the number of segments, like y_axis = (-240, 240, 60), and similarly the z_axis """
        pNum_y = y_axis[2] + 1
        pNum_z = z_axis[2] + 1
        delta_y = (y_axis[1] - y_axis[0])/y_axis[2]
        delta_z = (z_axis[1] - z_axis[0])/z_axis[2]
        coor_y = range(int(y_axis[0]), int(y_axis[1] + delta_y), int(delta_y))
        coor_z = range(int(z_axis[0]), int(z_axis[1] + delta_z), int(delta_z))
        coor_x = sum(self.secData[:,1])/shape(self.secData[:,1])[0] # all y coordinate are the same, because this is a section of yNormal
        coors_org = self.secData[:,1:4] # build the original points mat

        # compute mesh coordinates and velocities
        from scipy.interpolate import griddata
        [Ymesh, Zmesh] = meshgrid(coor_y, coor_z)
        Xmesh = mat(ones((shape(Ymesh)))) * coor_x
        Xmesh = Xmesh.ravel()
        Ymesh = Ymesh.ravel()
        Zmesh = Zmesh.ravel()
        coors_mesh = (vstack((Xmesh,Ymesh,Zmesh))).T # build the mesh points mat

        Vx = griddata(coors_org, self.secData[:,4], coors_mesh, method = 'nearest')
        Vy = griddata(coors_org, self.secData[:,5], coors_mesh, method = 'nearest')
        Vz = griddata(coors_org, self.secData[:,6], coors_mesh, method = 'nearest')
        V_mesh = hstack((Vx,Vy,Vz)) # interpolated velocity mat

        meshData = mat(zeros((pNum_y * pNum_z,6))) # initialize a mat storing interpolated meshData
        meshData[:,0:3] = coors_mesh
        meshData[:,3:6] = V_mesh
        self.meshData = meshData

        # compute the horizontally averaged mesh Data (only valid for Ny section)
        z_horizAve = self.segmentSum(meshData[:,2], pNum_z, pNum_y)
        Vx_horizAve = self.segmentSum(meshData[:,3], pNum_z, pNum_y)
        Vy_horizAve = self.segmentSum(meshData[:,4], pNum_z, pNum_y)
        Vz_horizAve = self.segmentSum(meshData[:,5], pNum_z, pNum_y)
        self.meshData_horizAve = {'z':z_horizAve, 'Vx':Vx_horizAve, 'Vy':Vy_horizAve, 'Vz':Vz_horizAve}

    def meshITP_Nz(self,x_axis,y_axis): # interpolate the original wake data and project it onto a structral mesh
        """ y_axis should be a tuple indicating the min, max value and the number of segments, like y_axis = (-240, 240, 60), and similarly the z_axis """
        pNum_x = x_axis[2] + 1
        pNum_y = y_axis[2] + 1
        delta_x = (x_axis[1] - x_axis[0])/x_axis[2]
        delta_y = (y_axis[1] - y_axis[0])/y_axis[2]
        coor_x = range(int(x_axis[0]), int(x_axis[1] + delta_x), int(delta_x))
        coor_y = range(int(y_axis[0]), int(y_axis[1] + delta_y), int(delta_y))
        coor_z = sum(self.secData[:,3])/shape(self.secData[:,3])[0] # all y coordinate are the same, because this is a section of yNormal
        coors_org = self.secData[:,1:4] # build the original points mat

        # compute mesh coordinates and velocities
        from scipy.interpolate import griddata
        [Xmesh, Ymesh] = meshgrid(coor_x, coor_y)
        Zmesh = mat(ones((shape(Ymesh)))) * coor_z
        Xmesh = Xmesh.ravel()
        Ymesh = Ymesh.ravel()
        Zmesh = Zmesh.ravel()
        coors_mesh = (vstack((Xmesh,Ymesh,Zmesh))).T # build the mesh points mat

        Vx = griddata(coors_org, self.secData[:,4], coors_mesh, method = 'nearest')
        Vy = griddata(coors_org, self.secData[:,5], coors_mesh, method = 'nearest')
        Vz = griddata(coors_org, self.secData[:,6], coors_mesh, method = 'nearest')
        V_mesh = hstack((Vx,Vy,Vz)) # interpolated velocity mat

        meshData = mat(zeros((pNum_x * pNum_y,6))) # initialize a mat storing interpolated meshData
        meshData[:,0:3] = coors_mesh
        meshData[:,3:6] = V_mesh
        self.meshData = meshData

    def x_cut(self, x):
        """ according to a x value, cut the meshData and extract the line data """
        cutData = {}
        index = where(self.meshData[:,0] == x)[0]
        cutData['y'] = self.meshData[index,1]
        cutData['z'] = self.meshData[index,2]
        cutData['Vx'] = self.meshData[index,-3]
        cutData['Vy'] = self.meshData[index,-2]
        cutData['Vz'] = self.meshData[index,-1]
        return cutData

    def y_cut(self, x):
        """ according to a x value, cut the meshData and extract the line data """
        cutData = {}
        index = where(self.meshData[:,1] == x)[0]
        cutData['x'] = self.meshData[index,0]
        cutData['z'] = self.meshData[index,2]
        cutData['Vx'] = self.meshData[index,-3]
        cutData['Vy'] = self.meshData[index,-2]
        cutData['Vz'] = self.meshData[index,-1]
        return cutData

    def z_cut(self, z):
        """ according to a z value, cut the meshData and extract the line data """
        cutData = {}
        index = where(self.meshData[:,2] == z)[0]
        cutData['x'] = self.meshData[index,0]
        cutData['y'] = self.meshData[index,1]
        cutData['Vx'] = self.meshData[index,-3]
        cutData['Vy'] = self.meshData[index,-2]
        cutData['Vz'] = self.meshData[index,-1]
        return cutData


class Wake:
    """ members """
    wakeData = 0 # wake data dict
    timeList = 0
    startTime = 0
    stopTime = 0
    tNum = 0

    secList = 0

    ''' constructor '''
    def __init__(self, wakeDataDict):
        self.wakeData = wakeDataDict

        self.timeList = list(wakeDataDict.keys())
        self.timeList.sort()
        self.startTime = min([float(i) for i in self.timeList])
        self.stopTime = max([float(i) for i in self.timeList])
        self.tNum = len(self.timeList)

        self.secList = list(wakeDataDict[self.timeList[0]].keys())
        self.secList.sort()

    ''' functions '''
    def ave_wakeData(self):
        """ this function compute the time average velocities of each wake section """
        wakeDataDict_ave = dict(zip(self.secList, self.secList))
        for i in self.secList:
            secSum = mat(zeros(shape(self.wakeData[self.timeList[0]][i][:,4:7]))) # initialize a mat for summing data of sec i in all times
            for j in self.timeList:
                secSum += self.wakeData[j][i][:,4:7]
            wakeDataDict_ave[i] = secSum / self.tNum
            wakeDataDict_ave[i] = c_[self.wakeData[self.timeList[0]][i][:,0:4], wakeDataDict_ave[i]]
        return wakeDataDict_ave #返回一个字典，key为截面，value是7列矩阵

    def intensity(self):
        """ this function compute the turbulence intensity of Vx, Vy, Vz of each wake section """
        ave = self.ave_wakeData()
        intensity = dict(zip(self.secList, self.secList))
        for section in self.secList:
            v_ave = ave[section][:,4:7] + 0.0001 # 加一个小量避免出现分母为0
            sum2 = np.zeros(v_ave.shape)
            for time in self.timeList:
                v = self.wakeData[time][section][:,4:7]
                sum2 = sum2 + np.power((v - v_ave), 2)
            sum2 = sum2 / len(self.timeList)
            intensity[section] = c_[self.wakeData[self.timeList[0]][section][:,0:4], (sum2 / v_ave)]
        return intensity #返回一个字典，key为截面，value是7列矩阵
