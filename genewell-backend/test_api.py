#!/usr/bin/env python3
"""
Simple API Test Script
=====================

Test the GeneWell ML API endpoints
"""

import requests
import json
import time

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:5000"
    
    print("=== Testing GeneWell ML API ===\n")
    
    # Test 1: Health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Health check passed")
            print(f"   Model loaded: {data.get('model_loaded', False)}")
            print(f"   Status: {data.get('status', 'unknown')}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Health check error: {e}")
    
    # Test 2: Home endpoint
    print("\n2. Testing home endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Home endpoint working")
            print(f"   API Version: {data.get('version', 'unknown')}")
            print(f"   Available endpoints: {len(data.get('endpoints', {}))}")
        else:
            print(f"   ✗ Home endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Home endpoint error: {e}")
    
    # Test 3: Model info endpoint
    print("\n3. Testing model info endpoint...")
    try:
        response = requests.get(f"{base_url}/model-info")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Model info endpoint working")
            print(f"   Features count: {data.get('features_count', 0)}")
            print(f"   Model path: {data.get('model_path', 'unknown')}")
        else:
            print(f"   ✗ Model info failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Model info error: {e}")
    
    # Test 4: Sample data download
    print("\n4. Testing sample data download...")
    try:
        response = requests.get(f"{base_url}/sample-data")
        if response.status_code == 200:
            print(f"   ✓ Sample data download working")
            print(f"   Content length: {len(response.content)} bytes")
            
            # Save sample data
            with open('test_sample_data.csv', 'wb') as f:
                f.write(response.content)
            print(f"   Sample data saved as 'test_sample_data.csv'")
        else:
            print(f"   ✗ Sample data download failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Sample data error: {e}")
    
    # Test 5: Prediction endpoint (if sample data exists)
    print("\n5. Testing prediction endpoint...")
    try:
        with open('test_sample_data.csv', 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{base_url}/predict", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Prediction endpoint working")
            print(f"   Predictions made: {data.get('total_patients', 0)}")
            
            # Show sample results
            results = data.get('results', [])
            if results:
                sample = results[0]
                print(f"   Sample result:")
                print(f"     Patient ID: {sample.get('patient_id', 'Unknown')}")
                print(f"     Risk Score: {sample.get('risk_score', 0):.3f}")
                print(f"     Risk Level: {sample.get('risk_level', 'Unknown')}")
        else:
            print(f"   ✗ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ✗ Prediction error: {e}")
    
    print("\n=== API Test Complete ===")

if __name__ == "__main__":
    test_api()
