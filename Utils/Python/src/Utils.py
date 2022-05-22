import numpy as np

def mag2dB(mag):
    
    return 20*np.log10(np.abs(mag))