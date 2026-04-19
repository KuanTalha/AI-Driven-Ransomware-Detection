import psutil
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import defaultdict

class FileEventHandler(FileSystemEventHandler):
    """Handles file system events and tracks file operations"""
    
    def __init__(self):
        self.file_events = defaultdict(int)
        self.lock = threading.Lock()
    
    def on_created(self, event):
        if not event.is_directory:
            with self.lock:
                self.file_events['created'] += 1
    
    def on_deleted(self, event):
        if not event.is_directory:
            with self.lock:
                self.file_events['deleted'] += 1
    
    def on_moved(self, event):
        if not event.is_directory:
            with self.lock:
                self.file_events['renamed'] += 1
    
    def get_and_reset_counts(self):
        """Get current counts and reset them"""
        with self.lock:
            counts = dict(self.file_events)
            self.file_events.clear()
            return counts

class SystemMonitor:
    """Monitors system resources and file operations"""
    
    def __init__(self, watch_path="C:\\"):
        self.file_handler = FileEventHandler()
        self.observer = Observer()
        self.observer.schedule(self.file_handler, watch_path, recursive=True)
        self.observer.start()
        self.last_disk_io = psutil.disk_io_counters()
    
    def get_system_data(self):
        """Collect and return system monitoring data"""
        # CPU and memory usage
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        # Disk I/O metrics
        current_disk_io = psutil.disk_io_counters()
        disk_read_rate = current_disk_io.read_bytes - self.last_disk_io.read_bytes
        disk_write_rate = current_disk_io.write_bytes - self.last_disk_io.write_bytes
        self.last_disk_io = current_disk_io
        
        # Process information
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # File operation counts
        file_events = self.file_handler.get_and_reset_counts()
        
        return {
            'timestamp': time.time(),
            'cpu_usage': cpu_percent,
            'memory_usage': {
                'percent': memory.percent,
                'available_gb': memory.available / (1024**3),
                'used_gb': memory.used / (1024**3)
            },
            'disk_io': {
                'read_bytes_per_sec': disk_read_rate,
                'write_bytes_per_sec': disk_write_rate
            },
            'file_operations': {
                'created': file_events.get('created', 0),
                'deleted': file_events.get('deleted', 0),
                'renamed': file_events.get('renamed', 0)
            },
            'process_count': len(processes),
            'top_processes': sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:5]
        }
    
    def monitor_continuously(self, interval=5):
        """Continuously monitor system and yield data every interval seconds"""
        try:
            while True:
                yield self.get_system_data()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the file system observer"""
        self.observer.stop()
        self.observer.join()

# Example usage
if __name__ == "__main__":
    monitor = SystemMonitor()
    
    try:
        for data in monitor.monitor_continuously(interval=3):
            print(f"CPU: {data['cpu_usage']:.1f}% | "
                  f"Memory: {data['memory_usage']['percent']:.1f}% | "
                  f"Files Created: {data['file_operations']['created']} | "
                  f"Processes: {data['process_count']}")
    except KeyboardInterrupt:
        monitor.stop()
        print("\nMonitoring stopped.")