#!/usr/bin/env python
"""
Quick setup and run script for the Image Classification Web App
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is 3.7+"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_streamlit_app():
    """Run the Streamlit application"""
    print("\n🚀 Starting the web app...")
    print("The app will open in your browser at: http://localhost:8501")
    print("\nTo stop the app, press Ctrl+C in the terminal\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 App stopped")
    except Exception as e:
        print(f"❌ Error running app: {e}")
        return False
    return True

def main():
    print("="*60)
    print(" Image Classification Web App - Setup & Run")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        sys.exit(1)
    
    # Install dependencies
    if not install_requirements():
        sys.exit(1)
    
    # Run the app
    if not run_streamlit_app():
        sys.exit(1)

if __name__ == "__main__":
    main()
