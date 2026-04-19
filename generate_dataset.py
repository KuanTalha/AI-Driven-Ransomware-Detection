import csv
import random
import numpy as np

def generate_ransomware_dataset(num_samples=1000, output_file='ransomware_dataset.csv'):
    """
    Generate a synthetic dataset for ransomware detection
    
    Features:
    - cpu_usage: CPU utilization percentage (0-100)
    - disk_writes: Disk write operations per second
    - file_rename_count: Number of file rename operations per minute
    - process_count: Number of running processes
    - label: 0 = normal, 1 = ransomware
    """
    
    data = []
    
    # Generate normal behavior samples (70% of dataset)
    normal_samples = int(num_samples * 0.7)
    for _ in range(normal_samples):
        # Normal system behavior characteristics
        cpu_usage = np.random.normal(25, 15)  # Average 25% CPU, std 15%
        cpu_usage = max(0, min(100, cpu_usage))  # Clamp to 0-100%
        
        disk_writes = np.random.exponential(50)  # Low disk write activity
        disk_writes = min(disk_writes, 500)  # Cap at reasonable limit
        
        file_rename_count = np.random.poisson(2)  # Very few file renames
        file_rename_count = min(file_rename_count, 10)
        
        process_count = np.random.normal(120, 20)  # Normal process count
        process_count = max(50, min(300, int(process_count)))
        
        data.append([
            round(cpu_usage, 2),
            round(disk_writes, 2),
            file_rename_count,
            process_count,
            0  # Normal label
        ])
    
    # Generate ransomware behavior samples (30% of dataset)
    ransomware_samples = num_samples - normal_samples
    for _ in range(ransomware_samples):
        # Ransomware behavior characteristics
        cpu_usage = np.random.normal(75, 20)  # High CPU usage for encryption
        cpu_usage = max(30, min(100, cpu_usage))  # Ransomware uses significant CPU
        
        disk_writes = np.random.normal(800, 300)  # Heavy disk write activity
        disk_writes = max(200, min(2000, disk_writes))  # High write operations
        
        file_rename_count = np.random.normal(150, 50)  # Many file renames/encryptions
        file_rename_count = max(50, min(500, int(file_rename_count)))
        
        process_count = np.random.normal(140, 25)  # Slightly higher process count
        process_count = max(80, min(350, int(process_count)))
        
        data.append([
            round(cpu_usage, 2),
            round(disk_writes, 2),
            file_rename_count,
            process_count,
            1  # Ransomware label
        ])
    
    # Shuffle the data
    random.shuffle(data)
    
    # Write to CSV file
    headers = ['cpu_usage', 'disk_writes', 'file_rename_count', 'process_count', 'label']
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"Dataset generated: {output_file}")
    print(f"Total samples: {num_samples}")
    print(f"Normal samples: {normal_samples}")
    print(f"Ransomware samples: {ransomware_samples}")
    
    return data

if __name__ == "__main__":
    # Generate the dataset
    dataset = generate_ransomware_dataset(1000, 'ransomware_dataset.csv')
    
    # Display sample data
    print("\nSample data (first 10 rows):")
    print("CPU Usage | Disk Writes | File Renames | Process Count | Label")
    print("-" * 65)
    for i in range(10):
        row = dataset[i]
        print(f"{row[0]:8.2f} | {row[1]:10.2f} | {row[2]:11d} | {row[3]:12d} | {row[4]:5d}")