#!/usr/bin/env python3
"""
Test script for GeneWell ML Pipeline
"""

import requests
import json
import time
import os
from personalized_predictor import PersonalizedPredictor

def test_ml_pipeline():
    """Test the ML pipeline directly"""
    print("=== Testing ML Pipeline ===")
    
    try:
        # Initialize predictor
        predictor = PersonalizedPredictor()
        print("+ Predictor initialized")
        
        # Load and preprocess data
        X, y = predictor.load_and_preprocess()
        print(f"+ Loaded and preprocessed data: {X.shape[0]} samples, {X.shape[1]} features")
        
        # Train model
        predictor.train_model(X, y)
        print("+ Model trained successfully")
        
        # Test prediction with sample data
        sample_data = {
            'age': 45,
            'gender': 'Female',
            'blood_group': 'A+',
            'bmi': 24.5,
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'age_factor': 1.1,
            'gender_factor': 1.0,
            'medical_factor': 1.2,
            'family_factor': 1.1,
            'lifestyle_factor': 0.9,
            'bmi_factor': 1.0
        }
        
        risk_score = predictor.predict_risk(sample_data)
        print(f"+ Risk prediction completed: {risk_score:.3f}")
        
        # Display sample results
        print(f"\nSample Prediction Results:")
        print(f"  Risk Score: {risk_score:.3f}")
        print(f"  Risk Level: {'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low'}")
        print(f"  Patient Age: {sample_data['age']}")
        print(f"  Patient Gender: {sample_data['gender']}")
        print(f"  Blood Group: {sample_data['blood_group']}")
        
        return True
        
    except Exception as e:
        print(f"- Pipeline test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n=== Testing API Endpoints ===")
    
    base_url = "http://localhost:5000"
    
    try:
        # Test health endpoint
        print("Testing health endpoint...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("+ Health endpoint working")
            health_data = response.json()
            print(f"  Model loaded: {health_data.get('model_loaded', False)}")
        else:
            print(f"- Health endpoint failed: {response.status_code}")
            return False
        
        # Test model info endpoint
        print("Testing model info endpoint...")
        response = requests.get(f"{base_url}/model-info")
        if response.status_code == 200:
            print("+ Model info endpoint working")
            model_info = response.json()
            print(f"  Features: {model_info.get('features_count', 0)}")
            print(f"  Diseases: {model_info.get('diseases_count', 0)}")
        else:
            print(f"- Model info endpoint failed: {response.status_code}")
        
        # Test sample data download
        print("Testing sample data download...")
        response = requests.get(f"{base_url}/sample-data")
        if response.status_code == 200:
            print("+ Sample data download working")
            with open('test_sample.csv', 'wb') as f:
                f.write(response.content)
            print("  Sample data saved as 'test_sample.csv'")
        else:
            print(f"- Sample data download failed: {response.status_code}")
        
        # Test prediction endpoint
        print("Testing prediction endpoint...")
        if os.path.exists('test_sample.csv'):
            with open('test_sample.csv', 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{base_url}/predict", files=files)
            
            if response.status_code == 200:
                print("+ Prediction endpoint working")
                pred_data = response.json()
                print(f"  Predictions made for {pred_data.get('total_patients', 0)} patients")
                
                # Display sample prediction
                if pred_data.get('results'):
                    sample_result = pred_data['results'][0]
                    print(f"  Sample patient: {sample_result['patient_id']}")
                    print(f"  Health status: {sample_result['health_status']}")
            else:
                print(f"- Prediction endpoint failed: {response.status_code}")
                print(f"  Response: {response.text}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("- Cannot connect to API server. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"- API test failed: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n=== Testing Batch Prediction ===")
    
    base_url = "http://localhost:5000"
    
    try:
        # Create sample batch data
        batch_data = {
            "patients": [
                {
                    "Patient_ID": "TEST001",
                    "Age": 45,
                    "Gender": "Male",
                    "Blood_Group": "A+",
                    "Medical_History": "None",
                    "Report_Type": "Routine",
                    "BRCA1_Value": 1.2,
                    "BRCA1_Normal_Min": 0.8,
                    "BRCA1_Normal_Max": 1.5,
                    "BRCA2_Value": 1.1,
                    "BRCA2_Normal_Min": 0.9,
                    "BRCA2_Normal_Max": 1.4,
                    "INS_Value": 0.6,
                    "INS_Normal_Min": 0.8,
                    "INS_Normal_Max": 1.2,
                    "APOE_Value": 2.1,
                    "APOE_Normal_Min": 1.0,
                    "APOE_Normal_Max": 1.8
                },
                {
                    "Patient_ID": "TEST002",
                    "Age": 35,
                    "Gender": "Female",
                    "Blood_Group": "O+",
                    "Medical_History": "None",
                    "Report_Type": "Screening",
                    "BRCA1_Value": 0.7,
                    "BRCA1_Normal_Min": 0.8,
                    "BRCA1_Normal_Max": 1.5,
                    "BRCA2_Value": 0.8,
                    "BRCA2_Normal_Min": 0.9,
                    "BRCA2_Normal_Max": 1.4,
                    "INS_Value": 1.0,
                    "INS_Normal_Min": 0.8,
                    "INS_Normal_Max": 1.2,
                    "APOE_Value": 1.5,
                    "APOE_Normal_Min": 1.0,
                    "APOE_Normal_Max": 1.8
                }
            ]
        }
        
        # Send batch prediction request
        response = requests.post(
            f"{base_url}/predict-batch",
            json=batch_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("+ Batch prediction working")
            batch_results = response.json()
            print(f"  Predictions made for {batch_results.get('total_patients', 0)} patients")
            
            # Display results
            for result in batch_results.get('results', []):
                print(f"  Patient {result['patient_id']}: {result['health_status']}")
                print(f"    Risk factors: {len(result['risk_factors'])}")
        else:
            print(f"- Batch prediction failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"- Batch prediction test failed: {e}")
        return False

def test_export_report():
    """Test report export functionality"""
    print("\n=== Testing Report Export ===")
    
    base_url = "http://localhost:5000"
    
    try:
        # Create sample results data
        sample_results = [
            {
                "patient_id": "TEST001",
                "health_status": "High Risk",
                "risk_factors": ["High risk for Diabetes_Type_1", "High risk for Breast_Cancer"],
                "predictions": {
                    "Diabetes_Type_1": {"predicted": True, "probability": 0.85},
                    "Breast_Cancer": {"predicted": True, "probability": 0.78},
                    "Hypertension": {"predicted": False, "probability": 0.25}
                }
            },
            {
                "patient_id": "TEST002",
                "health_status": "Normal",
                "risk_factors": [],
                "predictions": {
                    "Diabetes_Type_1": {"predicted": False, "probability": 0.15},
                    "Breast_Cancer": {"predicted": False, "probability": 0.22},
                    "Hypertension": {"predicted": False, "probability": 0.18}
                }
            }
        ]
        
        # Send export request
        response = requests.post(
            f"{base_url}/export-report",
            json={"results": sample_results},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            print("+ Report export working")
            report_data = response.json()
            print(f"  Report generated for {report_data.get('total_patients', 0)} patients")
            print(f"  Summary: {report_data.get('summary', {})}")
        else:
            print(f"- Report export failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"- Report export test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("GeneWell ML Pipeline Test Suite")
    print("=" * 50)
    
    # Test ML pipeline
    pipeline_success = test_ml_pipeline()
    
    # Test API endpoints (only if server is running)
    api_success = test_api_endpoints()
    
    # Test batch prediction
    batch_success = test_batch_prediction()
    
    # Test report export
    export_success = test_export_report()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"ML Pipeline: {'+ PASS' if pipeline_success else '- FAIL'}")
    print(f"API Endpoints: {'+ PASS' if api_success else '- FAIL'}")
    print(f"Batch Prediction: {'+ PASS' if batch_success else '- FAIL'}")
    print(f"Report Export: {'+ PASS' if export_success else '- FAIL'}")
    
    # Cleanup
    if os.path.exists('test_sample.csv'):
        os.remove('test_sample.csv')
        print("\nCleaned up test files")
    
    print("\nTest suite completed!")

if __name__ == "__main__":
    main()
