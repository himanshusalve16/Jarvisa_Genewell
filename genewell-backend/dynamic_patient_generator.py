#!/usr/bin/env python3
"""
Dynamic Patient Data Generator
=============================

Generates diverse patient data with different risk profiles for testing
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
import os

class DynamicPatientGenerator:
    def __init__(self):
        self.gene_diseases = [
            {'gene_id': 7157, 'gene_symbol': 'TP53', 'disease_name': 'Breast Cancer', 'base_risk': 0.85},
            {'gene_id': 675, 'gene_symbol': 'BRCA1', 'disease_name': 'Ovarian Cancer', 'base_risk': 0.92},
            {'gene_id': 5888, 'gene_symbol': 'BRCA2', 'disease_name': 'Prostate Cancer', 'base_risk': 0.78},
            {'gene_id': 2064, 'gene_symbol': 'ERBB2', 'disease_name': 'Lung Cancer', 'base_risk': 0.72},
            {'gene_id': 1026, 'gene_symbol': 'CDKN2A', 'disease_name': 'Melanoma', 'base_risk': 0.68},
            {'gene_id': 3845, 'gene_symbol': 'KRAS', 'disease_name': 'Colon Cancer', 'base_risk': 0.75},
            {'gene_id': 1956, 'gene_symbol': 'EGFR', 'disease_name': 'Brain Cancer', 'base_risk': 0.70},
            {'gene_id': 7157, 'gene_symbol': 'TP53', 'disease_name': 'Liver Cancer', 'base_risk': 0.65},
            {'gene_id': 675, 'gene_symbol': 'BRCA1', 'disease_name': 'Pancreatic Cancer', 'base_risk': 0.80},
            {'gene_id': 5888, 'gene_symbol': 'BRCA2', 'disease_name': 'Stomach Cancer', 'base_risk': 0.73}
        ]
        
        self.medical_conditions = [
            'None', 'Diabetes', 'Hypertension', 'Heart Disease', 'Asthma', 
            'Obesity', 'High Cholesterol', 'Arthritis', 'Depression', 'Anxiety'
        ]
        
        self.blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        self.genders = ['Male', 'Female']
        
    def generate_patient_data(self, num_patients=10):
        """Generate diverse patient data with different risk profiles"""
        patients = []
        
        for i in range(num_patients):
            # Generate diverse patient characteristics
            age = random.randint(25, 75)
            gender = random.choice(self.genders)
            blood_group = random.choice(self.blood_groups)
            bmi = round(random.uniform(18.5, 40.0), 1)
            medical_history = random.choice(self.medical_conditions)
            
            # Select random gene-disease combination
            gene_disease = random.choice(self.gene_diseases)
            
            # Generate varied scores based on patient characteristics
            base_score = gene_disease['base_risk']
            
            # Add age factor (older = higher risk)
            age_factor = min(age / 100.0, 1.0)
            
            # Add BMI factor (higher BMI = higher risk)
            bmi_factor = min(max((bmi - 18.5) / (40 - 18.5), 0), 1)
            
            # Add medical history factor
            medical_factor = 0.0
            if medical_history in ['Diabetes', 'Hypertension', 'Heart Disease']:
                medical_factor = random.uniform(0.05, 0.15)
            elif medical_history in ['Obesity', 'High Cholesterol']:
                medical_factor = random.uniform(0.03, 0.10)
            
            # Calculate final scores with some randomness
            score = min(max(base_score + random.uniform(-0.1, 0.1), 0.1), 1.0)
            evidence_strength = min(max(base_score + random.uniform(-0.15, 0.15), 0.2), 1.0)
            combined_score = min(max((score + evidence_strength) / 2 + random.uniform(-0.1, 0.1), 0.1), 1.0)
            
            # Generate other features
            ei = random.uniform(0.5, 0.95)
            association_age = random.randint(5, 25)
            research_activity = random.uniform(0.01, 0.15)
            disease_class_encoded = random.randint(1, 5)
            
            patient = {
                'patient_id': f'P{i:04d}',
                'age': age,
                'gender': gender,
                'blood_group': blood_group,
                'bmi': bmi,
                'medical_history': medical_history,
                'gene_id': gene_disease['gene_id'],
                'gene_symbol': gene_disease['gene_symbol'],
                'disease_name': gene_disease['disease_name'],
                'disease_class_encoded': disease_class_encoded,
                'score': round(score, 3),
                'ei': round(ei, 3),
                'combined_score': round(combined_score, 3),
                'evidence_strength': round(evidence_strength, 3),
                'association_age': association_age,
                'research_activity': round(research_activity, 4)
            }
            
            patients.append(patient)
        
        return patients
    
    def generate_high_risk_patients(self, num_patients=5):
        """Generate patients with high risk profiles"""
        patients = []
        
        for i in range(num_patients):
            # High risk characteristics
            age = random.randint(60, 75)
            gender = random.choice(self.genders)
            blood_group = random.choice(self.blood_groups)
            bmi = round(random.uniform(30.0, 40.0), 1)  # High BMI
            medical_history = random.choice(['Diabetes', 'Hypertension', 'Heart Disease', 'Obesity'])
            
            # High-risk gene-disease combinations
            gene_disease = random.choice(self.gene_diseases[:5])  # Top 5 high-risk genes
            
            # High scores
            score = random.uniform(0.8, 1.0)
            evidence_strength = random.uniform(0.8, 1.0)
            combined_score = random.uniform(0.8, 1.0)
            
            patient = {
                'patient_id': f'H{i:04d}',
                'age': age,
                'gender': gender,
                'blood_group': blood_group,
                'bmi': bmi,
                'medical_history': medical_history,
                'gene_id': gene_disease['gene_id'],
                'gene_symbol': gene_disease['gene_symbol'],
                'disease_name': gene_disease['disease_name'],
                'disease_class_encoded': random.randint(1, 3),
                'score': round(score, 3),
                'ei': round(random.uniform(0.7, 0.95), 3),
                'combined_score': round(combined_score, 3),
                'evidence_strength': round(evidence_strength, 3),
                'association_age': random.randint(10, 20),
                'research_activity': round(random.uniform(0.05, 0.15), 4)
            }
            
            patients.append(patient)
        
        return patients
    
    def generate_medium_risk_patients(self, num_patients=5):
        """Generate patients with medium risk profiles"""
        patients = []
        
        for i in range(num_patients):
            # Medium risk characteristics
            age = random.randint(40, 60)
            gender = random.choice(self.genders)
            blood_group = random.choice(self.blood_groups)
            bmi = round(random.uniform(25.0, 30.0), 1)  # Moderate BMI
            medical_history = random.choice(['None', 'High Cholesterol', 'Asthma', 'Arthritis'])
            
            # Medium-risk gene-disease combinations
            gene_disease = random.choice(self.gene_diseases[3:7])  # Medium-risk genes
            
            # Medium scores
            score = random.uniform(0.5, 0.8)
            evidence_strength = random.uniform(0.5, 0.8)
            combined_score = random.uniform(0.5, 0.8)
            
            patient = {
                'patient_id': f'M{i:04d}',
                'age': age,
                'gender': gender,
                'blood_group': blood_group,
                'bmi': bmi,
                'medical_history': medical_history,
                'gene_id': gene_disease['gene_id'],
                'gene_symbol': gene_disease['gene_symbol'],
                'disease_name': gene_disease['disease_name'],
                'disease_class_encoded': random.randint(2, 4),
                'score': round(score, 3),
                'ei': round(random.uniform(0.5, 0.8), 3),
                'combined_score': round(combined_score, 3),
                'evidence_strength': round(evidence_strength, 3),
                'association_age': random.randint(15, 25),
                'research_activity': round(random.uniform(0.02, 0.08), 4)
            }
            
            patients.append(patient)
    
        return patients
    
    def generate_low_risk_patients(self, num_patients=5):
        """Generate patients with low risk profiles"""
        patients = []
        
        for i in range(num_patients):
            # Low risk characteristics
            age = random.randint(25, 40)
            gender = random.choice(self.genders)
            blood_group = random.choice(self.blood_groups)
            bmi = round(random.uniform(18.5, 25.0), 1)  # Normal BMI
            medical_history = 'None'
            
            # Low-risk gene-disease combinations
            gene_disease = random.choice(self.gene_diseases[5:])  # Lower-risk genes
            
            # Low scores
            score = random.uniform(0.2, 0.5)
            evidence_strength = random.uniform(0.2, 0.5)
            combined_score = random.uniform(0.2, 0.5)
            
            patient = {
                'patient_id': f'L{i:04d}',
                'age': age,
                'gender': gender,
                'blood_group': blood_group,
                'bmi': bmi,
                'medical_history': medical_history,
                'gene_id': gene_disease['gene_id'],
                'gene_symbol': gene_disease['gene_symbol'],
                'disease_name': gene_disease['disease_name'],
                'disease_class_encoded': random.randint(3, 5),
                'score': round(score, 3),
                'ei': round(random.uniform(0.3, 0.6), 3),
                'combined_score': round(combined_score, 3),
                'evidence_strength': round(evidence_strength, 3),
                'association_age': random.randint(20, 30),
                'research_activity': round(random.uniform(0.01, 0.05), 4)
            }
            
            patients.append(patient)
        
        return patients
    
    def generate_diverse_sample_data(self, total_patients=20):
        """Generate a diverse mix of patients with different risk levels"""
        # Generate different risk level patients
        high_risk = self.generate_high_risk_patients(7)
        medium_risk = self.generate_medium_risk_patients(7)
        low_risk = self.generate_low_risk_patients(6)
        
        # Combine all patients
        all_patients = high_risk + medium_risk + low_risk
        
        # Shuffle to mix risk levels
        random.shuffle(all_patients)
        
        return all_patients
    
    def save_sample_data(self, patients, filename=None):
        """Save patient data to CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'dynamic_sample_data_{timestamp}.csv'
        
        df = pd.DataFrame(patients)
        
        # Create uploads directory if it doesn't exist
        os.makedirs('uploads', exist_ok=True)
        
        filepath = os.path.join('uploads', filename)
        df.to_csv(filepath, index=False)
        
        print(f"✅ Generated {len(patients)} diverse patients")
        print(f"📁 Saved to: {filepath}")
        
        # Show risk distribution
        risk_levels = []
        for patient in patients:
            score = patient['score']
            if score > 0.7:
                risk_levels.append('High')
            elif score > 0.4:
                risk_levels.append('Medium')
            else:
                risk_levels.append('Low')
        
        print(f"\n📊 Risk Distribution:")
        print(f"   High Risk: {risk_levels.count('High')} patients")
        print(f"   Medium Risk: {risk_levels.count('Medium')} patients")
        print(f"   Low Risk: {risk_levels.count('Low')} patients")
        
        return filepath
    
    def generate_fresh_sample(self, num_patients=20):
        """Generate a fresh sample data file with timestamp"""
        patients = self.generate_diverse_sample_data(num_patients)
        return self.save_sample_data(patients)


def main():
    """Main function to test the patient generator"""
    print("=== Dynamic Patient Data Generator ===\n")
    
    generator = DynamicPatientGenerator()
    
    # Generate diverse sample data
    print("🔄 Generating diverse patient data...")
    sample_file = generator.generate_fresh_sample(25)
    
    print(f"\n🎯 Sample data ready for testing!")
    print(f"📁 File: {sample_file}")
    print(f"💡 Upload this file to test different risk scores and health statuses")


if __name__ == "__main__":
    main()
