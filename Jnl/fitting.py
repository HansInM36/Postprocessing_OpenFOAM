import numpy as np
import scipy as sp
from scipy import stats
from scipy.optimize import leastsq

def func_parabola(p,x):
    '''
    parabola function
    p: parameter, a tuple (a,b,c)
    '''
    return p[0]*x**2 + p[1]*x + p[2]

def func_gs(p,x):
    '''
    gaussian function
    p: parameter, a tuple (mu,sigma)
    '''
    return stats.norm(p[0],p[1]).pdf(x)

def func_ABL(p,kappa,z0,x):
    '''
    ABL Vx function
    p: parameter, a tuple (uf,kappa,z0)
    '''
    return p * 1/kappa * np.log(x/z0)

def fit(func,p0,x,y):
    '''
    fitting
    func: fitting function
    p0: initial parameters for fitting function, a tuple, for example (alpha, beta, garma)
    x: sample array x
    y: sample array y
    '''
    def error(p,x,y):
        return func(p,x) - y
    return leastsq(error,p0,args=(x,y))[0]

def fit_ABL(p0,kappa,z0,x,y):
    '''
    fitting by ABL log rule
    p0: initial parameters for fitting function, a tuple, for example (uf, kappa)
    x: sample array x
    y: sample array y
    '''
    def error(p,x,y):
        return func_ABL(p,kappa,z0,x) - y
    return leastsq(error,p0,args=(x,y))[0]

def fit_gs(p0,x,y):
    '''
    fitting by gaussian curve
    p0: initial parameters for gaussian function, a tuple (mu0, sigma0)
    x: sample array x
    y: sample array y
    '''
    def error(p,x,y):
        return func_gs(p,x) - y
    # normalization
    delta = (max(x) - min(x)) / (np.shape(x)[0] - 1)
    S = sum(y)*delta - 0.5*(y[np.where(x==min(x))] + y[np.where(x==max(x))])
    y = y / S
    return leastsq(error,p0,args=(x,y))[0]


'''
# testing code
x = np.linspace(10,200,40)
p = 1.5
y = func_ABL(p,0.4,0.15,x)
p0 = 3.5
pp = fit_ABL(p0,0.4,0.15,x,y)
yp = func_ABL(pp,0.4,0.15,x)
yp - y
'''
