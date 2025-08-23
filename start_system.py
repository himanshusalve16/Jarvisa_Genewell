#!/usr/bin/env python3
"""
GeneWell System Startup Script
==============================

This script helps you start both the backend and frontend servers
for the GeneWell ML system.
"""

import os
import sys
import subprocess
import time
import threading
import signal
import requests
from pathlib import Path

class GeneWellSystem:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = False
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("Checking system dependencies...")
        
        # Check Python
        try:
            python_version = sys.version_info
            if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
                print("❌ Python 3.8 or higher is required")
                return False
            print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        except Exception as e:
            print(f"❌ Python check failed: {e}")
            return False
        
        # Check Node.js
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js {result.stdout.strip()}")
            else:
                print("❌ Node.js not found")
                return False
        except FileNotFoundError:
            print("❌ Node.js not found. Please install Node.js 14 or higher")
            return False
        
        # Check npm
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ npm {result.stdout.strip()}")
            else:
                print("❌ npm not found")
                return False
        except FileNotFoundError:
            print("❌ npm not found")
            return False
        
        return True
    
    def setup_backend(self):
        """Setup and start the backend server"""
        print("\n=== Setting up Backend ===")
        
        backend_dir = Path("genewell-backend")
        if not backend_dir.exists():
            print("❌ Backend directory not found")
            return False
        
        # Change to backend directory
        os.chdir(backend_dir)
        
        # Install Python dependencies
        print("Installing Python dependencies...")
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Failed to install dependencies: {result.stderr}")
                return False
            print("✅ Dependencies installed")
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
        
        # Train model if needed
        print("Checking model status...")
        try:
            result = subprocess.run([sys.executable, 'run.py'], 
                                  input='2\n',  # Choose option 2 to train model
                                  capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                print(f"❌ Model training failed: {result.stderr}")
                return False
            print("✅ Model training completed")
        except subprocess.TimeoutExpired:
            print("⚠️  Model training timed out, but continuing...")
        except Exception as e:
            print(f"⚠️  Model training error: {e}, but continuing...")
        
        # Start backend server
        print("Starting backend server...")
        try:
            self.backend_process = subprocess.Popen([sys.executable, 'app.py'],
                                                  stdout=subprocess.PIPE,
                                                  stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(5)
            
            # Check if server is running
            try:
                response = requests.get('http://localhost:5000/health', timeout=5)
                if response.status_code == 200:
                    print("✅ Backend server started successfully")
                    print("   URL: http://localhost:5000")
                    return True
                else:
                    print(f"❌ Backend server health check failed: {response.status_code}")
                    return False
            except requests.exceptions.RequestException:
                print("❌ Backend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
    
    def setup_frontend(self):
        """Setup and start the frontend server"""
        print("\n=== Setting up Frontend ===")
        
        # Go back to root directory
        os.chdir(Path(__file__).parent)
        
        frontend_dir = Path("genewell-frontend")
        if not frontend_dir.exists():
            print("❌ Frontend directory not found")
            return False
        
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Install Node.js dependencies
        print("Installing Node.js dependencies...")
        try:
            result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Failed to install dependencies: {result.stderr}")
                return False
            print("✅ Dependencies installed")
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
        
        # Start frontend server
        print("Starting frontend server...")
        try:
            self.frontend_process = subprocess.Popen(['npm', 'start'],
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE)
            
            # Wait for server to start
            time.sleep(10)
            
            # Check if server is running
            try:
                response = requests.get('http://localhost:3000', timeout=5)
                if response.status_code == 200:
                    print("✅ Frontend server started successfully")
                    print("   URL: http://localhost:3000")
                    return True
                else:
                    print(f"⚠️  Frontend server may still be starting...")
                    return True
            except requests.exceptions.RequestException:
                print("⚠️  Frontend server may still be starting...")
                return True
                
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
    
    def start_system(self):
        """Start the complete GeneWell system"""
        print("GeneWell ML System Startup")
        print("=" * 50)
        
        # Check dependencies
        if not self.check_dependencies():
            print("\n❌ System dependencies not met. Please install required software.")
            return False
        
        # Setup backend
        if not self.setup_backend():
            print("\n❌ Backend setup failed")
            return False
        
        # Setup frontend
        if not self.setup_frontend():
            print("\n❌ Frontend setup failed")
            return False
        
        self.running = True
        
        print("\n" + "=" * 50)
        print("🎉 GeneWell System Started Successfully!")
        print("=" * 50)
        print("Backend API: http://localhost:5000")
        print("Frontend App: http://localhost:3000")
        print("\nPress Ctrl+C to stop the system")
        print("=" * 50)
        
        return True
    
    def stop_system(self):
        """Stop the GeneWell system"""
        print("\nStopping GeneWell system...")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            print("✅ Frontend server stopped")
        
        if self.backend_process:
            self.backend_process.terminate()
            print("✅ Backend server stopped")
        
        self.running = False
        print("GeneWell system stopped")

def signal_handler(signum, frame):
    """Handle Ctrl+C signal"""
    if hasattr(signal_handler, 'system'):
        signal_handler.system.stop_system()
    sys.exit(0)

def main():
    """Main function"""
    system = GeneWellSystem()
    signal_handler.system = system
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        if system.start_system():
            # Keep the system running
            while system.running:
                time.sleep(1)
    except KeyboardInterrupt:
        system.stop_system()
    except Exception as e:
        print(f"❌ System error: {e}")
        system.stop_system()

if __name__ == "__main__":
    main()
