# Takes the text file output of BiPoFinder and histograms the time separation of peaks.
# Maybe convoluted but it works

import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from scipy.signal import find_peaks
import numpy as np
from scipy.optimize import curve_fit
import funcs

# Define Exponential decay Func 
# t - Time
# A - Background Activity
# B - Coef
# C - half-life
def exp_decay(t, A, B, C):
    return A + B * np.exp(-t /( C * np.log(2)))

# loops over the input csv
# built hist data
def loop_csv(in_file):
    df_files = pd.read_csv(in_file)
    for row in df_files.iterrows():
        time_data.append(find_dT(row[1][0]))

# Extracts the time difference data from a single CSV
def find_dT(file_path):
    df = pd.read_csv(file_path, skiprows=3, names=['Time', 'Channel A', 'Channel D'])
    df['Channel D'] = pd.to_numeric(df['Channel D'], errors='coerce')
    valleys, _ = find_peaks(-df['Channel D'], distance=100, height=0.03)
    time_diff = df['Time'].iloc[valleys[1]] - df['Time'].iloc[valleys[0]]
    return time_diff 

def fit_and_plot(fit_func, x_data, y_data):
    popt, pcov = curve_fit(fit_func, x_data, y_data, p0=[0, 1, 300], bounds=([0,0,0],[1, np.inf, np.inf]))
    A, B, C = popt

    # Calculate uncertainties
    perr = np.sqrt(np.sqrt(np.diag(pcov)))
    A_err, B_err, C_err = perr

    # Plot the fitted curve
    x_fit = np.linspace(bin_centers[0], bin_centers[-1], 100)
    y_fit = exp_decay(x_fit, A, B, C)
    plt.plot(x_fit, y_fit, 'r-', label=f'Fit: A={A:.2f}±{A_err:.2f}, B={B:.2f}±{B_err:.2f}, C={C:.2f}±{C_err:.2f}')
    plt.legend()
    plt.show()

# Parse for --in_file 'directory'
in_file = funcs.get_args()

# Initialize Hist Data
time_data = []

# Iterate over files in the csv.
loop_csv(in_file)

# Histogram Time Data
counts, bin_centers = funcs.plot_hist_1D(time_data, 
        in_file, 
        'Polonium Decay Time', 
        None, 
        False, 
        False,
        False)

# Fit and plot
fit_and_plot(exp_decay, bin_centers, counts)
