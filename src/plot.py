import matplotlib.pyplot as plt
import numpy as np
from config import *

def plot(data, sr = sampling_rate):
    t = np.arange(len(data))/float(sr)
    plt.plot(t, data)
    plt.show()
    