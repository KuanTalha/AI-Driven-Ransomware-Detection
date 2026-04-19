#!/usr/bin/env python3
"""
Ransomware Behavior Simulator for Demo Purposes
Simulates ransomware-like behavior patterns for testing the detection system
"""

import os
import time
import random
import threading
import psutil
from datetime import datetime

class RansomwareSimulator:
    def __init__(self, intensity='medium'):
        self.intensity = intensity
        self.running = False
        self.created_files = []
        
    def simulate_file_encryption(self, file_count=50):
        """Simulate rapid file creation and encryption"""
        print(f"🦠 Simulating file encryption ({file_count} files)...")
        
        # Create temporary directory
        sim_dir = "ransomware_simulation"
        os.makedirs(sim_dir, exist_ok=True)
        
        for i in range(file_count):
            if not self.running:
                break
                
            # Create original file
            original_file = f"{sim_dir}/document_{i}.txt"
            with open(original_file, 'w') as f:
                f.write(f"Important document {i} content " + "X" * 500)
            
            self.created_files.append(original_file)
            
            # Simulate encryption by creating .encrypted version
            encrypted_file = f"{original_file}.encrypted"
            with open(encrypted_file, 'wb') as f:
                f.write(b"ENCRYPTED_DATA_" + os.urandom(100))
            
            self.created_files.append(encrypted_file)
            
            # Delete original (simulate encryption)
            try:
                os.remove(original_file)
            except:
                pass
            
            # Rapid file operations
            time.sleep(0.05 if self.intensity == 'high' else 0.1)
        
        print(f"✅ File encryption simulation complete")
    
    def simulate_cpu_spike(self, duration=10):
        """Simulate high CPU usage"""
        print(f"🔥 Simulating CPU spike for {duration} seconds...")
        
        def cpu_intensive_task():
            end_time = time.time() + duration
            while time.time() < end_time and self.running:
                # CPU intensive operations
                for _ in range(10000):
                    _ = random.random() ** 2
                    _ = hash(str(random.random()))
        
        # Start multiple threads based on intensity
        thread_count = 2 if self.intensity == 'low' else 4 if self.intensity == 'medium' else 8
        threads = []
        
        for _ in range(thread_count):
            t = threading.Thread(target=cpu_intensive_task)
            t.start()
            threads.append(t)
        
        # Wait for completion
        for t in threads:
            t.join()
        
        print("✅ CPU spike simulation complete")
    
    def simulate_memory_usage(self, duration=5):
        """Simulate memory consumption"""
        print(f"💾 Simulating memory usage for {duration} seconds...")
        
        # Allocate memory blocks
        memory_blocks = []
        block_size = 1024 * 1024  # 1MB blocks
        
        try:
            for i in range(50 if self.intensity == 'low' else 100):
                if not self.running:
                    break
                    
                block = bytearray(block_size)
                memory_blocks.append(block)
                time.sleep(0.1)
            
            # Hold memory for duration
            time.sleep(duration)
            
        except MemoryError:
            print("⚠️ Memory limit reached")
        finally:
            # Clean up memory
            memory_blocks.clear()
        
        print("✅ Memory usage simulation complete")
    
    def simulate_network_activity(self):
        """Simulate suspicious network patterns"""
        print("🌐 Simulating network activity...")
        
        # Simulate DNS lookups to suspicious domains
        suspicious_domains = [
            "ransom-payment.onion",
            "crypto-locker.tor",
            "pay-bitcoin.dark"
        ]
        
        for domain in suspicious_domains:
            if not self.running:
                break
            print(f"   📡 Simulated connection attempt to {domain}")
            time.sleep(0.5)
        
        print("✅ Network activity simulation complete")
    
    def create_ransom_note(self):
        """Create a simulated ransom note"""
        print("📝 Creating ransom note...")
        
        ransom_content = """
        ⚠️ RANSOMWARE SIMULATION - FOR DEMO PURPOSES ONLY ⚠️
        
        This is a SIMULATED ransom note for demonstration.
        
        Your files have been encrypted (simulated).
        To recover your files, you need to pay (THIS IS FAKE).
        
        Contact: demo@simulation.fake
        Bitcoin Address: 1DemoAddressNotReal123456789
        
        ⚠️ THIS IS NOT REAL RANSOMWARE ⚠️
        """
        
        with open("README_RANSOM_DEMO.txt", 'w') as f:
            f.write(ransom_content)
        
        self.created_files.append("README_RANSOM_DEMO.txt")
        print("✅ Ransom note created")
    
    def start_simulation(self, duration=30):
        """Start the complete ransomware simulation"""
        print("🚨 STARTING RANSOMWARE SIMULATION")
        print("=" * 50)
        print(f"Intensity: {self.intensity.upper()}")
        print(f"Duration: {duration} seconds")
        print(f"Start time: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 50)
        
        self.running = True
        
        # Phase 1: Initial file operations
        file_thread = threading.Thread(
            target=self.simulate_file_encryption, 
            args=(30 if self.intensity == 'low' else 50 if self.intensity == 'medium' else 100,)
        )
        file_thread.start()
        
        # Phase 2: CPU spike (parallel)
        time.sleep(2)
        cpu_thread = threading.Thread(
            target=self.simulate_cpu_spike, 
            args=(duration // 2,)
        )
        cpu_thread.start()
        
        # Phase 3: Memory usage
        time.sleep(5)
        memory_thread = threading.Thread(
            target=self.simulate_memory_usage,
            args=(duration // 3,)
        )
        memory_thread.start()
        
        # Phase 4: Network activity
        time.sleep(3)
        self.simulate_network_activity()
        
        # Phase 5: Create ransom note
        time.sleep(2)
        self.create_ransom_note()
        
        # Wait for all threads to complete
        file_thread.join()
        cpu_thread.join()
        memory_thread.join()
        
        print("\n🏁 RANSOMWARE SIMULATION COMPLETE")
        print(f"End time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Files created: {len(self.created_files)}")
    
    def stop_simulation(self):
        """Stop the simulation"""
        print("\n🛑 Stopping simulation...")
        self.running = False
    
    def cleanup(self):
        """Clean up simulation artifacts"""
        print("🧹 Cleaning up simulation files...")
        
        for file_path in self.created_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
        
        # Remove simulation directory
        try:
            if os.path.exists("ransomware_simulation"):
                import shutil
                shutil.rmtree("ransomware_simulation")
        except Exception as e:
            print(f"Error removing simulation directory: {e}")
        
        self.created_files.clear()
        print("✅ Cleanup complete")

def main():
    """Main function for running the simulator"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ransomware Behavior Simulator")
    parser.add_argument('--intensity', choices=['low', 'medium', 'high'], 
                       default='medium', help='Simulation intensity')
    parser.add_argument('--duration', type=int, default=30, 
                       help='Simulation duration in seconds')
    parser.add_argument('--cleanup', action='store_true', 
                       help='Clean up previous simulation files')
    
    args = parser.parse_args()
    
    simulator = RansomwareSimulator(intensity=args.intensity)
    
    if args.cleanup:
        simulator.cleanup()
        return
    
    try:
        simulator.start_simulation(duration=args.duration)
    except KeyboardInterrupt:
        print("\n⚠️ Simulation interrupted by user")
        simulator.stop_simulation()
    finally:
        # Ask user if they want to clean up
        response = input("\nClean up simulation files? (y/n): ").lower()
        if response == 'y':
            simulator.cleanup()

if __name__ == "__main__":
    main()