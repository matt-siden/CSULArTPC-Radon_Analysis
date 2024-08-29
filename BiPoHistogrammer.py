import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from scipy.signal import find_peaks
import numpy as np
from scipy.optimize import curve_fit

def exponential_decay(t, A, B, C):
    return A + B * np.exp(-t / C)

def analyze_csv(file_path):
    df = pd.read_csv(file_path, skiprows=3, names=['Time', 'Channel A', 'Channel D'])
    valleys, _ = find_peaks(-df['Channel D'], distance=100, height=0.01)
    if len(valleys) >= 2:
        time_diff = df['Time'].iloc[valleys[1]] - df['Time'].iloc[valleys[0]]
        return time_diff
    return None

def process_csv_files(input_file, output_histogram):
    time_differences = []
    
    with open(input_file, 'r') as file:
        csv_files = file.read().splitlines()
    
    total_files = len(csv_files)
    processed_files = 0
    
    print(f"Total CSV files to process: {total_files}")
    
    for csv_file in csv_files:
        processed_files += 1
        try:
            time_diff = analyze_csv(csv_file)
            if time_diff is not None:
                time_differences.append(time_diff)
        except Exception as e:
            print(f"Error processing {csv_file}: {str(e)}")
        
        print(f"\rProgress: {processed_files}/{total_files} files processed.", end="", flush=True)
    
    print("\nProcessing complete.")
    print(f"Total files processed: {processed_files}")
    print(f"Files with two peaks: {len(time_differences)}")
    
    # Create normalized histogram
    plt.figure(figsize=(10, 6))
    counts, bins, _ = plt.hist(time_differences, bins='auto', density=True, edgecolor='black')
    plt.title("Normalized Histogram of Time Differences Between Prominent Peaks")
    plt.xlabel("Time Difference")
    plt.ylabel("Probability Density")
    
    # Perform curve fitting on the histogram data
    bin_centers = (bins[:-1] + bins[1:]) / 2
    try:
        popt, pcov = curve_fit(exponential_decay, bin_centers, counts, p0=[np.min(counts), np.max(counts) - np.min(counts), np.mean(bin_centers)])
        A, B, C = popt
        
        # Calculate uncertainties
        perr = np.sqrt(np.diag(pcov))
        A_err, B_err, C_err = perr
        
        # Plot the fitted curve
        x_fit = np.linspace(bin_centers[0], bin_centers[-1], 100)
        y_fit = exponential_decay(x_fit, A, B, C)
        plt.plot(x_fit, y_fit, 'r-', label=f'Fit: A={A:.2f}±{A_err:.2f}, B={B:.2f}±{B_err:.2f}, C={C:.2f}±{C_err:.2f}')
        plt.legend()
        
        print(f"Fit parameters:")
        print(f"A = {A:.2f} ± {A_err:.2f}")
        print(f"B = {B:.2f} ± {B_err:.2f}")
        print(f"C = {C:.2f} ± {C_err:.2f}")
    except RuntimeError:
        print("Curve fitting failed for the histogram data")
    
    plt.savefig(output_histogram)
    plt.close()
    
    print(f"Normalized histogram with fit saved as {output_histogram}")

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--in_file', required=True, help='Input text file containing paths to CSV files')
parser.add_argument('--out_histogram', required=True, help='Output file to save the histogram')
args = parser.parse_args()

process_csv_files(args.in_file, args.out_histogram)
