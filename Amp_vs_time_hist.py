import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import funcs
from matplotlib.colors import LogNorm

# From each csv file pulls 
#     1) The file creation timestamp
#     2) The minimim amplitude
# Appends these values to a 2D array [Times, Amps]
def process_csv(csv_path):
    global data
    timestamps.append(os.path.getmtime(csv_path))
    df = pd.read_csv(csv_path, skiprows=(1,3))
    df['Channel D'] = pd.to_numeric(df['Channel D'], errors='coerce') # Convert String "NaN" to np.NaN
    amplitudes.append(df["Channel D"].min())

# a bit complex
# x_list - list of x data
# y_list - list of y data
# in_file - pass filename - used to make title
def plot_2D_hists(x_list, y_list, in_file):
    fig, ax = plt.subplots(1, 2, figsize=(16, 8))

    # Titles for the subplots
    log_hist_title = os.path.basename(os.path.normpath(in_file)) + " Histogram - Log Color Scale"
    reg_hist_title = os.path.basename(os.path.normpath(in_file)) + " Histogram"

    # Determine range for the histograms
    xmin = np.min(x_list)
    xmax = np.max(x_list)

    ymin = np.min(y_list)
    ymax = np.max(y_list)

    # Bin calculations
    num_bins_x = int((xmax - xmin) / 2)
    num_bins_reg_y = int(-(0.1 / 0.0001) * ymin)

    # Regular 2D Histogram
    h1 = ax[0].hist2d(x_list, y_list, bins=[num_bins_x, num_bins_reg_y])
    ax[0].set_ylim([-0.2, 0])
    ax[0].set_title(reg_hist_title, fontsize=20)
    ax[0].set_xlabel("Minutes Since Run Start", fontsize=16)
    ax[0].set_ylabel("Waveform Amplitude", fontsize=16)

    # 2D Histogram with Logarithmic Color Scale
    h2 = ax[1].hist2d(x_list, y_list, bins=[num_bins_x, 100], norm=LogNorm())
    ax[1].set_ylim([-0.2, 0])
    ax[1].set_title(log_hist_title, fontsize=20)
    ax[1].set_xlabel("Minutes Since Run Start", fontsize=16)
    ax[1].set_ylabel("Waveform Amplitude", fontsize=16)

    # Add colorbars
    fig.colorbar(h1[3], ax=ax[0])
    fig.colorbar(h2[3], ax=ax[1])

    plt.show()

# Get input file
in_file = funcs.get_args()

# Initialize data lists
timestamps = []
amplitudes = []

# use func.loop_big to loop over input run, extract what's needed from csv
funcs.loop_big(in_file, process_csv)

start_time = min(timestamps)
times = [(x-start_time)/60 for x in timestamps]

plot_2D_hists(times, amplitudes, in_file)
