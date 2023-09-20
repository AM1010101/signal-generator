import numpy as np
from scipy.signal import chirp, spectrogram
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 1500)
w = chirp(t, f0=0.1, f1=3.25, t1=10, method='logarithmic')
w_rev = chirp(t, f0=3.25, f1=0.1, t1=10, method='logarithmic')
w_combined = np.concatenate((w, w_rev))

t = np.linspace(0, 10, 2*1500)
plt.plot(t, w_combined)

plt.xlabel('t (sec)')
plt.title("Linear Chirp, f(0)=6, f(10)=1")
plt.xlabel('t (sec)')
plt.show()