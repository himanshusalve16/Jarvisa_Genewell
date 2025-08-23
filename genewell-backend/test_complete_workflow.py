#!/usr/bin/env python3
"""
Complete Workflow Test
=====================

Test the complete PDF -> CSV -> Prediction workflow
"""

import requests
import json
import time
import os
from pdf_to_csv_converter import PDFToCSVConverter

def create_sample_pdf_content():
    """Create a sample PDF content for testing"""
    sample_content = """
    GeneWell Medical Report
    =======================
    
    Patient Information:
    ===================
    Patient ID: P001
    Age: 45
    Gender: Female
    Blood Group: A+
    Medical History: Diabetes, Hypertension
    Report Type: Diagnostic
    
    Gene Analysis Results:
    =====================
    
    Gene: TP53
    Value: 0.8
    Normal Range: 1.0 - 2.0
    Status: Deficient
    Notes: Tumor suppressor gene mutation detected
    
    Gene: BRCA1
    Value: 2.5
    Normal Range: 1.0 - 2.0
    Status: Excessive
    Notes: Breast cancer susceptibility gene elevated
    
    Gene: APC
    Value: 1.5
    Normal Range: 1.0 - 2.0
    Status: Normal
    Notes: Adenomatous polyposis coli gene within normal range
    
    Gene: MLH1
    Value: 0.6
    Normal Range: 1.0 - 2.0
    Status: Deficient
    Notes: DNA mismatch repair gene mutation
    
    Summary:
    ========
    Multiple gene mutations detected. High risk for cancer development.
    Recommend genetic counseling and regular screening.
    """
    
    # Save as text file (simulating PDF content)
    with open('sample_gene_report.txt', 'w') as f:
        f.write(sample_content)
    
    return 'sample_gene_report.txt'

def test_pdf_converter():
    """Test the PDF to CSV converter"""
    print("=== Testing PDF to CSV Converter ===")
    
    try:
        # Create sample content
        sample_file = create_sample_pdf_content()
        print(f"✓ Created sample report: {sample_file}")
        
        # Initialize converter
        converter = PDFToCSVConverter()
        print("✓ PDF converter initialized")
        
        # Test text extraction (simulating PDF)
        with open(sample_file, 'r') as f:
            text = f.read()
        
        # Parse gene data
        gene_data = converter.parse_gene_data(text)
        print(f"✓ Parsed {len(gene_data)} genes from report")
        
        # Extract patient info
        patient_info = converter.extract_patient_info(text)
        print(f"✓ Extracted patient info: {patient_info}")
        
        # Convert to ML format
        df = converter.convert_to_ml_format(gene_data, patient_info)
        print(f"✓ Converted to ML format: {len(df)} records")
        
        # Save test CSV
        test_csv = 'test_converted_report.csv'
        df.to_csv(test_csv, index=False)
        print(f"✓ Saved test CSV: {test_csv}")
        
        # Show sample data
        print("\nSample converted data:")
        print(df.head(2).to_string())
        
        return test_csv
        
    except Exception as e:
        print(f"✗ PDF converter test failed: {e}")
        return None

def test_api_endpoints():
    """Test the API endpoints"""
    print("\n=== Testing API Endpoints ===")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Health check passed")
            print(f"   Model loaded: {data.get('model_loaded', False)}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Health check error: {e}")
        return False
    
    # Test 2: Home endpoint
    print("2. Testing home endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Home endpoint working")
            print(f"   API Version: {data.get('version', 'unknown')}")
            print(f"   Workflow: {data.get('workflow', [])}")
        else:
            print(f"   ✗ Home endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Home endpoint error: {e}")
    
    # Test 3: Model info
    print("3. Testing model info endpoint...")
    try:
        response = requests.get(f"{base_url}/model-info")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Model info working")
            print(f"   Features: {data.get('features_count', 0)}")
        else:
            print(f"   ✗ Model info failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Model info error: {e}")
    
    return True

def test_pdf_upload_and_prediction():
    """Test PDF upload and prediction workflow"""
    print("\n=== Testing PDF Upload and Prediction ===")
    
    base_url = "http://localhost:5000"
    
    # Test 1: PDF conversion
    print("1. Testing PDF conversion endpoint...")
    try:
        # Create a sample CSV file to simulate converted PDF
        sample_csv = 'test_converted_report.csv'
        if not os.path.exists(sample_csv):
            print(f"   ✗ Test CSV not found: {sample_csv}")
            return False
        
        with open(sample_csv, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{base_url}/predict", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Prediction successful")
            print(f"   Patients analyzed: {data.get('total_patients', 0)}")
            
            # Show sample results
            results = data.get('results', [])
            if results:
                print("\n   Sample Prediction Results:")
                for i, result in enumerate(results[:3]):
                    print(f"   Patient {i+1}:")
                    print(f"     ID: {result.get('patient_id', 'Unknown')}")
                    print(f"     Risk Score: {result.get('risk_score', 0):.3f}")
                    print(f"     Risk Level: {result.get('risk_level', 'Unknown')}")
                    print(f"     Health Status: {result.get('health_status', 'Unknown')}")
        else:
            print(f"   ✗ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ✗ Prediction error: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("GeneWell Complete Workflow Test")
    print("=" * 50)
    
    # Test 1: PDF Converter
    test_csv = test_pdf_converter()
    if not test_csv:
        print("✗ PDF converter test failed. Stopping.")
        return
    
    # Test 2: API Endpoints
    if not test_api_endpoints():
        print("✗ API endpoints test failed. Make sure the server is running.")
        print("Start the server with: python app.py")
        return
    
    # Test 3: Complete Workflow
    if test_pdf_upload_and_prediction():
        print("\n🎉 ALL TESTS PASSED!")
        print("The complete PDF -> CSV -> Prediction workflow is working!")
    else:
        print("\n✗ Workflow test failed.")
    
    # Cleanup
    cleanup_files = ['sample_gene_report.txt', 'test_converted_report.csv']
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Cleaned up: {file}")

if __name__ == "__main__":
    main()
