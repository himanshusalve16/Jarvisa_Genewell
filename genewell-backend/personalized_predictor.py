#!/usr/bin/env python3
"""
Personalized Gene-Disease Predictor
==================================

Simplified ML pipeline for personalized gene-disease prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonalizedPredictor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.model = None
        self.feature_names = None
        
    def load_and_preprocess(self, file_path: str = None):
        """Load and preprocess the ML training dataset"""
        if file_path is None:
            # Try to find the most recent dataset
            import glob
            import os
            datasets = glob.glob('ml_training_dataset_*.csv')
            if datasets:
                file_path = max(datasets, key=os.path.getctime)
            else:
                raise FileNotFoundError("No training dataset found. Please run the data collector first.")
        
        logger.info(f"Loading dataset: {file_path}")
        
        # Load data
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} records")
        
        # Select features
        feature_cols = [
            'age', 'gender', 'blood_group', 'bmi', 'systolic_bp', 'diastolic_bp',
            'gene_id', 'disease_class_encoded', 'score', 'ei', 'combined_score',
            'evidence_strength', 'association_age', 'research_activity',
            'age_factor', 'gender_factor', 'medical_factor', 'family_factor',
            'lifestyle_factor', 'bmi_factor'
        ]
        
        # Filter available columns
        available_features = [col for col in feature_cols if col in df.columns]
        logger.info(f"Using {len(available_features)} features")
        
        # Prepare data
        X = df[available_features].copy()
        y = df['personalized_risk_score'].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        y = y.fillna(y.median())
        
        # Encode categorical
        categorical_cols = ['gender', 'blood_group']
        for col in categorical_cols:
            if col in X.columns:
                le = LabelEncoder()
                X[col] = X[col].astype(str)
                X[col] = le.fit_transform(X[col])
                self.label_encoders[col] = le
        
        # Scale numerical
        numerical_cols = [col for col in X.columns if col not in categorical_cols]
        X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])
        
        self.feature_names = X.columns.tolist()
        
        return X, y
    
    def train_model(self, X, y):
        """Train the prediction model"""
        logger.info("Training Random Forest model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        logger.info(f"Model Performance - R²: {r2:.4f}, RMSE: {rmse:.4f}")
        
        return r2, rmse
    
    def predict_risk(self, patient_data, gene_disease_data=None):
        """Predict personalized risk for a patient"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        # If gene_disease_data is not provided, use default sample data
        if gene_disease_data is None:
            gene_disease_data = [
                {
                    'gene_id': 7157, 'gene_symbol': 'TP53', 'disease_name': 'Breast cancer',
                    'disease_class_encoded': 1, 'score': 0.85, 'ei': 0.78,
                    'combined_score': 0.82, 'evidence_strength': 0.9,
                    'association_age': 15, 'research_activity': 0.06
                },
                {
                    'gene_id': 675, 'gene_symbol': 'BRCA1', 'disease_name': 'Breast cancer',
                    'disease_class_encoded': 1, 'score': 0.92, 'ei': 0.88,
                    'combined_score': 0.90, 'evidence_strength': 0.95,
                    'association_age': 20, 'research_activity': 0.08
                }
            ]
        
        # Prepare prediction data
        records = []
        for gd in gene_disease_data:
            record = {**patient_data, **gd}
            records.append(record)
        
        df_pred = pd.DataFrame(records)
        
        # Select features
        available_features = [col for col in self.feature_names if col in df_pred.columns]
        X_pred = df_pred[available_features].copy()
        
        # Handle missing values - only for numerical columns
        numerical_cols = [col for col in X_pred.columns if col not in ['gender', 'blood_group']]
        if numerical_cols:
            X_pred[numerical_cols] = X_pred[numerical_cols].fillna(X_pred[numerical_cols].median())
        
        # Encode categorical (only gender and blood_group)
        categorical_cols = ['gender', 'blood_group']
        for col in categorical_cols:
            if col in X_pred.columns and col in self.label_encoders:
                X_pred[col] = X_pred[col].astype(str)
                # Handle unseen categories by using the first known category
                X_pred[col] = X_pred[col].map(lambda x: x if x in self.label_encoders[col].classes_ else self.label_encoders[col].classes_[0])
                X_pred[col] = self.label_encoders[col].transform(X_pred[col])
        
        # Scale numerical (all other columns)
        numerical_cols = [col for col in X_pred.columns if col not in categorical_cols]
        if numerical_cols:
            # Convert to numeric first
            for col in numerical_cols:
                X_pred[col] = pd.to_numeric(X_pred[col], errors='coerce')
            X_pred[numerical_cols] = self.scaler.transform(X_pred[numerical_cols])
        
        # Predict
        predictions = self.model.predict(X_pred)
        
        # Return average risk score for the patient
        avg_risk = float(np.mean(predictions))
        
        return avg_risk
    
    def predict_detailed_risk(self, patient_data, gene_disease_data):
        """Predict detailed risk breakdown for a patient"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        # Prepare prediction data
        records = []
        for gd in gene_disease_data:
            record = {**patient_data, **gd}
            records.append(record)
        
        df_pred = pd.DataFrame(records)
        
        # Select features
        available_features = [col for col in self.feature_names if col in df_pred.columns]
        X_pred = df_pred[available_features].copy()
        
        # Handle missing values - only for numerical columns
        numerical_cols = [col for col in X_pred.columns if col not in ['gender', 'blood_group']]
        if numerical_cols:
            X_pred[numerical_cols] = X_pred[numerical_cols].fillna(X_pred[numerical_cols].median())
        
        # Encode categorical (only gender and blood_group)
        categorical_cols = ['gender', 'blood_group']
        for col in categorical_cols:
            if col in X_pred.columns and col in self.label_encoders:
                X_pred[col] = X_pred[col].astype(str)
                # Handle unseen categories by using the first known category
                X_pred[col] = X_pred[col].map(lambda x: x if x in self.label_encoders[col].classes_ else self.label_encoders[col].classes_[0])
                X_pred[col] = self.label_encoders[col].transform(X_pred[col])
        
        # Scale numerical (all other columns)
        numerical_cols = [col for col in X_pred.columns if col not in categorical_cols]
        if numerical_cols:
            # Convert to numeric first
            for col in numerical_cols:
                X_pred[col] = pd.to_numeric(X_pred[col], errors='coerce')
            X_pred[numerical_cols] = self.scaler.transform(X_pred[numerical_cols])
        
        # Predict
        predictions = self.model.predict(X_pred)
        
        # Format results
        results = []
        for i, (pred, record) in enumerate(zip(predictions, records)):
            result = {
                'gene_symbol': record.get('gene_symbol', 'Unknown'),
                'disease_name': record.get('disease_name', 'Unknown'),
                'predicted_risk': float(pred),
                'risk_category': 'High' if pred > 0.7 else 'Medium' if pred > 0.4 else 'Low',
                'health_status': 'High Risk' if pred > 0.7 else 'At Risk' if pred > 0.4 else 'Normal'
            }
            results.append(result)
        
        return sorted(results, key=lambda x: x['predicted_risk'], reverse=True)
    
    def save_model(self, file_path='personalized_model.pkl'):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names
        }
        joblib.dump(model_data, file_path)
        logger.info(f"Model saved to {file_path}")
    
    def load_model(self, file_path='personalized_model.pkl'):
        """Load a trained model"""
        model_data = joblib.load(file_path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoders = model_data['label_encoders']
        self.feature_names = model_data['feature_names']
        logger.info(f"Model loaded from {file_path}")
    
    def predict_from_csv(self, file_path):
        """Predict risk for multiple patients from CSV file"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        # Load CSV
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} patients from {file_path}")
        
        results = []
        for idx, row in df.iterrows():
            try:
                # Convert row to dict
                patient_data = row.to_dict()
                
                # Predict risk
                risk_score = self.predict_risk(patient_data)
                
                result = {
                    'patient_id': patient_data.get('patient_id', f'P{idx:04d}'),
                    'risk_score': risk_score,
                    'risk_level': 'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low',
                    'health_status': 'High Risk' if risk_score > 0.7 else 'At Risk' if risk_score > 0.4 else 'Normal'
                }
                results.append(result)
                
            except Exception as e:
                logger.warning(f"Error predicting for patient {idx}: {e}")
                results.append({
                    'patient_id': patient_data.get('patient_id', f'P{idx:04d}'),
                    'risk_score': 0.0,
                    'risk_level': 'Unknown',
                    'health_status': 'Error',
                    'error': str(e)
                })
        
        return results


