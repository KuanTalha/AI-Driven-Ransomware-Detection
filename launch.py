#!/usr/bin/env python3
"""
Quick launcher for the AI-Driven Ransomware Detection System
"""

import os
import sys

def check_dependencies():
    """Check if required modules are available"""
    required_modules = [
        'psutil', 'watchdog', 'sklearn', 'joblib', 'numpy'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print("❌ Missing required dependencies:")
        for module in missing:
            print(f"   - {module}")
        print("\nInstall with: pip install " + " ".join(missing))
        return False
    
    return True

def main():
    """Launch the detection system"""
    print("🛡️  AI-Driven Ransomware Detection System Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if model exists
    if not os.path.exists('ransomware_model.pkl'):
        print("⚠️  Model file not found. Training new model...")
        try:
            from model.train_model import RansomwareModelTrainer
            trainer = RansomwareModelTrainer()
            trainer.train_model()
            print("✅ Model training complete")
        except Exception as e:
            print(f"❌ Model training failed: {e}")
            print("System will use fallback detection")
    
    # Launch main system
    print("\n🚀 Launching detection system...")
    try:
        from main import main as run_main
        run_main()
    except Exception as e:
        print(f"❌ System launch failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()