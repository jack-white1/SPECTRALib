import numpy as np
import matplotlib.pyplot as plt

def boxcar_filter(time_series, boxcar_width):
    boxcar = np.ones(boxcar_width) / boxcar_width
    filtered_series = np.convolve(time_series, boxcar, mode='valid')
    return filtered_series


