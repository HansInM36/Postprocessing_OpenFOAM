import numpy as np
import matplotlib.pyplot as plt


z = np.linspace(2,1000,500)

# NBL
g = 9.8
uf = 0.5
kappa = 0.4
z0 = 0.2
uNBL = uf/kappa * np.log(z/z0)

# CBL
def PHI_CBL(x):
    x = (1 - 16*x)**0.25
    return 2*np.log((1+x)/2) + np.log((1+x**2)/2) - 2*np.arctan(x) + np.pi/2

g = 9.8
uf = 0.5
kappa = 0.4
z0 = 0.2
qs = -0.04
L = 300*uf**3 / (g*qs*kappa)
phi = np.zeros(z.shape)
for i in range(z.shape[0]):
    phi[i] = PHI_CBL(z[i]/L)
uCBL = uf/kappa * (np.log(z/z0) - phi)

# SBL
def PHI_SBL(x):
    if 0 < x and x <= 0.5:
        return -5 * x
    elif 0.5 <= x and x <= 7:
        return x + 2/3 * (x - 5/0.35)
    else:
        return np.exp(-0.35 * x) + 2/3*5/0.35


g = 9.8
uf = 0.5
kappa = 0.4
z0 = 0.2
qs = 0.02
L = 300*uf**3 / (g*qs*kappa)
phi = np.zeros(z.shape)
for i in range(z.shape[0]):
    phi[i] = PHI_SBL(z[i]/L)
uSBL = uf/kappa * (np.log(z/z0) - phi)

plt.plot(uNBL, z, 'g-', linewidth=2)
plt.plot(uCBL, z, 'r-', linewidth=2)
plt.plot(uSBL, z, 'b-', linewidth=2)
plt.grid()
plt.show()
