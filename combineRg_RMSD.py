#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to merge RMSD and Rg xvg files
Output format: Time RMSD Rg
"""

def read_rmsd_file(filename):
    """Read RMSD file and return dictionary of time and RMSD data"""
    rmsd_data = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # ����ע���кͿ���
                if line.startswith('#') or line.startswith('@') or not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    time = float(parts[0])
                    rmsd = float(parts[1])
                    rmsd_data[time] = rmsd
        
        print(f"Read {len(rmsd_data)} RMSD data points from {filename}")
        return rmsd_data
    
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return {}
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return {}

def read_rg_file(filename):
    """Read Rg file and return dictionary of time and Rg data"""
    rg_data = {}
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                # ����ע���кͿ���
                if line.startswith('#') or line.startswith('@') or not line:
                    continue
                
                parts = line.split()
                if len(parts) >= 2:
                    time = float(parts[0])
                    rg = float(parts[1])  # Take first Rg value (total Rg)
                    rg_data[time] = rg
        
        print(f"Read {len(rg_data)} Rg data points from {filename}")
        return rg_data
    
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return {}
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return {}

def merge_data(rmsd_data, rg_data):
    """Merge RMSD and Rg data"""
    # Find common time points
    common_times = set(rmsd_data.keys()) & set(rg_data.keys())
    
    if not common_times:
        print("Warning: No common time points found!")
        return []
    
    # Sort by time
    sorted_times = sorted(common_times)
    
    merged_data = []
    for time in sorted_times:
        merged_data.append([time, rmsd_data[time], rg_data[time]])
    
    print(f"Merged {len(merged_data)} data points")
    return merged_data

def write_combined_file(data, output_filename):
    """Write merged data to file"""
    try:
        with open(output_filename, 'w') as f:
            # Write file header
            f.write("# Combined RMSD and Rg data\n")
            f.write("# Time (ps)    RMSD (nm)    Rg (nm)\n")
            f.write("@    title \"RMSD vs Rg\"\n")
            f.write("@    xaxis  label \"Time (ps)\"\n")
            f.write("@    yaxis  label \"RMSD (nm), Rg (nm)\"\n")
            f.write("@TYPE xy\n")
            
            # Write data
            for time, rmsd, rg in data:
                f.write(f"{time:12.6f} {rmsd:12.6f} {rg:12.6f}\n")
        
        print(f"Merged data saved to {output_filename}")
        
    except Exception as e:
        print(f"Error writing file: {e}")

def main():
    # File names
    rmsd_file = "rmsd_pro.xvg"
    rg_file = "Rg.xvg"
    output_file = "combined.xvg"
    
    print("Starting to merge xvg files...")
    print("=" * 50)
    
    # Read data
    rmsd_data = read_rmsd_file(rmsd_file)
    rg_data = read_rg_file(rg_file)
    
    if not rmsd_data or not rg_data:
        print("Cannot read data files, please check if files exist and format is correct")
        return
    
    # Merge data
    merged_data = merge_data(rmsd_data, rg_data)
    
    if not merged_data:
        print("Merge failed, no common time points found")
        return
    
    # Write merged file
    write_combined_file(merged_data, output_file)
    
    print("=" * 50)
    print("Merge completed!")
    print(f"Output file: {output_file}")
    print(f"Data points: {len(merged_data)}")
    
    # Show preview of first few lines
    print("\nFirst 5 lines preview:")
    print("Time (ps)    RMSD (nm)    Rg (nm)")
    print("-" * 40)
    for i, (time, rmsd, rg) in enumerate(merged_data[:5]):
        print(f"{time:9.3f}    {rmsd:8.6f}    {rg:7.6f}")
    
    if len(merged_data) > 5:
        print("...")

if __name__ == "__main__":
    main()
