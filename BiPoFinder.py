import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from scipy.signal import find_peaks
import funcs

def process_csv(csv_path):
    global out_file # Reference to output text file.
    global out_dir # Reference to output filepath
    df = pd.read_csv(csv_path, skiprows=(1,3))
    df['Channel D'] = pd.to_numeric(df['Channel D'], errors='coerce')
    valleys, _ = find_peaks(-df['Channel D'], distance=100, height=0.03)
    if len(valleys) >=2:
        out_file.write(f"{csv_path}\n")
        funcs.plot_waveform(df, csv_path, 'Channel D', False)
        
        # Save the plot to a file
        output_filename = os.path.join(out_dir, os.path.splitext(os.path.basename(csv_path))[0]+".png")
        plt.savefig(output_filename)
        plt.close()

# Get input directory
in_file = funcs.get_args()

# Declare output list of Waveforms with two peaks. 
out_file_name = os.path.join(in_file,"BiPoCandidates.txt")
out_dir = os.path.join(in_file, "BiPoCandidates")

# Create/Open output text file
out_file = open(out_file_name, 'w')

# Make the output folder to hold waveform images
os.makedirs(out_dir, exist_ok=True)

funcs.loop_big(in_file, process_csv)

out_file.close()
