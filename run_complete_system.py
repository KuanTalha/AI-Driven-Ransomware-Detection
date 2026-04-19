#!/usr/bin/env python3
"""
AI-Driven Ransomware Detection System - Complete Launcher
Starts both the detection system and web dashboard
"""

import subprocess
import sys
import time
import threading
import webbrowser
from pathlib import Path

def start_dashboard():
    """Start the Streamlit dashboard"""
    print("Starting web dashboard...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "false"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Dashboard failed to start: {e}")
    except KeyboardInterrupt:
        print("Dashboard stopped")

def start_detection_system():
    """Start the main detection system"""
    print("Starting detection system...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Detection system failed to start: {e}")
    except KeyboardInterrupt:
        print("Detection system stopped")

def main():
    """Main launcher"""
    print("AI-Driven Ransomware Detection System")
    print("=" * 50)
    print()
    
    # Check if we're in the right directory
    if not Path("main.py").exists() or not Path("app.py").exists():
        print("Error: Please run this script from the project directory")
        print("   Make sure main.py and app.py are in the current directory")
        sys.exit(1)
    
    print("Starting system components...")
    print("Dashboard will be available at: http://localhost:8501")
    print("Detection system will run in this terminal")
    print()
    print("Press Ctrl+C to stop both components")
    print()
    
    # Start dashboard in a separate thread
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    dashboard_thread.start()
    
    # Wait a moment for dashboard to start
    time.sleep(3)
    
    # Try to open browser
    try:
        webbrowser.open("http://localhost:8501")
        print("Opening dashboard in browser...")
    except Exception:
        print("Please manually open http://localhost:8501 in your browser")
    
    print()
    
    # Start detection system in main thread
    try:
        start_detection_system()
    except KeyboardInterrupt:
        print("\nShutting down system...")
        print("System stopped successfully")

if __name__ == "__main__":
    main()