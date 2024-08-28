import os
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from scipy.signal import find_peaks

def analyze_and_plot_csv(file_path, output_folder, text_file):
    # Read the CSV file, skipping the first 3 rows (titles, units, blank)
    df = pd.read_csv(file_path, skiprows=3, names=['Time', 'Channel A', 'Channel D'])
    
    # Find peaks (or in this case, valleys) in Channel D
    valleys, _ = find_peaks(-df['Channel D'], distance=100, height=0.01)
    
    # Check if there are at least two valleys below 0.01
    if len(valleys) >= 2:
        print(f"Found file with two peaks below 0.03: {file_path}")
        text_file.write(f"{file_path}\n")
        
        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df['Time'], df['Channel D'])
        plt.scatter(df['Time'].iloc[valleys], df['Channel D'].iloc[valleys], color='red')
        plt.title(f"Channel D - {os.path.basename(file_path)}")
        plt.xlabel("Time")
        plt.ylabel("Channel D")
        plt.axhline(y=0.01, color='r', linestyle='--')
        plt.axhline(y=-0.01, color='r', linestyle='--')
        
        # Save the plot to a file
        output_filename = os.path.join(output_folder, f"{os.path.basename(file_path)}.png")
        plt.savefig(output_filename)
        plt.close()

def search_csv_files(root_folder, output_folder, output_text_file):
    total_files = sum([len(files) for r, d, files in os.walk(root_folder) if any(f.endswith('.csv') for f in files)])
    processed_files = 0
    files_with_peaks = 0
    
    print(f"Total CSV files found: {total_files}")
    
    with open(output_text_file, 'w') as text_file:
        for root, dirs, files in os.walk(root_folder):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    processed_files += 1
                    try:
                        analyze_and_plot_csv(file_path, output_folder, text_file)
                        files_with_peaks += 1
                    except Exception as e:
                        print(f"Error processing {file_path}: {str(e)}")
                    
                    # Update progress
                    print(f"\rProgress: {processed_files}/{total_files} files processed. Files with peaks: {files_with_peaks}", end="", flush=True)
    
    print("\nProcessing complete.")
    print(f"Total files processed: {processed_files}")
    print(f"Files with two peaks below 0.01: {files_with_peaks}")

# Parse for --in_file 'directory'
parser = argparse.ArgumentParser()
parser.add_argument('--in_file', required=True, help='Input directory containing CSV files')
parser.add_argument('--out_file', required=True, help='Output text file to save filenames')
parser.add_argument('--out_folder', required=True, help='Output folder to save plots')
args = parser.parse_args()
folder = args.in_file
output_text_file = args.out_file
output_folder = args.out_folder

# Create the output folder if it does not exist
os.makedirs(output_folder, exist_ok=True)

search_csv_files(folder, output_folder, output_text_file)
