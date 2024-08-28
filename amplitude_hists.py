# Histogram the amplitudes of a [triggered] dataset. Additionally prints the mean.
# Usage (Ubuntu): 'python3 path/to/amplitude_hists.py --in_file '/path/to/directory/''
# Usage (Windows): 'python3 path\to\amplitude_hists.py --in_file \path\to\directory\'
 
import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os
import numpy as np

# Parse for --in_file 'directory'
parser = argparse.ArgumentParser()
parser.add_argument('--in_file', required=True)
args = parser.parse_args()
root_directory = args.in_file

# ~~~ Edit these ~~~ #
channel = 'Channel D'  # Channel to process (usually D in all recent runs)
bins = 100  # Histogram Bins
hist_range = [-0.6, 0]  # Range of the Histogram [lower, upper]
# ~~~ Edit these ~~~ #

def process_folder(folder_path):
    amplitudes = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            filepath = os.path.join(folder_path, filename)
            df = pd.read_csv(filepath, skiprows=[1])
            df[channel] = pd.to_numeric(df[channel], errors='coerce')
            min_val = df[channel].min()
            if min_val < -0.02:  # and min_val>-0.5:
                amplitudes.append(min_val)
    return amplitudes

# Process all subfolders
all_amplitudes = []
for subfolder in os.listdir(root_directory):
    subfolder_path = os.path.join(root_directory, subfolder)
    if os.path.isdir(subfolder_path):
        subfolder_amplitudes = process_folder(subfolder_path)
        all_amplitudes.extend(subfolder_amplitudes)
        
        # Create histogram for each subfolder
        plt.figure()
        plt.hist(subfolder_amplitudes, bins=bins, range=hist_range)
        plt.title(f'Max Amplitudes - {subfolder}')
        plt.xlabel('Max Amplitudes')
        plt.ylabel('Counts')
        plt.xticks(rotation=45)
        mean = sum(subfolder_amplitudes) / len(subfolder_amplitudes) * 1000  # mean in mV
        std = np.std(subfolder_amplitudes)
        plt.text(hist_range[0], plt.ylim()[1]*0.9, f'Mean: {mean:.2f} mV', fontsize=12)
        plt.text(hist_range[0], plt.ylim()[1]*0.8, f'Standard Dev: {std:.2f}', fontsize=12)
        plt.savefig(f'{subfolder}_histogram.png')
        plt.close()

# Create overall histogram
plt.figure()
plt.hist(all_amplitudes, bins=bins, range=hist_range)
plt.title('Max Amplitudes - All Folders')
plt.xlabel('Max Amplitudes')
plt.ylabel('Counts')
plt.xticks(rotation=45)
mean = sum(all_amplitudes) / len(all_amplitudes) * 1000  # mean in mV
std = np.std(all_amplitudes)
plt.text(hist_range[0], plt.ylim()[1]*0.9, f'Mean: {mean:.2f} mV', fontsize=12)
plt.text(hist_range[0], plt.ylim()[1]*0.8, f'Standard Dev: {std:.2f}', fontsize=12)
plt.savefig('overall_histogram.png')
plt.show()

print(f"Overall Mean: {mean:.2f} mV")
print(f"Overall Standard Deviation: {std:.2f}")