def main():
    """Main function to test the personalized predictor"""
    print("=== Personalized Gene-Disease Predictor ===\n")
    
    try:
        # Initialize predictor
        predictor = PersonalizedPredictor()
        
        # Load and preprocess data
        print("1. Loading and preprocessing data...")
        X, y = predictor.load_and_preprocess('ml_training_dataset_20250823_003021.csv')
        
        # Train model
        print("\n2. Training model...")
        r2, rmse = predictor.train_model(X, y)
        
        # Save model
        print("\n3. Saving model...")
        predictor.save_model()
        
        # Test prediction
        print("\n4. Testing prediction...")
        
        # Sample patient data
        patient_data = {
            'age': 45, 'gender': 'Female', 'blood_group': 'A+', 'bmi': 26.5,
            'systolic_bp': 125, 'diastolic_bp': 82, 'age_factor': 1.1,
            'gender_factor': 1.0, 'medical_factor': 1.6, 'family_factor': 1.3,
            'lifestyle_factor': 0.9, 'bmi_factor': 1.0
        }
        
        # Sample gene-disease data
        gene_disease_data = [
            {
                'gene_id': 7157, 'gene_symbol': 'TP53', 'disease_name': 'Breast cancer',
                'disease_class_encoded': 1, 'score': 0.85, 'ei': 0.78,
                'combined_score': 0.82, 'evidence_strength': 0.9,
                'association_age': 15, 'research_activity': 0.06
            },
            {
                'gene_id': 675, 'gene_symbol': 'BRCA1', 'disease_name': 'Breast cancer',
                'disease_class_encoded': 1, 'score': 0.92, 'ei': 0.88,
                'combined_score': 0.90, 'evidence_strength': 0.95,
                'association_age': 20, 'research_activity': 0.0475
            }
        ]
        
        # Make predictions
        results = predictor.predict_risk(patient_data, gene_disease_data)
        
        # Display results
        print(f"\nPersonalized Risk Predictions:")
        print("=" * 50)
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['gene_symbol']} → {result['disease_name']}")
            print(f"   Risk Score: {result['predicted_risk']:.3f}")
            print(f"   Category: {result['risk_category']}")
            print(f"   Status: {result['health_status']}")
        
        print(f"\n✅ Model Performance - R²: {r2:.4f}, RMSE: {rmse:.4f}")
        print("\n=== Personalized Predictor Ready ===")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
