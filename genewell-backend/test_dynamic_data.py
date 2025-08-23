#!/usr/bin/env python3
"""
Test Dynamic Sample Data
========================

Test the predictor with the new dynamic sample data
"""

from personalized_predictor import PersonalizedPredictor

def test_dynamic_data():
    """Test the predictor with dynamic sample data"""
    print("=== Testing Dynamic Sample Data ===\n")
    
    try:
        # Initialize predictor
        predictor = PersonalizedPredictor()
        predictor.load_model()
        
        # Test with dynamic sample data
        results = predictor.predict_from_csv('uploads/dynamic_sample_data_20250823_100003.csv')
        
        print(f"📊 Results for {len(results)} patients:")
        print("=" * 60)
        
        # Show first 10 results
        for i, result in enumerate(results[:10]):
            print(f"{i+1:2d}. Patient {result['patient_id']}: {result['risk_score']} risk ({result['risk_level']}) - {result['health_status']}")
        
        if len(results) > 10:
            print(f"   ... and {len(results) - 10} more patients")
        
        # Count risk levels
        high_count = sum(1 for r in results if r['risk_level'] == 'High')
        medium_count = sum(1 for r in results if r['risk_level'] == 'Medium')
        low_count = sum(1 for r in results if r['risk_level'] == 'Low')
        
        print(f"\n📈 Risk Distribution:")
        print(f"   High Risk: {high_count} patients")
        print(f"   Medium Risk: {medium_count} patients")
        print(f"   Low Risk: {low_count} patients")
        
        # Check for diversity
        unique_risk_scores = set(r['risk_score'] for r in results)
        print(f"\n🎯 Unique Risk Scores: {len(unique_risk_scores)} different values")
        
        if len(unique_risk_scores) > 5:
            print("✅ Great diversity in risk scores!")
        else:
            print("⚠️  Limited diversity in risk scores")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_dynamic_data()
