import numpy as np


def tfilter(x,tao):
    '''
    filter x with tao
    x must be a 1D array
    '''
    '''
    import timefilter as tf
    x = np.array([1,2,3,4,5,6,7])
    tf.tfilter(x,3)
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
