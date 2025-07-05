#!/usr/bin/env python3
"""
OpenTrend - GitHub Trending Analyzer
Simple script to run the Streamlit application
"""

import subprocess
import sys
import os

def check_requirements():
    """Check if all required packages are installed."""
    required_packages = [
        ('streamlit', 'streamlit'),
        ('requests-html', 'requests_html'),
        ('beautifulsoup4', 'bs4'), 
        ('pandas', 'pandas'),
        ('matplotlib', 'matplotlib'),
        ('plotly', 'plotly'),
        ('seaborn', 'seaborn')
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them using:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def run_app():
    """Run the Streamlit application."""
    if not check_requirements():
        return
    
    print("🚀 Starting OpenTrend application...")
    print("🌐 The app will open in your default web browser")
    print("📍 URL: http://localhost:8501")
    print("\n🛑 Press Ctrl+C to stop the application\n")
    
    try:
        # Change to the script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    
    except KeyboardInterrupt:
        print("\n👋 OpenTrend application stopped!")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    run_app()
