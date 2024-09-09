# Common functions between analysis scripts

import os
import pandas as pd
import argparse
import numpy as np
import matplotlib.pyplot as plt

# Loop through a directory of subdirectories and pass some function to each csv
# Also implments a counter to tell the user 
#   1) What subdirectory they are on and 
#   2) what csv file in that subdir they are on
#
# dir_path - path to the large directory
# func - function to use to process each csv file. 
def loop_big(dir_path, func):
    
    subdir_total = len(os.listdir(dir_path))
    subdir_num = 0
    for subdir in os.listdir(dir_path):
        subdir_num += 1
        subdir_path = os.path.join(dir_path, subdir)
        if not os.path.isdir(subdir_path):
            continue
        csv_total = len(os.listdir(subdir_path))
        csv_num = 0
        for csv in os.listdir(subdir_path):
            csv_num += 1
            if not csv.lower().endswith('.csv'):
                continue
            csv_path = os.path.join(subdir_path, csv)
            func(csv_path)
            print(f"\rProcessing: On Subdirectory {subdir_num}/{subdir_total}, File {csv_num}/{csv_total}    ", end="", flush=True)


# Putting this here to standardize the command format
# each bool is whether a specific script has that parameter
# originally included output paths as well but I think it
#     makes more sense to print to the input dir
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_file', required=True)
    args = parser.parse_args()
    in_file = args.in_file
    return in_file


# Self Explanatory, plots histogram w/ error bars from a python list (data), also saves the hist.png
# to the input to the input directory.
# save - boolean, if True saves next to the input file
# norm - boolean, if True normalizes Hist
def plot_hist_1D(data, in_file, x_axis_title, hist_range, norm, show, save):
    data = np.array(data, dtype=np.float64)
   
    counts, bin_edges = np.histogram(data, bins=16, range=hist_range, density=norm)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_width = bin_edges[1] - bin_edges[0]

    # Branching if normalization is desired
    if norm:
        counts_err = np.sqrt(counts / bin_width) / np.sqrt(len(data))
        y_axis_title = "Probability Density"
    else:
        counts_err = np.sqrt(bin_width/counts)
        y_axis_title = "Counts"
    
    plt.errorbar(bin_centers, 
                counts, 
                yerr=counts_err,  
                ecolor='black', 
                capsize=3, 
                fmt='.',
                color='black')
    hist_title = os.path.basename(os.path.normpath(in_file)) + " Histogram"
    plt.title(hist_title)
    plt.xlabel(x_axis_title)
    plt.ylabel(y_axis_title)
    plt.grid(True)
    if show:
        plt.show()
    if save:
        save_path = os.path.join(in_file, "amplitude_hist.png")
        plt.savefig(save_path)
    return counts, bin_centers
    
# Plot Waveform - Generally Plots a given column from a given df
# df - input dataframe - probably already read from a csv
# in_file - really only used for plot title
# column - name of column to plot, 'Channel D' is usually the PMT Waveform. 
# show - boolean shows plot if true
def plot_waveform(df, in_file, column, show):
    plt.figure(figsize=(10, 6))
    plt.plot(df["Time"], df[column], marker='', linestyle='-', label=column)

    ### Units may not be accurate based on how data is collected
    plt.xlabel('Time [ns]')
    plt.ylabel('Output Signal [V]')

    plot_title = os.path.splitext(os.path.basename(in_file))[0] + " Waveform"
    plt.title(plot_title)

    plt.legend()
    if show:
        plt.show()

def placeholder(df):
    pass


#print(os.path.isdir("Downloads/Radon Post-Reference"))
#loop_big("Downloads/Radon Post-Reference", placeholder)
