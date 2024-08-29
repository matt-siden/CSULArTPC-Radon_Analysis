import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import funcs


# From each csv file pulls 
#     1) The file creation timestamp
#     2) The minimim amplitude
# Appends these values to a 2D array [Times, Amps]
def process_csv(csv_path):
    global data
    timestamps.append(os.path.getctime(csv_path))
    df = pd.read_csv(csv_path, skiprows=(1,3))
    amplitudes.append(df["Channel D"].min())

# a bit complex
# x_list - list of x data
# y_list - list of y data
# in_file - pass filename - used to make title
def plot_2D_hists(x_list, y_list, in_file):
    fig, ax = plt.subplots(1,2)
    
    log_hist_title = os.path.basename(os.path.normpath(in_file)) + " Histogram - Log Scale"
    reg_hist_title = os.path.basename(os.path.normpath(in_file)) + " Histogram"

    ax[0].hist2d(x_list, y_list)
    ax[0].set_ylim([-1,0])
    ax[0].set_title(reg_hist_title)

    ax[1].hist2d(x_list, y_list)
    ax[1].set_yscale('symlog')
    ax[1].set_title(log_hist_title)
    
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
