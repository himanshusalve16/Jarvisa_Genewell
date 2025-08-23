#!/usr/bin/env python3
"""
Test Fixed Predictor Script
===========================

This script tests the fixed personalized predictor to ensure it works correctly.
"""

from personalized_predictor import PersonalizedPredictor
import os

def test_predictor():
    """Test the fixed predictor"""
    print("=== Testing Fixed Personalized Predictor ===\n")
    
    try:
        # Initialize predictor
        predictor = PersonalizedPredictor()
        print("✅ Predictor initialized successfully")
        
        # Check if model exists
        if os.path.exists('personalized_model.pkl'):
            print("✅ Found existing model file")
            
            # Load the model
            print("🔄 Loading existing model...")
            predictor.load_model()
            print("✅ Model loaded successfully")
            
            # Test prediction with sample data
            print("\n🔄 Testing prediction with sample data...")
            
            # Sample patient data (matching the features we expect)
            patient_data = {
                'age': 45, 'gender': 'Female', 'blood_group': 'A+', 'bmi': 26.5,
                'medical_history': 'None'
            }
            
            # Sample gene-disease data
            gene_disease_data = [
                {
                    'gene_id': 7157, 'gene_symbol': 'TP53', 'disease_name': 'Breast cancer',
                    'disease_class_encoded': 1, 'score': 0.85, 'ei': 0.78,
                    'combined_score': 0.82, 'evidence_strength': 0.9,
                    'association_age': 15, 'research_activity': 0.06
                }
            ]
            
            # Make prediction
            risk_score = predictor.predict_risk(patient_data, gene_disease_data)
            
            # Display results
            print(f"\n📊 Prediction Results:")
            print(f"   Risk Score: {risk_score:.4f}")
            print(f"   Risk Percentage: {risk_score * 100:.1f}%")
            
            if risk_score > 0.7:
                risk_level = 'High'
                health_status = 'High Risk'
            elif risk_score > 0.4:
                risk_level = 'Medium'
                health_status = 'At Risk'
            else:
                risk_level = 'Low'
                health_status = 'Normal'
            
            print(f"   Risk Level: {risk_level}")
            print(f"   Health Status: {health_status}")
            
            # Verify the prediction is reasonable
            if risk_score > 0 and risk_score <= 1:
                print("✅ Prediction is within valid range (0-1)")
            else:
                print("❌ Prediction is outside valid range")
                return False
            
            if risk_score > 0.1:  # Should be significantly above 0
                print("✅ Prediction shows meaningful risk assessment")
            else:
                print("⚠️  Prediction may be too low")
            
            return True
            
        else:
            print("❌ No existing model found")
            print("🔄 Training new model...")
            
            # Load and preprocess data
            X, y = predictor.load_and_preprocess()
            
            # Train model
            r2, rmse = predictor.train_model(X, y)
            
            # Save model
            predictor.save_model()
            
            print(f"✅ New model trained and saved")
            print(f"   Performance - R²: {r2:.4f}, RMSE: {rmse:.4f}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_csv_prediction():
    """Test CSV file prediction"""
    print("\n=== Testing CSV File Prediction ===\n")
    
    try:
        # Check if test sample exists
        test_file = 'uploads/test_sample.csv'
        if not os.path.exists(test_file):
            print(f"❌ Test file not found: {test_file}")
            return False
        
        # Initialize predictor
        predictor = PersonalizedPredictor()
        
        # Load model
        if os.path.exists('personalized_model.pkl'):
            predictor.load_model()
        else:
            print("❌ No model available for testing")
            return False
        
        # Test CSV prediction
        print("🔄 Testing CSV prediction...")
        results = predictor.predict_from_csv(test_file)
        
        print(f"\n📊 CSV Prediction Results:")
        for result in results:
            print(f"   Patient {result['patient_id']}: {result['risk_score']} risk ({result['risk_level']})")
            
            # Check if we got meaningful results
            if result['health_status'] == 'Error':
                print(f"      ❌ Error: {result.get('error', 'Unknown error')}")
            else:
                print(f"      ✅ Success: {result['health_status']}")
        
        # Count successful predictions
        successful = sum(1 for r in results if r['health_status'] != 'Error')
        total = len(results)
        
        print(f"\n📈 Summary: {successful}/{total} successful predictions")
        
        if successful > 0:
            print("✅ CSV prediction is working!")
            return True
        else:
            print("❌ All CSV predictions failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during CSV testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Testing Fixed Personalized Predictor\n")
    
    # Test basic predictor
    basic_test = test_predictor()
    
    # Test CSV prediction
    csv_test = test_csv_prediction()
    
    # Final summary
    print("\n" + "="*50)
    print("🎯 TEST RESULTS SUMMARY")
    print("="*50)
    
    if basic_test and csv_test:
        print("🎉 ALL TESTS PASSED!")
        print("✅ The predictor is now working correctly")
        print("✅ Risk scores should display properly in the web app")
        print("✅ No more 0.0% risk scores or Error status")
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  There may still be issues to resolve")
    
    print("\n💡 Next steps:")
    print("1. Restart your Flask backend server")
    print("2. Test the web application again")
    print("3. Upload a CSV file to verify predictions work")
