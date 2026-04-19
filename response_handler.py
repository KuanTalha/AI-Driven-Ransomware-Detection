import os
import shutil
import logging
from datetime import datetime

class ResponseHandler:
    def __init__(self, quarantine_dir='quarantine'):
        self.quarantine_dir = quarantine_dir
        self.setup_logging()
        self.setup_quarantine()
    
    def setup_logging(self):
        """Setup logging for threat responses"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ransomware_alerts.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_quarantine(self):
        """Create quarantine directory if it doesn't exist"""
        if not os.path.exists(self.quarantine_dir):
            os.makedirs(self.quarantine_dir)
    
    def handle_threat(self, threat_result, process_id=None, affected_files=None):
        """
        Handle detected ransomware threat
        
        Args:
            threat_result: Dict from detector with threat_score, is_threat, alert_level
            process_id: Process ID to terminate (for simulation)
            affected_files: List of file paths to quarantine
        """
        if not threat_result['is_threat']:
            return
        
        score = threat_result['threat_score']
        level = threat_result['alert_level']
        
        # Log warning
        self.log_threat(score, level)
        
        # Print alert
        self.print_alert(score, level)
        
        # Terminate suspicious process (simulation)
        if process_id:
            self.terminate_process(process_id)
        
        # Quarantine affected files
        if affected_files:
            self.quarantine_files(affected_files)
    
    def log_threat(self, score, level):
        """Log threat detection"""
        self.logger.warning(f"RANSOMWARE THREAT DETECTED - Score: {score:.3f}, Level: {level}")
    
    def print_alert(self, score, level):
        """Print clear alert message"""
        print("\n" + "="*50)
        print("🚨 RANSOMWARE THREAT DETECTED 🚨")
        print(f"Threat Score: {score:.3f}")
        print(f"Alert Level: {level}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*50)
    
    def terminate_process(self, process_id):
        """Simulate process termination (demo safe)"""
        print(f"🛑 SIMULATING: Terminating suspicious process {process_id}")
        self.logger.info(f"Simulated termination of process {process_id}")
        # In real implementation: os.kill(process_id, signal.SIGTERM)
    
    def quarantine_files(self, file_paths):
        """Move affected files to quarantine folder"""
        quarantined = []
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    filename = os.path.basename(file_path)
                    quarantine_path = os.path.join(self.quarantine_dir, filename)
                    
                    # Handle duplicate names
                    counter = 1
                    while os.path.exists(quarantine_path):
                        name, ext = os.path.splitext(filename)
                        quarantine_path = os.path.join(self.quarantine_dir, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    shutil.move(file_path, quarantine_path)
                    quarantined.append(quarantine_path)
                    print(f"🔒 Quarantined: {file_path} -> {quarantine_path}")
                    
                except Exception as e:
                    self.logger.error(f"Failed to quarantine {file_path}: {e}")
        
        if quarantined:
            self.logger.info(f"Quarantined {len(quarantined)} files")

# Example usage
if __name__ == "__main__":
    handler = ResponseHandler()
    
    # Simulate threat detection
    threat_result = {
        'threat_score': 0.85,
        'is_threat': True,
        'alert_level': 'HIGH'
    }
    
    # Demo response
    handler.handle_threat(
        threat_result,
        process_id=1234,
        affected_files=['demo_file.txt']  # Create this file for testing
    )