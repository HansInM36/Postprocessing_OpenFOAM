import numpy as np
from numpy import *

class SignalSeq:
    ''' members '''
    X = 0
    N = 0
    E_X = 0
    sigma_X = 0
    var_X = 0

    ''' constructor '''
    def __init__(self, x):
        '''
        x: signal sequence, 1D array
        fs: sample frequency
        '''
        self.X = x
        self.N = len(x)
        self.E_X = mean(x)
        self.var_X = var(x)

    ''' method '''
    def AR(self, X=None):
        '''
        X is signal sequence in 1D array
        '''
        if X is None: # because we can't define the function like this def autocor(self, X=self.X):
            X = self.X
        N = len(X)
        m = array([i for i in range(0,N)])
        RX = array(zeros(N))
        for i in range(0,N):
            RX[i] = sum([X[j] * X[j+i] for j in range(0,N-i)]) / N
        return vstack((m,RX))


    def PSE_t_AM(self, fs, X=None): # use autocorrelation function method for temporal power spectrum estimation
        '''
        X is signal sequence in 1D array
        fs is sample frequency
        '''
        if X is None:
            X = self.X
        N = len(X)
        f = linspace(0,fs,N) # the frequency axis
        f = f[range(int(N/2))]
        ps = fft.fft(self.AR(X)[1,:]) # use FFT algorithm to do the DTFT
        ps = abs(ps)
        ps = ps[range(int(N/2))]
        return vstack((f,ps))

    def PSE_s_AM(self, wl, X=None): # use autocorrelation function method for spatial power spectrum estimation
        '''
        X is signal sequence in 1D array
        wl is a tuple containing the smallest and the largest wave length (i.e. the smallest mesh length and the 1D domain length)
        '''
        if X is None:
            X = self.X
        N = len(X)
        L = max(wl)
        delta = min(wl)
        l = linspace(delta, L, N)
        k = array([2*pi/i for i in l[range(int(N/2))]])
        k.sort()
        ps = fft.fft(self.AR(X)[1,:])
        ps = abs(ps)
        ps = ps[range(int(N/2))]
        return vstack((k,ps))

class SignalMat:
    ''' members '''
    Mat = 0
    Size = 0
    E_X = 0
    sigma_X = 0
    var_X = 0

    ''' constructor '''
    def __init__(self, mat):
        '''
        x: signal sequence, 1D array
        fs: sample frequency
        '''
        self.Mat = mat
        self.Size = shape(mat)

    ''' method '''
    def AR(self, Mat=None):
        '''
        Mat is signal matrix in 2D array
        '''
        if Mat is None: # because we can't define the function like this def autocor(self, X=self.X):
            Mat = self.Mat
        Size = shape(Mat)
        Rmn = zeros((Size[0],Size[1]))
        for i in range(0,Size[0]):
            for j in range(0,Size[1]):
                for p in range(0,Size[0]-i):
                    for q in range(0,Size[1]-j):
                        Rmn[i,j] = Rmn[i,j] + Mat[i,j]*Mat[i+p,j+q]
        Rmn = Rmn / (Size[0] * Size[1])
        return Rmn

    def PSE_2D_AM(self, wl2D, Mat=None): # use autocorrelation function method for spatial power spectrum estimation
        '''
        Mat is signal matrix in 2D array
        wl2D is a 2*2 array containing the smallest and the largest wave length (i.e. the smallest mesh length and the 1D domain length) in x and y dimension
        '''
        if Mat is None:
            Mat = self.Mat
        Size = shape(Mat)
        Lx = max(wl2D[0,:])
        deltax = min(wl2D[0,:])
        Ly = max(wl2D[1,:])
        deltay = min(wl2D[1,:])
        lx = linspace(deltax, Lx, Size[0])
        ly = linspace(deltay, Ly, Size[1])
        kx = array([2*pi/i for i in lx[range(int(Size[0]/2))]])
        ky = array([2*pi/j for j in ly[range(int(Size[1]/2))]])
        kx.sort()
        ky.sort()        
        ps = fft.fft2(self.AR(Mat))
        ps = abs(ps)
        return ps
