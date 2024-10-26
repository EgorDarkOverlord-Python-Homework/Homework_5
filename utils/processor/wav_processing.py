import numpy as np

def wav_histogram(data, d_type):
    return np.histogram(data, 256, (np.iinfo(d_type).min, np.iinfo(d_type).max))[0]