#!/usr/bin/env python3
"""
AI-Driven Ransomware Detection System - Main Integration Module
Integrates system monitoring, feature extraction, AI detection, and automated response
"""

import time
import threading
import signal
import sys
from datetime import datetime
import json

# Import system modules
from monitor.system_monitor import SystemMonitor
from features.feature_extractor import FeatureExtractor
from detection.detector import RansomwareDetector
from response.response_handler import ResponseHandler

class RansomwareDetectionSystem:
    def __init__(self):
        self.running = False
        self.monitor = None
        self.feature_extractor = FeatureExtractor(window_size=60)
        self.detector = RansomwareDetector(model_path='ransomware_model.pkl')
        self.response_handler = ResponseHandler()
        self.dashboard_data = {
            'detections': [],
            'system_metrics': [],
            'alerts': []
        }
        
    def activity_callback(self, activity):
        """Process system activity through the detection pipeline"""
        try:
            # Extract features from activity
            features = self.feature_extractor.update_buffer(activity)
            
            # Run AI detection
            is_threat, probability = self.detector.predict(features)
            
            # Store metrics for dashboard
            self.dashboard_data['system_metrics'].append({
                'timestamp': datetime.now().isoformat(),
                'activity': activity,
                'features': features.tolist(),
                'threat_probability': probability
            })
            
            # Trigger response if threat detected
            if is_threat:
                print(f"⚠️  THREAT DETECTED - Probability: {probability:.3f}")
                
                detection_data = {
                    'probability': probability,
                    'features': features.tolist(),
                    'activity': activity,
                    'timestamp': datetime.now().isoformat()
                }
                
                # Execute automated response
                response_actions = self.response_handler.handle_detection(detection_data)
                
                # Log for dashboard
                self.dashboard_data['detections'].append(detection_data)
                self.dashboard_data['alerts'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': f"Ransomware detected (p={probability:.3f})",
                    'actions': response_actions
                })
                
                # Save dashboard data
                self.save_dashboard_data()
                
            elif probability > 0.3:  # Elevated activity
                print(f"ℹ️  Elevated activity - Probability: {probability:.3f}")
                
        except Exception as e:
            print(f"Error in detection pipeline: {e}")
    
    def start_system(self):
        """Start the ransomware detection system"""
        print("🚀 Starting AI-Driven Ransomware Detection System...")
        
        try:
            # Initialize system monitor
            self.monitor = SystemMonitor(self.activity_callback)
            self.running = True
            
            # Start monitoring
            print("📡 Starting system monitoring...")
            observer = self.monitor.start_monitoring()
            
            print("✅ System monitoring active")
            print("🤖 AI detection engine ready")
            print("🛡️  Automated response system armed")
            print("📊 Dashboard data collection started")
            print("\n--- System Status ---")
            print("Press Ctrl+C to stop the system\n")
            
            # Main monitoring loop
            while self.running:
                # Display periodic status
                detection_summary = self.detector.get_detection_summary()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"Detections: {detection_summary['total_detections']} | "
                      f"Threats: {detection_summary['ransomware_detected']}")
                
                time.sleep(30)  # Status update every 30 seconds
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown signal received...")
            self.stop_system()
        except Exception as e:
            print(f"❌ System error: {e}")
            self.stop_system()
    
    def stop_system(self):
        """Stop the ransomware detection system"""
        print("🔄 Stopping system components...")
        
        self.running = False
        
        if self.monitor:
            self.monitor.stop_monitoring()
            print("✅ System monitoring stopped")
        
        # Save final dashboard data
        self.save_dashboard_data()
        print("✅ Dashboard data saved")
        
        # Print final summary
        detection_summary = self.detector.get_detection_summary()
        response_history = self.response_handler.get_response_history()
        
        print("\n--- Final Summary ---")
        print(f"Total detections: {detection_summary['total_detections']}")
        print(f"Ransomware detected: {detection_summary['ransomware_detected']}")
        print(f"Response actions: {len(response_history)}")
        print("🏁 System shutdown complete")
    
    def save_dashboard_data(self):
        """Save data for dashboard consumption"""
        try:
            with open('dashboard_data.json', 'w') as f:
                json.dump(self.dashboard_data, f, indent=2)
        except Exception as e:
            print(f"Error saving dashboard data: {e}")
    
    def get_system_status(self):
        """Get current system status"""
        return {
            'running': self.running,
            'detection_summary': self.detector.get_detection_summary(),
            'response_history': len(self.response_handler.get_response_history()),
            'dashboard_metrics': len(self.dashboard_data['system_metrics'])
        }

def signal_handler(sig, frame):
    """Handle shutdown signals gracefully"""
    print("\n🛑 Received shutdown signal")
    sys.exit(0)

def main():
    """Main entry point"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start the detection system
    detection_system = RansomwareDetectionSystem()
    
    try:
        detection_system.start_system()
    except Exception as e:
        print(f"❌ Failed to start system: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()