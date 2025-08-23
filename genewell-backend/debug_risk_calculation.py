#!/usr/bin/env python3
"""
Debug Risk Calculation
======================

Debug the risk calculation to find why NaN% is showing
"""

from personalized_predictor import PersonalizedPredictor
import pandas as pd

def debug_risk_calculation():
    """Debug the risk calculation step by step"""
    print("=== Debugging Risk Calculation ===\n")
    
    try:
        # Initialize predictor
        predictor = PersonalizedPredictor()
        print("✅ Predictor initialized")
        
        # Load model
        predictor.load_model()
        print("✅ Model loaded")
        
        # Test with a simple patient
        print("\n🔄 Testing with simple patient data...")
        
        patient_data = {
            'age': 45,
            'gender': 'Female',
            'blood_group': 'A+',
            'bmi': 26.5,
            'medical_history': 'None'
        }
        
        gene_disease_data = [{
            'gene_id': 7157,
            'gene_symbol': 'TP53',
            'disease_name': 'Breast Cancer',
            'disease_class_encoded': 1,
            'score': 0.85,
            'ei': 0.78,
            'combined_score': 0.82,
            'evidence_strength': 0.9,
            'association_age': 15,
            'research_activity': 0.06
        }]
        
        print(f"Patient data: {patient_data}")
        print(f"Gene disease data: {gene_disease_data}")
        
        # Test fallback risk calculation
        print("\n🔄 Testing fallback risk calculation...")
        fallback_risk = predictor._calculate_fallback_risk(patient_data, gene_disease_data)
        print(f"Fallback risk: {fallback_risk}")
        
        # Test simple risk calculation
        print("\n🔄 Testing simple risk calculation...")
        simple_risk = predictor._calculate_simple_risk(patient_data, gene_disease_data)
        print(f"Simple risk: {simple_risk}")
        
        # Test CSV prediction
        print("\n🔄 Testing CSV prediction...")
        
        # Create a simple test CSV
        test_data = [{
            'patient_id': 'TEST001',
            'age': 45,
            'gender': 'Female',
            'blood_group': 'A+',
            'bmi': 26.5,
            'medical_history': 'None',
            'gene_id': 7157,
            'gene_symbol': 'TP53',
            'disease_name': 'Breast Cancer',
            'disease_class_encoded': 1,
            'score': 0.85,
            'ei': 0.78,
            'combined_score': 0.82,
            'evidence_strength': 0.9,
            'association_age': 15,
            'research_activity': 0.06
        }]
        
        df = pd.DataFrame(test_data)
        test_file = 'test_debug.csv'
        df.to_csv(test_file, index=False)
        
        print(f"Created test CSV: {test_file}")
        
        # Test prediction
        results = predictor.predict_from_csv(test_file)
        print(f"Prediction results: {results}")
        
        # Clean up
        import os
        os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_risk_calculation()
