#!/usr/bin/env python3
"""
GeneWell ML System Startup Script
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'sklearn', 'xgboost', 
        'matplotlib', 'seaborn', 'joblib', 'flask', 
        'flask_cors', 'plotly', 'openpyxl', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"+ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"- {package} - MISSING")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install missing packages using:")
        print("pip install -r requirements.txt")
        return False
    
    print("+ All dependencies are installed!")
    return True

def train_model():
    """Train the ML model"""
    print("\n=== Training ML Model ===")
    
    try:
        from personalized_predictor import PersonalizedPredictor
        
        # Initialize predictor
        predictor = PersonalizedPredictor()
        
        # Check if model already exists
        if os.path.exists('personalized_model.pkl'):
            print("+ Model already exists, loading...")
            predictor.load_model('personalized_model.pkl')
            return True
        
        print("Training new model...")
        
        # Load and preprocess data
        print("1. Loading and preprocessing data...")
        X, y = predictor.load_and_preprocess()
        
        # Train model
        print("2. Training model...")
        predictor.train_model(X, y)
        
        # Save model
        print("3. Saving model...")
        predictor.save_model('personalized_model.pkl')
        
        print("+ Model trained and saved successfully!")
        return True
        
    except Exception as e:
        print(f"- Error training model: {e}")
        return False

def start_api_server():
    """Start the Flask API server"""
    print("\n=== Starting API Server ===")
    
    try:
        # Check if server is already running
        try:
            response = requests.get('http://localhost:5000/health', timeout=2)
            if response.status_code == 200:
                print("+ API server is already running!")
                return True
        except:
            pass
        
        print("Starting API server...")
        
        # Start the server in a subprocess
        server_process = subprocess.Popen([
            sys.executable, 'app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        # Check if server started successfully
        try:
            response = requests.get('http://localhost:5000/health', timeout=5)
            if response.status_code == 200:
                print("+ API server started successfully!")
                print("Server URL: http://localhost:5000")
                return True
            else:
                print(f"- Server started but health check failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("- Server failed to start or health check failed")
            return False
            
    except Exception as e:
        print(f"- Error starting server: {e}")
        return False

def run_tests():
    """Run the test suite"""
    print("\n=== Running Tests ===")
    
    try:
        result = subprocess.run([
            sys.executable, 'test_pipeline.py'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"- Error running tests: {e}")
        return False

def show_menu():
    """Show the main menu"""
    print("\n" + "=" * 50)
    print("GeneWell ML System")
    print("=" * 50)
    print("1. Check Dependencies")
    print("2. Train Model")
    print("3. Start API Server")
    print("4. Run Tests")
    print("5. Full Setup (Dependencies + Train + Server)")
    print("6. Exit")
    print("=" * 50)

def main():
    """Main function"""
    print("GeneWell ML System Startup")
    print("=" * 50)
    
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                check_dependencies()
                
            elif choice == '2':
                if check_dependencies():
                    train_model()
                else:
                    print("Please install missing dependencies first.")
                    
            elif choice == '3':
                if check_dependencies():
                    start_api_server()
                else:
                    print("Please install missing dependencies first.")
                    
            elif choice == '4':
                if check_dependencies():
                    run_tests()
                else:
                    print("Please install missing dependencies first.")
                    
            elif choice == '5':
                print("\n=== Full Setup ===")
                
                # Check dependencies
                if not check_dependencies():
                    print("Please install missing dependencies first.")
                    continue
                
                # Train model
                if not train_model():
                    print("Model training failed. Please check the errors above.")
                    continue
                
                # Start server
                if not start_api_server():
                    print("Server startup failed. Please check the errors above.")
                    continue
                
                print("\n+ Full setup completed successfully!")
                print("API server is running at: http://localhost:5000")
                print("You can now use the API endpoints or integrate with the frontend.")
                
            elif choice == '6':
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
