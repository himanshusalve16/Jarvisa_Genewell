#!/usr/bin/env python3
"""
GeneWell Integration Test Script
================================

This script tests the integration between frontend and backend
to ensure everything is working properly.
"""

import requests
import json
import time
import os
from pathlib import Path

def test_backend_health():
    """Test backend health endpoint"""
    print("Testing backend health...")
    try:
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is healthy")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Model loaded: {data.get('model_loaded', False)}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_model_info():
    """Test model information endpoint"""
    print("\nTesting model information...")
    try:
        response = requests.get('http://localhost:5000/model-info', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model information retrieved")
            print(f"   Model loaded: {data.get('model_loaded', False)}")
            print(f"   Features count: {data.get('features_count', 'N/A')}")
            return True
        else:
            print(f"⚠️  Model info check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Model info request failed: {e}")
        return False

def test_sample_data_download():
    """Test sample data download"""
    print("\nTesting sample data download...")
    try:
        response = requests.get('http://localhost:5000/sample-data', timeout=10)
        if response.status_code == 200:
            print(f"✅ Sample data download successful")
            print(f"   Content length: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ Sample data download failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Sample data download failed: {e}")
        return False

def test_frontend_connection():
    """Test frontend connection"""
    print("\nTesting frontend connection...")
    try:
        response = requests.get('http://localhost:3000', timeout=5)
        if response.status_code == 200:
            print(f"✅ Frontend is accessible")
            return True
        else:
            print(f"❌ Frontend connection failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def test_file_upload():
    """Test file upload functionality"""
    print("\nTesting file upload...")
    
    # Create a sample CSV file for testing
    sample_data = """patient_id,age,gender,blood_group,bmi,gene_id,disease_name,score
P001,45,Female,A+,26.5,7157,Breast cancer,0.85
P002,52,Male,B+,28.1,675,Ovarian cancer,0.92"""
    
    # Save sample file
    test_file_path = "test_sample.csv"
    with open(test_file_path, 'w') as f:
        f.write(sample_data)
    
    try:
        # Upload the test file
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test_sample.csv', f, 'text/csv')}
            response = requests.post('http://localhost:5000/predict', files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ File upload successful")
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Total patients: {data.get('total_patients', 0)}")
            
            if 'results' in data and data['results']:
                print(f"   Sample result: {data['results'][0]}")
            
            return True
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ File upload request failed: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists(test_file_path):
            os.remove(test_file_path)

def test_api_endpoints():
    """Test all API endpoints"""
    print("\nTesting API endpoints...")
    
    endpoints = [
        ('/', 'GET', 'API Information'),
        ('/health', 'GET', 'Health Check'),
        ('/model-info', 'GET', 'Model Information'),
    ]
    
    all_passed = True
    
    for endpoint, method, description in endpoints:
        try:
            if method == 'GET':
                response = requests.get(f'http://localhost:5000{endpoint}', timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {description}: {endpoint}")
            else:
                print(f"❌ {description}: {endpoint} - Status {response.status_code}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: {endpoint} - Error {e}")
            all_passed = False
    
    return all_passed

def main():
    """Main test function"""
    print("GeneWell Integration Test")
    print("=" * 50)
    
    # Wait a moment for servers to be ready
    print("Waiting for servers to be ready...")
    time.sleep(2)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Model Information", test_model_info),
        ("Sample Data Download", test_sample_data_download),
        ("Frontend Connection", test_frontend_connection),
        ("API Endpoints", test_api_endpoints),
        ("File Upload", test_file_upload),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the system configuration.")
    
    print("\nNext steps:")
    print("1. Open http://localhost:3000 in your browser")
    print("2. Navigate to 'Upload Report' page")
    print("3. Check the system status")
    print("4. Download sample data and test file upload")

if __name__ == "__main__":
    main()
