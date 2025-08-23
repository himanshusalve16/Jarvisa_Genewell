#!/usr/bin/env python3
"""
Test script to verify the fixed model works with actual data
"""

import pandas as pd
from personalized_predictor import PersonalizedPredictor
import os

def test_model_with_actual_data():
    """Test the model with the actual data format"""
    print("=== Testing Model with Actual Data ===\n")
    
    # Initialize predictor
    predictor = PersonalizedPredictor()
    
    # Check if model exists
    if not os.path.exists('personalized_model.pkl'):
        print("❌ Model not found. Training new model...")
        try:
            # Load and preprocess data
            print("1. Loading and preprocessing data...")
            X, y = predictor.load_and_preprocess()
            
            # Train model
            print("2. Training model...")
            r2, rmse = predictor.train_model(X, y)
            
            # Save model
            print("3. Saving model...")
            predictor.save_model('personalized_model.pkl')
            print(f"✅ Model trained and saved. R²: {r2:.4f}, RMSE: {rmse:.4f}")
        except Exception as e:
            print(f"❌ Model training failed: {e}")
            return False
    else:
        print("✅ Loading existing model...")
        predictor.load_model('personalized_model.pkl')
    
    # Test with actual data
    print("\n=== Testing with Actual Data ===")
    
    # Load the test data
    test_data_path = 'uploads/test_sample.csv'
    if os.path.exists(test_data_path):
        print(f"Testing with: {test_data_path}")
        
        # Make predictions
        results = predictor.predict_from_csv(test_data_path)
        
        print("\n=== Prediction Results ===")
        for result in results:
            print(f"Patient {result['patient_id']}:")
            print(f"  Risk Score: {result['risk_score']}")
            print(f"  Risk Level: {result['risk_level']}")
            print(f"  Health Status: {result['health_status']}")
            if 'raw_score' in result:
                print(f"  Raw Score: {result['raw_score']:.4f}")
            print()
        
        return True
    else:
        print(f"❌ Test data not found: {test_data_path}")
        return False

if __name__ == "__main__":
    test_model_with_actual_data()
