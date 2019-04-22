import numpy as np
import matplotlib.pyplot as plt

def filter_t(y,t):
    ''' t must less than len(y)/2 '''
    t = int(t)
    N = np.shape(y)[0]
    yy = np.zeros(np.shape(y))
    for i in range(0,N):
        if i < t:
            yy[i] = sum(y[0:i]) / (i+1)
        elif N-i < t:
            yy[i] = sum(y[i:N]) / (N-i+1)
        else:
            yy[i] = sum(y[i-t:i+t+1]) / (2*t+1)
    return yy



x = np.linspace(0,300,60)
phi = np.random.permutation(range(60)) * 2*np.pi/60/5
y = np.sin(x * 2*np.pi/300 + phi)
y1 = filter_t(y,3)
y2 = filter_t(y,20)

plt.figure(figsize = (8, 4))
plt.plot(x, y, 'ro', linewidth = 1, label='original')
plt.plot(x, y1, 'g-', linewidth = 1, label='tao = 3')
plt.plot(x, y2, 'b-', linewidth = 1, label='tao = 20')
plt.ylabel('V(m/s)')
plt.xlabel('t(s)')
legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')
plt.grid()
plt.show()
