# Plots a single waveform - consider consider modifying this up to be called by other scripts
# Usage (Ubuntu): 'python3 /path/to/plot_waveform.py --in_csv '/path/to/csv/''
# Usage (Windows): 'python3 \path\to\plot_waveform.py --in_csv \path\to\csv\'

import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os

# Parse for --in_file 'directory'
parser = argparse.ArgumentParser()
parser.add_argument('--in_csv', required=True)
args = parser.parse_args()

csvname = args.in_csv # Directory to input

# List of channels to plot
channels = ['Channel A', 'Channel B', 'Channel C'] 

# Load the CSV file into a DataFrame
df = pd.read_csv(csvname, skiprows=[1,2])
plt.figure(figsize=(10, 6))
    
for channel in channels:
    plt.plot(df["Time"], df[channel], marker='', linestyle='-', label=channel)

### Units may not be accurate based on how data is collected
plt.xlabel('Time [ns]') 
plt.ylabel('Output Signal [V]')

plt.title('Radon Test Vessel - ' + str(csvname))
#plt.set_ylim([-0.5, 0.5])
plt.legend()
plt.locator_params(axis='x', nbins=10)
plt.grid(True)
plt.show()
