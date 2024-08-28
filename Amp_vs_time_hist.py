import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

def process_csv_files(root_folder):
    all_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.csv'):
                all_files.append(os.path.join(root, file))

    total_files = len(all_files)
    print(f"Total CSV files to process: {total_files}")

    # Sort files by creation time
    all_files.sort(key=os.path.getctime)

    start_time = os.path.getctime(all_files[0])
    data = []

    for i, file_path in enumerate(all_files, 1):
        try:
            # Read the CSV file, skipping the first 3 rows
            df = pd.read_csv(file_path, skiprows=3, names=['Time', 'Channel A', 'Channel D'])
            
            # Convert 'Channel D' to numeric, coercing errors to NaN
            df['Channel D'] = pd.to_numeric(df['Channel D'], errors='coerce')
            
            # Drop any rows with NaN values
            df = df.dropna(subset=['Channel D'])
            
            if not df.empty:
                # Find the maximum negative amplitude in Channel D
                max_neg_amplitude = df['Channel D'].min()
                
                # Calculate time since start in minutes
                file_time = os.path.getctime(file_path)
                time_since_start = (file_time - start_time) / 60  # Convert to minutes
                
                data.append((time_since_start, max_neg_amplitude))
            
            # Update progress
            print(f"\rProcessing: {i}/{total_files} files completed", end="", flush=True)
        
        except Exception as e:
            print(f"\nError processing {file_path}: {str(e)}")

    print("\nProcessing complete.")
    return data

def create_2d_histogram(data, output_file):
    if not data:
        print("No valid data to create histogram.")
        return

    times, amplitudes = zip(*data)
    
    plt.figure(figsize=(12, 8))
    plt.hist2d(times, amplitudes, bins=(50, 50), cmap='viridis')
    plt.colorbar(label='Count')
    plt.xlabel('Time Since Run Start [m]')
    plt.ylabel('Amplitude [V]')
    plt.title('Max Amplitudes All Data')
    plt.savefig(output_file)
    plt.close()
    
    print(f"2D histogram saved as {output_file}")

def main(args):
    data = process_csv_files(args.input_folder)
    create_2d_histogram(data, args.output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV files and create a 2D histogram.")
    parser.add_argument('--input_folder', required=True, help='Root folder containing subfolders with CSV files')
    parser.add_argument('--output_file', required=True, help='Output file name for the 2D histogram (e.g., histogram.png)')
    args = parser.parse_args()

    main(args)
