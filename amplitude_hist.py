# Skims a given run and histograms the amplitudes of a dataset
# Usage (Ubuntu): 'python3 path/to/amplitude_hists.py --in_file '/path/to/directory/''
# Usage (Windows): 'python3 path\to\amplitude_hists.py --in_file \path\to\directory\'

import funcs  
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Function to process each CSV file
def process_csv(csv_path):
    global amplitudes  # Reference to the global list to accumulate data
    df = pd.read_csv(csv_path, skiprows=(1,3))
    min_val = df["Channel D"].min()
    amplitudes.append(min_val)

# Parse for --in_file 'directory'
in_file = funcs.get_args()
#print(os.path.basename(os.path.normpath(in_file)))
# ~~~ Edit these ~~~ #
#channel = 'Channel D'  # Channel to process (usually D in all recent runs)
#bins = 100  # Histogram Bins
hist_range = [-0.6, 0]  # Range of the Histogram [lower, upper]
# ~~~ Edit these ~~~ #

# This list will store all amplitudes from all subdirectories
amplitudes = []

# Use funcs.loop_big to process each CSV file in each subdirectory
funcs.loop_big(in_file, process_csv)

funcs.plot_hist_1D(amplitudes, in_file, "Amplitudes", hist_range)
