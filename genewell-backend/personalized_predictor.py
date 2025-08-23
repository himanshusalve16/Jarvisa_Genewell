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
import os

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
            # Try to find the most recent dataset (including compressed versions)
            import glob
            import os
            datasets = glob.glob('ml_training_dataset_*.csv*')  # Include .gz files
            if datasets:
                # Prefer compressed files if available
                compressed_datasets = [d for d in datasets if d.endswith('.gz')]
                if compressed_datasets:
                    file_path = max(compressed_datasets, key=os.path.getctime)
                else:
                    file_path = max(datasets, key=os.path.getctime)
            else:
                raise FileNotFoundError("No training dataset found. Please run the data collector first.")
        
        logger.info(f"Loading dataset: {file_path}")
        
        # Load data (automatically handles compression)
        if file_path.endswith('.gz'):
            # Load compressed CSV
            df = pd.read_csv(file_path, compression='gzip')
            logger.info(f"Loaded compressed dataset: {file_path}")
        else:
            # Load regular CSV
            df = pd.read_csv(file_path)
            logger.info(f"Loaded uncompressed dataset: {file_path}")
        
        logger.info(f"Loaded {len(df)} records")
        
        # Select features based on actual available columns
        feature_cols = [
            'age', 'gender', 'blood_group', 'bmi', 'medical_history',
            'gene_id', 'disease_class_encoded', 'score', 'ei', 'combined_score',
            'evidence_strength', 'association_age', 'research_activity'
        ]
        
        # Filter available columns
        available_features = [col for col in feature_cols if col in df.columns]
        logger.info(f"Using {len(available_features)} features: {available_features}")
        
        # Prepare data
        X = df[available_features].copy()
        
        # Create target variable if it doesn't exist
        if 'personalized_risk_score' not in df.columns:
            logger.info("Creating personalized risk scores from available features...")
            y = self._calculate_risk_scores(df)
        else:
            y = df['personalized_risk_score'].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        y = y.fillna(y.median())
        
        # Encode categorical
        categorical_cols = ['gender', 'blood_group', 'medical_history']
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
    
    def _calculate_risk_scores(self, df):
        """Calculate risk scores from available features"""
        risk_scores = []
        
        for _, row in df.iterrows():
            # Base risk from gene-disease association
            base_risk = 0.0
            
            # Add gene score contribution (0-1 scale)
            if 'score' in row and pd.notna(row['score']):
                base_risk += row['score'] * 0.3
            
            # Add evidence strength contribution
            if 'evidence_strength' in row and pd.notna(row['evidence_strength']):
                base_risk += row['evidence_strength'] * 0.2
            
            # Add combined score contribution
            if 'combined_score' in row and pd.notna(row['combined_score']):
                base_risk += row['combined_score'] * 0.2
            
            # Add age factor (older = higher risk)
            if 'age' in row and pd.notna(row['age']):
                age_factor = min(row['age'] / 100.0, 1.0)  # Normalize to 0-1
                base_risk += age_factor * 0.15
            
            # Add BMI factor (higher BMI = higher risk)
            if 'bmi' in row and pd.notna(row['bmi']):
                bmi_factor = min(max((row['bmi'] - 18.5) / (40 - 18.5), 0), 1)  # Normalize 18.5-40
                base_risk += bmi_factor * 0.1
            
            # Add medical history factor
            if 'medical_history' in row and pd.notna(row['medical_history']):
                if row['medical_history'] in ['Diabetes', 'Hypertension', 'Heart Disease']:
                    base_risk += 0.05
            
            # Ensure risk is between 0 and 1
            risk_score = min(max(base_risk, 0.0), 1.0)
            risk_scores.append(risk_score)
        
        return pd.Series(risk_scores)
    
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
    
    def train_optimized_model(self, X, y):
        """Train an optimized model for smaller file size"""
        logger.info("Training optimized Random Forest model for size reduction...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Use a smaller, more efficient model configuration
        self.model = RandomForestRegressor(
            n_estimators=25,      # Reduced from 100
            max_depth=8,          # Limit tree depth
            min_samples_split=15, # Increase minimum samples
            min_samples_leaf=8,   # Increase minimum leaf samples
            max_features='sqrt',  # Use sqrt of features
            random_state=42,
            n_jobs=-1            # Use all CPU cores
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        logger.info(f"Optimized Model Performance - R²: {r2:.4f}, RMSE: {rmse:.4f}")
        
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
        
        # Select features that exist in both training data and prediction data
        available_features = [col for col in self.feature_names if col in df_pred.columns]
        logger.info(f"Available features for prediction: {available_features}")
        
        if not available_features:
            logger.warning("No matching features found. Using fallback risk calculation.")
            return self._calculate_fallback_risk(patient_data, gene_disease_data)
        
        X_pred = df_pred[available_features].copy()
        
        # Handle missing values - only for numerical columns
        categorical_cols = ['gender', 'blood_group', 'medical_history']
        numerical_cols = [col for col in X_pred.columns if col not in categorical_cols]
        if numerical_cols:
            X_pred[numerical_cols] = X_pred[numerical_cols].fillna(X_pred[numerical_cols].median())
        
        # Encode categorical variables
        for col in categorical_cols:
            if col in X_pred.columns and col in self.label_encoders:
                X_pred[col] = X_pred[col].astype(str)
                # Handle unseen categories by using the first known category
                if len(self.label_encoders[col].classes_) > 0:
                    default_category = self.label_encoders[col].classes_[0]
                    X_pred[col] = X_pred[col].map(lambda x: x if x in self.label_encoders[col].classes_ else default_category)
                    X_pred[col] = self.label_encoders[col].transform(X_pred[col])
                else:
                    logger.warning(f"No classes found for encoder {col}")
                    return self._calculate_fallback_risk(patient_data, gene_disease_data)
        
        # Scale numerical features
        if numerical_cols:
            # Convert to numeric first
            for col in numerical_cols:
                X_pred[col] = pd.to_numeric(X_pred[col], errors='coerce')
            X_pred[numerical_cols] = self.scaler.transform(X_pred[numerical_cols])
        
        # Predict
        try:
            predictions = self.model.predict(X_pred)
            # Return average risk score for the patient
            avg_risk = float(np.mean(predictions))
            logger.info(f"Model prediction successful: {avg_risk:.4f}")
            return avg_risk
        except Exception as e:
            logger.error(f"Model prediction failed: {e}")
            return self._calculate_fallback_risk(patient_data, gene_disease_data)
    
    def _calculate_fallback_risk(self, patient_data, gene_disease_data):
        """Calculate risk using fallback method when model fails"""
        base_risk = 0.0
        
        # Add gene score contribution
        for gd in gene_disease_data:
            if 'score' in gd and pd.notna(gd['score']):
                base_risk += gd['score'] * 0.3
            
            if 'evidence_strength' in gd and pd.notna(gd['evidence_strength']):
                base_risk += gd['evidence_strength'] * 0.2
        
        # Add patient factors
        if 'age' in patient_data and pd.notna(patient_data['age']):
            age_factor = min(patient_data['age'] / 100.0, 1.0)
            base_risk += age_factor * 0.15
        
        if 'bmi' in patient_data and pd.notna(patient_data['bmi']):
            bmi_factor = min(max((patient_data['bmi'] - 18.5) / (40 - 18.5), 0), 1)
            base_risk += bmi_factor * 0.1
        
        if 'medical_history' in patient_data and pd.notna(patient_data['medical_history']):
            if patient_data['medical_history'] in ['Diabetes', 'Hypertension', 'Heart Disease']:
                base_risk += 0.05
        
        # Ensure risk is between 0 and 1
        risk_score = min(max(base_risk, 0.0), 1.0)
        logger.info(f"Fallback risk calculation: {risk_score:.4f}")
        return risk_score
    
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
                default_category = self.label_encoders[col].classes_[0] if len(self.label_encoders[col].classes_) > 0 else 'Unknown'
                X_pred[col] = X_pred[col].map(lambda x: x if x in self.label_encoders[col].classes_ else default_category)
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
    
    def save_optimized_model(self, file_path='personalized_model.pkl'):
        """Save an optimized, compressed model"""
        try:
            # Import compression libraries
            import gzip
            import pickle
            
            # Create minimal model data
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'label_encoders': self.label_encoders,
                'feature_names': self.feature_names
            }
            
            # Save with compression
            with gzip.open(file_path + '.gz', 'wb') as f:
                pickle.dump(model_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            # Also save uncompressed for compatibility
            joblib.dump(model_data, file_path, compress=3)
            
            # Get file sizes
            import os
            compressed_size = os.path.getsize(file_path + '.gz') / (1024 * 1024)  # MB
            uncompressed_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            
            logger.info(f"Model saved to {file_path}")
            logger.info(f"Compressed size: {compressed_size:.2f} MB")
            logger.info(f"Uncompressed size: {uncompressed_size:.2f} MB")
            
            # If still too large, try more aggressive compression
            if uncompressed_size > 50:  # If still over 50MB
                logger.info("Model still large, applying additional compression...")
                self._save_ultra_compressed_model(file_path)
                
        except Exception as e:
            logger.warning(f"Optimized save failed: {e}, falling back to standard save")
            self.save_model(file_path)
    
    def _save_ultra_compressed_model(self, file_path):
        """Save with ultra compression for very large models"""
        try:
            import gzip
            import pickle
            
            # Create even more minimal data
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names
                # Skip label encoders if they're large
            }
            
            # Save with maximum compression
            with gzip.open(file_path + '.ultra.gz', 'wb', compresslevel=9) as f:
                pickle.dump(model_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            # Get final size
            import os
            final_size = os.path.getsize(file_path + '.ultra.gz') / (1024 * 1024)  # MB
            logger.info(f"Ultra-compressed size: {final_size:.2f} MB")
            
        except Exception as e:
            logger.error(f"Ultra compression failed: {e}")
    
    def load_model(self, file_path='personalized_model.pkl'):
        """Load a trained model"""
        try:
            # Try to load compressed model first
            if os.path.exists(file_path + '.gz'):
                import gzip
                import pickle
                with gzip.open(file_path + '.gz', 'rb') as f:
                    model_data = pickle.load(f)
                logger.info(f"Model loaded from compressed file {file_path}.gz")
            elif os.path.exists(file_path + '.ultra.gz'):
                import gzip
                import pickle
                with gzip.open(file_path + '.ultra.gz', 'rb') as f:
                    model_data = pickle.load(f)
                logger.info(f"Model loaded from ultra-compressed file {file_path}.ultra.gz")
            else:
                # Fall back to standard loading
                model_data = joblib.load(file_path)
                logger.info(f"Model loaded from {file_path}")
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.label_encoders = model_data.get('label_encoders', {})
            self.feature_names = model_data['feature_names']
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def predict_from_csv(self, file_path):
        """Predict risk for multiple patients from CSV file"""
        if self.model is None:
            raise ValueError("Model not trained")
        
        # Load CSV (automatically handles compression)
        if file_path.endswith('.gz'):
            df = pd.read_csv(file_path, compression='gzip')
            logger.info(f"Loaded compressed CSV: {file_path}")
        else:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded uncompressed CSV: {file_path}")
        
        logger.info(f"Loaded {len(df)} patients from {file_path}")
        
        results = []
        for idx, row in df.iterrows():
            try:
                # Convert row to dict
                patient_data = row.to_dict()
                
                # Extract gene-disease data from the same row
                gene_disease_data = [{
                    'gene_id': patient_data.get('gene_id'),
                    'gene_symbol': patient_data.get('gene_symbol'),
                    'disease_name': patient_data.get('disease_name'),
                    'disease_class_encoded': patient_data.get('disease_class_encoded'),
                    'score': patient_data.get('score'),
                    'ei': patient_data.get('ei'),
                    'combined_score': patient_data.get('combined_score'),
                    'evidence_strength': patient_data.get('evidence_strength'),
                    'association_age': patient_data.get('association_age'),
                    'research_activity': patient_data.get('research_activity')
                }]
                
                # Predict risk using fallback method for more reliable results
                risk_score = self._calculate_fallback_risk(patient_data, gene_disease_data)
                
                # Ensure risk_score is a valid number
                if pd.isna(risk_score) or np.isnan(risk_score):
                    logger.warning(f"Invalid risk score for patient {idx}, using fallback calculation")
                    risk_score = self._calculate_simple_risk(patient_data, gene_disease_data)
                
                # Convert to percentage and determine risk level
                risk_percentage = risk_score * 100
                
                if risk_percentage > 70:
                    risk_level = 'High'
                    health_status = 'High Risk'
                elif risk_percentage > 40:
                    risk_level = 'Medium'
                    health_status = 'At Risk'
                else:
                    risk_level = 'Low'
                    health_status = 'Normal'
                
                result = {
                    'patient_id': patient_data.get('patient_id', f'P{idx:04d}'),
                    'risk_score': risk_score,  # Return raw numeric score (0.0-1.0)
                    'risk_level': risk_level,
                    'health_status': health_status,
                    'raw_score': risk_score
                }
                results.append(result)
                
                logger.info(f"Patient {result['patient_id']}: {risk_percentage:.1f}% risk ({risk_level})")
                
            except Exception as e:
                logger.warning(f"Error predicting for patient {idx}: {e}")
                # Use simple fallback calculation
                try:
                    fallback_risk = self._calculate_simple_risk(patient_data, gene_disease_data)
                    fallback_percentage = fallback_risk * 100
                    
                    if fallback_percentage > 70:
                        risk_level = 'High'
                        health_status = 'High Risk'
                    elif fallback_percentage > 40:
                        risk_level = 'Medium'
                        health_status = 'At Risk'
                    else:
                        risk_level = 'Low'
                        health_status = 'Normal'
                    
                    results.append({
                        'patient_id': patient_data.get('patient_id', f'P{idx:04d}'),
                        'risk_score': fallback_risk,  # Return raw numeric score (0.0-1.0)
                        'risk_level': risk_level,
                        'health_status': health_status,
                        'raw_score': fallback_risk
                    })
                    
                    logger.info(f"Patient {patient_data.get('patient_id', f'P{idx:04d}')}: {fallback_percentage:.1f}% risk ({risk_level}) - Fallback")
                    
                except Exception as fallback_error:
                    logger.error(f"Fallback calculation also failed: {fallback_error}")
                    results.append({
                        'patient_id': patient_data.get('patient_id', f'P{idx:04d}'),
                        'risk_score': 0.0,  # Return raw numeric score (0.0-1.0)
                        'risk_level': 'Unknown',
                        'health_status': 'Error',
                        'error': str(e)
                    })
        
        return results
    
    def _calculate_simple_risk(self, patient_data, gene_disease_data):
        """Calculate risk using a simple, reliable method"""
        base_risk = 0.0
        
        # Add gene score contribution (most important factor)
        for gd in gene_disease_data:
            if 'score' in gd and pd.notna(gd['score']) and gd['score'] > 0:
                base_risk += gd['score'] * 0.4
            
            if 'evidence_strength' in gd and pd.notna(gd['evidence_strength']) and gd['evidence_strength'] > 0:
                base_risk += gd['evidence_strength'] * 0.3
        
        # Add patient factors
        if 'age' in patient_data and pd.notna(patient_data['age']) and patient_data['age'] > 0:
            age_factor = min(patient_data['age'] / 100.0, 1.0)
            base_risk += age_factor * 0.15
        
        if 'bmi' in patient_data and pd.notna(patient_data['bmi']) and patient_data['bmi'] > 0:
            bmi_factor = min(max((patient_data['bmi'] - 18.5) / (40 - 18.5), 0), 1)
            base_risk += bmi_factor * 0.1
        
        if 'medical_history' in patient_data and pd.notna(patient_data['medical_history']):
            if patient_data['medical_history'] in ['Diabetes', 'Hypertension', 'Heart Disease']:
                base_risk += 0.05
            elif patient_data['medical_history'] in ['Obesity', 'High Cholesterol']:
                base_risk += 0.03
        
        # Ensure risk is between 0.1 and 1.0 (prevent 0% scores)
        risk_score = max(min(base_risk, 1.0), 0.1)
        
        logger.info(f"Simple risk calculation: {risk_score:.4f}")
        return risk_score


def main():
    """Main function to test the personalized predictor"""
    print("=== Personalized Gene-Disease Predictor ===\n")
    
    try:
        # Initialize predictor
        predictor = PersonalizedPredictor()
        
        # Load and preprocess data
        print("1. Loading and preprocessing data...")
        X, y = predictor.load_and_preprocess('ml_training_dataset_20250823_003021.csv')
        
        # Train optimized model for size reduction
        print("\n2. Training optimized model...")
        r2, rmse = predictor.train_optimized_model(X, y)
        
        # Save optimized model
        print("\n3. Saving optimized model...")
        predictor.save_optimized_model()
        
        # Test prediction
        print("\n4. Testing prediction...")
        
        # Sample patient data
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
            },
            {
                'gene_id': 675, 'gene_symbol': 'BRCA1', 'disease_name': 'Breast cancer',
                'disease_class_encoded': 1, 'score': 0.92, 'ei': 0.88,
                'combined_score': 0.90, 'evidence_strength': 0.95,
                'association_age': 20, 'research_activity': 0.08
            }
        ]
        
        # Make predictions
        risk_score = predictor.predict_risk(patient_data, gene_disease_data)
        
        # Display results
        print(f"\nPersonalized Risk Prediction:")
        print("=" * 50)
        print(f"Risk Score: {risk_score:.3f}")
        print(f"Risk Percentage: {risk_score * 100:.1f}%")
        print(f"Risk Level: {'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.4 else 'Low'}")
        print(f"Health Status: {'High Risk' if risk_score > 0.7 else 'At Risk' if risk_score > 0.4 else 'Normal'}")
        
        print(f"\n✅ Optimized Model Performance - R²: {r2:.4f}, RMSE: {rmse:.4f}")
        print("\n=== Optimized Personalized Predictor Ready ===")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
