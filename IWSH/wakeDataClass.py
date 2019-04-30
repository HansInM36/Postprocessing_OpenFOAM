import numpy as np
from numpy import *

def flt_seq(x,tao):
    """ 以tao来过滤一个序列 """
    '''
    filter x with tao
    x must be a 1D array
    '''
    '''
    x = np.array([1,2,3,4,5,6,7])
    flt_seq(x,3)
    '''
    tao = int(tao)
    l = np.shape(x)[0]
    y = np.zeros(np.shape(x))

    for i in range(l):
        if i-tao < 0:
            a = 0
        else:
            a = i-tao
        if i+tao+1 > l:
            b = l
        else:
            b = i+tao+1
        a, b = int(a), int(b)
        y[i] = sum(x[a:b]) / np.shape(x[a:b])[0]
    return y

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

class Sec(object):
    """ 初始化参数为一个储存了某一截面尾流信息的字典，key值是时刻，键值是pNum行7列的array """

    secData = {}
    topoData = 0 # 储存点编号，坐标的信息
    timeList = []
    pNum = 0
    tNum = 0
    secData_fd = {} # 储存经过tao过滤后的截面信息，字典形式和secData一样
    tseq = 0

    def __init__(self, secDataDict):
        self.secData = secDataDict
        self.timeList = list(secDataDict.keys())
        self.timeList.sort()
        self.topoData = secDataDict[self.timeList[0]][:,0:4]
        self.tNum = len(self.timeList)
        self.pNum = shape(secDataDict[self.timeList[0]])[0]
        self.tseq = array(self.timeList)

    def V_tSeq(self, r, axis):
        """ 抽取第secData第r行axis轴对应速度的时间序列 """
        '''
        r是行数，是一个整数，第一行r=0
        axis是str，'x','y'或'z'
        '''
        vseq = array(zeros((shape(self.tseq))))
        if axis == 'x':
            for i in range(self.tNum):
                vseq[i] = self.secData[self.timeList[i]][r,4]
        elif axis == 'y':
            for i in range(self.tNum):
                vseq[i] = self.secData[self.timeList[i]][r,5]
        elif axis == 'z':
            for i in range(self.tNum):
                vseq[i] = self.secData[self.timeList[i]][r,6]
        else:
            return print('wrong axis')
        return vseq

    def fSec(self, tao):
        """ 用tao过滤整个截面的信息，得到self.secData_fd """
        for t in range(self.tNum):
            self.secData_fd[self.timeList[t]] = array(zeros((self.pNum,3)))
        for r in range(self.pNum):
            Vx = self.V_tSeq(r,'x')
            Vy = self.V_tSeq(r,'y')
            Vz = self.V_tSeq(r,'z')
            Vx = tfilter(Vx, tao)
            Vy = tfilter(Vy, tao)
            Vz = tfilter(Vz, tao)
            for t in range(self.tNum):
                self.secData_fd[self.timeList[t]][r,0] = Vx[t]
                self.secData_fd[self.timeList[t]][r,1] = Vy[t]
                self.secData_fd[self.timeList[t]][r,2] = Vz[t]
        for t in range(self.tNum):
            self.secData_fd[self.timeList[t]] = hstack((self.topoData, self.secData_fd[self.timeList[t]]))

    def fSec_t(self, tao, t_str):
        """ 用tao过滤整个截面的信息，得到t_str时刻的过滤后的截面的信息 """
        '''
        t_str必须是一个包含于self.timeList里面的某个str
        '''
        sec_t_fd = array(zeros((self.pNum,3)))

        tDict = {}
        for tt in range(self.tNum): # 为简化计算，建立一个序数和时刻str一一对应的字典
            tDict[tt] = self.timeList[tt]
            if tDict[tt] == t_str:
                t = tt # t_str则对应于序数t
        if t-tao < 0:
            a = 0
        else:
            a = t-tao
        if t+tao+1 > self.tNum:
            b = self.tNum
        else:
            b = t+tao+1
        a, b = int(a), int(b)
        
        for r in range(self.pNum):
            Vx = 0
            Vy = 0
            Vz = 0
            for i in range(a,b):
                Vx += self.secData[tDict[i]][r,4]
                Vy += self.secData[tDict[i]][r,5]
                Vz += self.secData[tDict[i]][r,6]
            Vx = Vx/len(range(a,b))
            Vy = Vy/len(range(a,b))
            Vz = Vz/len(range(a,b))
            sec_t_fd[r,0] = Vx
            sec_t_fd[r,1] = Vy
            sec_t_fd[r,2] = Vz
        return hstack((self.topoData, sec_t_fd))















class SecITP:
    ''' 主要用于对某个平面信息进行网格化插值 '''
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
