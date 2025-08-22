#!/usr/bin/env python3
"""
Personalized Gene-Disease Data Collector
========================================

This script generates comprehensive datasets for personalized gene-disease prediction
by combining gene-disease associations with patient-specific features.

Features:
- Patient metadata (age, gender, medical history, etc.)
- Gene-disease associations with scores
- Personalized risk factors
- ML-ready features for prediction
- Multiple data formats for different use cases

Author: GeneWell ML Team
"""

import pandas as pd
import numpy as np
import json
import logging
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import os
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('personalized_gene_disease_collector.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PersonalizedGeneDiseaseCollector:
    """
    Comprehensive collector for personalized gene-disease prediction data
    """
    
    def __init__(self):
        """Initialize the personalized data collector"""
        self.gene_disease_associations = self._load_gene_disease_associations()
        logger.info("Personalized Gene-Disease Collector initialized")
    
    def _load_gene_disease_associations(self) -> pd.DataFrame:
        """
        Load existing gene-disease associations or generate synthetic ones
        """
        try:
            # Try to load existing associations
            if os.path.exists('gene_disease_ml_dataset.csv'):
                df = pd.read_csv('gene_disease_ml_dataset.csv')
                logger.info(f"Loaded {len(df)} existing gene-disease associations")
                return df
        except Exception as e:
            logger.warning(f"Could not load existing associations: {e}")
        
        # Generate synthetic associations if none exist
        logger.info("Generating synthetic gene-disease associations...")
        return self._generate_synthetic_associations()
    
    def _generate_synthetic_associations(self, n_associations: int = 1000) -> pd.DataFrame:
        """
        Generate synthetic gene-disease associations
        """
        # Common genes and their symbols
        genes = [
            ('7157', 'TP53', 'Tumor protein p53'),
            ('675', 'BRCA2', 'BRCA2 DNA repair associated'),
            ('675', 'BRCA1', 'BRCA1 DNA repair associated'),
            ('4609', 'MYC', 'MYC proto-oncogene'),
            ('3845', 'KRAS', 'KRAS proto-oncogene'),
            ('207', 'AKT1', 'AKT serine/threonine kinase 1'),
            ('5728', 'PTEN', 'Phosphatase and tensin homolog'),
            ('7157', 'PIK3CA', 'Phosphatidylinositol-4,5-bisphosphate 3-kinase catalytic subunit alpha'),
            ('7157', 'APC', 'APC regulator of WNT signaling pathway'),
            ('7157', 'VHL', 'Von Hippel-Lindau tumor suppressor'),
            ('7157', 'RB1', 'RB transcriptional corepressor 1'),
            ('7157', 'CDKN2A', 'Cyclin dependent kinase inhibitor 2A'),
            ('7157', 'SMAD4', 'SMAD family member 4'),
            ('7157', 'NOTCH1', 'Notch receptor 1'),
            ('7157', 'JAK2', 'Janus kinase 2'),
            ('7157', 'FLT3', 'Fms related receptor tyrosine kinase 3'),
            ('7157', 'IDH1', 'Isocitrate dehydrogenase 1'),
            ('7157', 'BRAF', 'B-Raf proto-oncogene'),
            ('7157', 'EGFR', 'Epidermal growth factor receptor'),
            ('7157', 'ALK', 'ALK receptor tyrosine kinase'),
            ('7157', 'ROS1', 'ROS proto-oncogene 1'),
            ('7157', 'MET', 'MET proto-oncogene'),
            ('7157', 'CFTR', 'Cystic fibrosis transmembrane conductance regulator'),
            ('7157', 'HBB', 'Hemoglobin subunit beta'),
            ('7157', 'F8', 'Coagulation factor VIII'),
            ('7157', 'F9', 'Coagulation factor IX'),
            ('7157', 'APP', 'Amyloid beta precursor protein'),
            ('7157', 'PSEN1', 'Presenilin 1'),
            ('7157', 'PSEN2', 'Presenilin 2'),
            ('7157', 'APOE', 'Apolipoprotein E'),
            ('7157', 'INS', 'Insulin'),
            ('7157', 'GCK', 'Glucokinase'),
            ('7157', 'HNF1A', 'HNF1 homeobox A'),
            ('7157', 'HNF4A', 'HNF4 homeobox A'),
            ('7157', 'PPARG', 'Peroxisome proliferator activated receptor gamma'),
            ('7157', 'KCNJ11', 'Potassium inwardly rectifying channel subfamily J member 11'),
            ('7157', 'ABCC8', 'ATP binding cassette subfamily C member 8')
        ]
        
        # Common diseases
        diseases = [
            ('C0006826', 'Cancer', 'Disease', 'Neoplasms'),
            ('C0011849', 'Diabetes mellitus', 'Disease', 'Endocrine diseases'),
            ('C0022658', 'Hypertension', 'Disease', 'Cardiovascular diseases'),
            ('C0002395', 'Alzheimer disease', 'Disease', 'Nervous system diseases'),
            ('C0019069', 'Hemophilia', 'Disease', 'Blood diseases'),
            ('C0010674', 'Cystic fibrosis', 'Disease', 'Respiratory diseases'),
            ('C0002895', 'Sickle cell anemia', 'Disease', 'Blood diseases'),
            ('C0004096', 'Asthma', 'Disease', 'Respiratory diseases'),
            ('C0003864', 'Arthritis', 'Disease', 'Musculoskeletal diseases'),
            ('C0002962', 'Atherosclerosis', 'Disease', 'Cardiovascular diseases'),
            ('C0004153', 'Breast cancer', 'Disease', 'Neoplasms'),
            ('C0007134', 'Lung cancer', 'Disease', 'Neoplasms'),
            ('C0007102', 'Colon cancer', 'Disease', 'Neoplasms'),
            ('C0006142', 'Prostate cancer', 'Disease', 'Neoplasms'),
            ('C0003873', 'Rheumatoid arthritis', 'Disease', 'Musculoskeletal diseases'),
            ('C0004096', 'Type 1 diabetes', 'Disease', 'Endocrine diseases'),
            ('C0011849', 'Type 2 diabetes', 'Disease', 'Endocrine diseases'),
            ('C0002395', 'Parkinson disease', 'Disease', 'Nervous system diseases'),
            ('C0002395', 'Multiple sclerosis', 'Disease', 'Nervous system diseases')
        ]
        
        associations = []
        
        for i in range(n_associations):
            # Randomly select gene and disease
            gene = random.choice(genes)
            disease = random.choice(diseases)
            
            # Generate realistic scores and evidence
            score = np.random.beta(2, 5)  # Skewed towards lower scores
            if random.random() < 0.2:  # 20% high-quality associations
                score = np.random.uniform(0.7, 1.0)
            
            nofpmids = int(np.random.exponential(3)) + 1  # Exponential distribution
            if score > 0.7:
                nofpmids = max(nofpmids, 5)  # High scores have more evidence
            
            # Generate years
            year_initial = random.randint(1990, 2020)
            year_final = random.randint(year_initial, 2024)
            
            association = {
                'gene_id': gene[0],
                'gene_symbol': gene[1],
                'gene_name': gene[2],
                'disease_id': disease[0],
                'disease_name': disease[1],
                'disease_type': disease[2],
                'disease_class': disease[3],
                'score': round(score, 3),
                'ei': round(score * 0.8 + random.uniform(0, 0.2), 3),
                'year_initial': year_initial,
                'year_final': year_final,
                'source': 'Synthetic',
                'pmid': f"PMID{random.randint(1000000, 9999999)}",
                'nofpmids': nofpmids,
                'nofsnps': random.randint(0, 50),
                'association_type': random.choice(['Genetic', 'Biochemical', 'Expression', 'Pathway']),
                'status': random.choice(['Validated', 'Predicted', 'Literature']),
                'created_date': datetime.now().isoformat(),
                'updated_date': datetime.now().isoformat()
            }
            
            associations.append(association)
        
        df = pd.DataFrame(associations)
        
        # Add ML features
        df = self._add_ml_features(df)
        
        return df
    
    def _add_ml_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add ML features to the dataset"""
        df_ml = df.copy()
        
        # Feature 1: Evidence strength (normalized)
        df_ml['evidence_strength'] = df_ml['nofpmids'] / df_ml['nofpmids'].max()
        
        # Feature 2: Score category
        df_ml['score_category'] = pd.cut(
            df_ml['score'], 
            bins=[0, 0.3, 0.5, 0.7, 1.0], 
            labels=['Low', 'Medium', 'High', 'Very High']
        )
        
        # Feature 3: Association age
        current_year = datetime.now().year
        df_ml['association_age'] = current_year - df_ml['year_initial']
        
        # Feature 4: Research activity
        df_ml['research_activity'] = df_ml['nofpmids'] / (df_ml['association_age'] + 1)
        
        # Feature 5: Combined score
        df_ml['combined_score'] = (
            df_ml['score'] * 0.6 + 
            df_ml['evidence_strength'] * 0.3 + 
            (df_ml['research_activity'] / df_ml['research_activity'].max()) * 0.1
        )
        
        # Feature 6: Disease class encoding
        disease_class_encoding = {
            'Disease': 1,
            'Phenotype': 2,
            'Sign or Symptom': 3,
            'Finding': 4,
            'Neoplasms': 1,
            'Endocrine diseases': 2,
            'Cardiovascular diseases': 3,
            'Nervous system diseases': 4,
            'Blood diseases': 5,
            'Respiratory diseases': 6,
            'Musculoskeletal diseases': 7
        }
        df_ml['disease_class_encoded'] = df_ml['disease_class'].map(disease_class_encoding).fillna(1)
        
        return df_ml
    
    def generate_personalized_dataset(self, 
                                    n_patients: int = 5000,
                                    output_file: str = None) -> str:
        """
        Generate personalized gene-disease prediction dataset
        
        Args:
            n_patients (int): Number of patients to generate
            output_file (str): Output filename
            
        Returns:
            str: Path to generated CSV file
        """
        logger.info(f"Generating personalized dataset with {n_patients} patients...")
        
        personalized_data = []
        
        for patient_id in range(n_patients):
            # Generate patient metadata
            patient_metadata = self._generate_patient_metadata(patient_id)
            
            # Select relevant gene-disease associations for this patient
            patient_associations = self._select_patient_associations(patient_metadata)
            
            # Create personalized records
            for _, association in patient_associations.iterrows():
                personalized_record = {
                    'patient_id': f'P{patient_id:04d}',
                    **patient_metadata,
                    **association.to_dict()
                }
                
                # Add personalized risk factors
                personalized_record.update(
                    self._calculate_personalized_risk_factors(patient_metadata, association)
                )
                
                personalized_data.append(personalized_record)
        
        # Convert to DataFrame
        df = pd.DataFrame(personalized_data)
        
        # Save to CSV
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"personalized_gene_disease_dataset_{timestamp}.csv"
        
        if not output_file.endswith('.csv'):
            output_file += '.csv'
        
        df.to_csv(output_file, index=False, encoding='utf-8')
        
        logger.info(f"Personalized dataset saved to: {output_file}")
        logger.info(f"Generated {len(df)} personalized records for {n_patients} patients")
        
        # Generate summary
        self._generate_personalized_summary(df, output_file)
        
        return output_file
    
    def _generate_patient_metadata(self, patient_id: int) -> Dict:
        """Generate realistic patient metadata"""
        # Age distribution (more realistic)
        age = int(np.random.normal(45, 15))  # Mean 45, std 15
        age = max(18, min(90, age))  # Clamp between 18-90
        
        # Gender
        gender = random.choice(['Male', 'Female'])
        
        # Blood group
        blood_group = random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
        
        # Medical history (realistic combinations)
        medical_conditions = []
        
        # Age-related conditions
        if age > 50:
            if random.random() < 0.3:
                medical_conditions.append('Hypertension')
            if random.random() < 0.2:
                medical_conditions.append('Diabetes')
        
        if age > 60:
            if random.random() < 0.25:
                medical_conditions.append('Heart Disease')
            if random.random() < 0.15:
                medical_conditions.append('Arthritis')
        
        # Gender-specific conditions
        if gender == 'Female' and age > 40:
            if random.random() < 0.1:
                medical_conditions.append('Breast Cancer')
        
        if gender == 'Male' and age > 50:
            if random.random() < 0.08:
                medical_conditions.append('Prostate Cancer')
        
        # Random conditions
        if random.random() < 0.05:
            medical_conditions.append('Asthma')
        if random.random() < 0.03:
            medical_conditions.append('Cystic Fibrosis')
        if random.random() < 0.02:
            medical_conditions.append('Hemophilia')
        
        medical_history = ', '.join(medical_conditions) if medical_conditions else 'None'
        
        # Family history
        family_conditions = []
        if random.random() < 0.4:
            family_conditions.append('Diabetes')
        if random.random() < 0.3:
            family_conditions.append('Heart Disease')
        if random.random() < 0.2:
            family_conditions.append('Cancer')
        if random.random() < 0.15:
            family_conditions.append('Alzheimer')
        
        family_history = ', '.join(family_conditions) if family_conditions else 'None'
        
        # Lifestyle factors
        lifestyle_factors = []
        if random.random() < 0.3:
            lifestyle_factors.append('Smoking')
        if random.random() < 0.4:
            lifestyle_factors.append('Sedentary')
        if random.random() < 0.2:
            lifestyle_factors.append('Obesity')
        if random.random() < 0.6:
            lifestyle_factors.append('Regular Exercise')
        
        lifestyle = ', '.join(lifestyle_factors) if lifestyle_factors else 'Healthy'
        
        # BMI (realistic distribution)
        bmi = np.random.normal(25, 5)  # Mean 25, std 5
        bmi = max(16, min(50, bmi))  # Clamp between 16-50
        
        # Blood pressure
        systolic = int(np.random.normal(120, 20))
        diastolic = int(np.random.normal(80, 10))
        
        return {
            'age': age,
            'gender': gender,
            'blood_group': blood_group,
            'medical_history': medical_history,
            'family_history': family_history,
            'lifestyle': lifestyle,
            'bmi': round(bmi, 1),
            'systolic_bp': max(90, min(200, systolic)),
            'diastolic_bp': max(60, min(120, diastolic)),
            'report_type': random.choice(['Routine', 'Diagnostic', 'Screening', 'Follow-up']),
            'created_date': datetime.now().isoformat()
        }
    
    def _select_patient_associations(self, patient_metadata: Dict) -> pd.DataFrame:
        """Select relevant gene-disease associations for a patient"""
        # Filter associations based on patient characteristics
        relevant_associations = self.gene_disease_associations.copy()
        
        # Age-based filtering
        age = patient_metadata['age']
        if age < 30:
            # Younger patients: focus on genetic conditions
            relevant_associations = relevant_associations[
                relevant_associations['disease_class'].isin(['Blood diseases', 'Respiratory diseases'])
            ]
        elif age > 60:
            # Older patients: focus on age-related conditions
            relevant_associations = relevant_associations[
                relevant_associations['disease_class'].isin(['Cardiovascular diseases', 'Nervous system diseases', 'Neoplasms'])
            ]
        
        # Medical history-based filtering
        medical_history = patient_metadata['medical_history'].lower()
        if 'diabetes' in medical_history:
            diabetes_genes = ['INS', 'GCK', 'HNF1A', 'HNF4A', 'PPARG', 'KCNJ11', 'ABCC8']
            relevant_associations = relevant_associations[
                relevant_associations['gene_symbol'].isin(diabetes_genes)
            ]
        elif 'cancer' in medical_history:
            cancer_genes = ['TP53', 'BRCA1', 'BRCA2', 'APC', 'KRAS', 'BRAF', 'EGFR']
            relevant_associations = relevant_associations[
                relevant_associations['gene_symbol'].isin(cancer_genes)
            ]
        
        # If no relevant associations found, use random sample
        if len(relevant_associations) == 0:
            relevant_associations = self.gene_disease_associations.sample(
                min(10, len(self.gene_disease_associations))
            )
        else:
            # Limit to reasonable number
            relevant_associations = relevant_associations.sample(
                min(15, len(relevant_associations))
            )
        
        return relevant_associations
    
    def _calculate_personalized_risk_factors(self, 
                                           patient_metadata: Dict, 
                                           association: pd.Series) -> Dict:
        """Calculate personalized risk factors for a patient-gene-disease combination"""
        risk_factors = {}
        
        # Base risk from association score
        base_risk = association['score']
        
        # Age factor
        age_factor = 1.0
        if patient_metadata['age'] > 60:
            age_factor = 1.3
        elif patient_metadata['age'] > 40:
            age_factor = 1.1
        elif patient_metadata['age'] < 25:
            age_factor = 0.8
        
        # Gender factor
        gender_factor = 1.0
        if patient_metadata['gender'] == 'Female':
            if 'breast cancer' in association['disease_name'].lower():
                gender_factor = 1.5
        elif patient_metadata['gender'] == 'Male':
            if 'prostate cancer' in association['disease_name'].lower():
                gender_factor = 1.4
        
        # Medical history factor
        medical_factor = 1.0
        medical_history = patient_metadata['medical_history'].lower()
        disease_name = association['disease_name'].lower()
        
        if 'diabetes' in medical_history and 'diabetes' in disease_name:
            medical_factor = 1.8
        elif 'hypertension' in medical_history and 'cardiovascular' in association['disease_class'].lower():
            medical_factor = 1.6
        elif 'cancer' in medical_history and 'cancer' in disease_name:
            medical_factor = 1.7
        
        # Family history factor
        family_factor = 1.0
        family_history = patient_metadata['family_history'].lower()
        
        if 'diabetes' in family_history and 'diabetes' in disease_name:
            family_factor = 1.4
        elif 'heart disease' in family_history and 'cardiovascular' in association['disease_class'].lower():
            family_factor = 1.3
        elif 'cancer' in family_history and 'cancer' in disease_name:
            family_factor = 1.5
        elif 'alzheimer' in family_history and 'alzheimer' in disease_name:
            family_factor = 1.6
        
        # Lifestyle factor
        lifestyle_factor = 1.0
        lifestyle = patient_metadata['lifestyle'].lower()
        
        if 'smoking' in lifestyle and 'cancer' in disease_name:
            lifestyle_factor = 1.4
        elif 'obesity' in lifestyle and 'diabetes' in disease_name:
            lifestyle_factor = 1.3
        elif 'sedentary' in lifestyle and 'cardiovascular' in association['disease_class'].lower():
            lifestyle_factor = 1.2
        elif 'regular exercise' in lifestyle:
            lifestyle_factor = 0.9
        
        # BMI factor
        bmi_factor = 1.0
        bmi = patient_metadata['bmi']
        if bmi > 30:  # Obese
            if 'diabetes' in disease_name or 'cardiovascular' in association['disease_class'].lower():
                bmi_factor = 1.3
        elif bmi < 18.5:  # Underweight
            bmi_factor = 0.9
        
        # Calculate personalized risk score
        personalized_risk = base_risk * age_factor * gender_factor * medical_factor * family_factor * lifestyle_factor * bmi_factor
        
        # Clamp to [0, 1]
        personalized_risk = max(0.0, min(1.0, personalized_risk))
        
        # Risk category
        if personalized_risk > 0.7:
            risk_category = 'High'
        elif personalized_risk > 0.4:
            risk_category = 'Medium'
        else:
            risk_category = 'Low'
        
        # Health status
        if personalized_risk > 0.7:
            health_status = 'High Risk'
        elif personalized_risk > 0.4:
            health_status = 'At Risk'
        else:
            health_status = 'Normal'
        
        risk_factors.update({
            'personalized_risk_score': round(personalized_risk, 3),
            'risk_category': risk_category,
            'health_status': health_status,
            'age_factor': round(age_factor, 2),
            'gender_factor': round(gender_factor, 2),
            'medical_factor': round(medical_factor, 2),
            'family_factor': round(family_factor, 2),
            'lifestyle_factor': round(lifestyle_factor, 2),
            'bmi_factor': round(bmi_factor, 2)
        })
        
        return risk_factors
    
    def _generate_personalized_summary(self, df: pd.DataFrame, filename: str):
        """Generate summary report for personalized dataset"""
        logger.info("Generating personalized dataset summary...")
        
        report = {
            'dataset_info': {
                'total_records': int(len(df)),
                'unique_patients': int(df['patient_id'].nunique()),
                'unique_genes': int(df['gene_symbol'].nunique()),
                'unique_diseases': int(df['disease_name'].nunique()),
                'date_generated': datetime.now().isoformat(),
                'filename': filename
            },
            'patient_demographics': {
                'age_distribution': {
                    'mean_age': float(df['age'].mean()),
                    'median_age': float(df['age'].median()),
                    'min_age': int(df['age'].min()),
                    'max_age': int(df['age'].max())
                },
                'gender_distribution': df['gender'].value_counts().to_dict(),
                'blood_group_distribution': df['blood_group'].value_counts().to_dict()
            },
            'risk_distribution': {
                'mean_personalized_risk': float(df['personalized_risk_score'].mean()),
                'risk_category_distribution': df['risk_category'].value_counts().to_dict(),
                'health_status_distribution': df['health_status'].value_counts().to_dict()
            },
            'top_diseases': df.groupby('disease_name')['personalized_risk_score'].mean().nlargest(10).to_dict(),
            'top_genes': df.groupby('gene_symbol')['personalized_risk_score'].mean().nlargest(10).to_dict()
        }
        
        # Save report
        report_filename = filename.replace('.csv', '_summary.json')
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Summary report saved to: {report_filename}")
        
        # Print summary
        print("\n" + "="*60)
        print("PERSONALIZED DATASET SUMMARY")
        print("="*60)
        print(f"Total Records: {report['dataset_info']['total_records']:,}")
        print(f"Unique Patients: {report['dataset_info']['unique_patients']:,}")
        print(f"Unique Genes: {report['dataset_info']['unique_genes']:,}")
        print(f"Unique Diseases: {report['dataset_info']['unique_diseases']:,}")
        print(f"Mean Age: {report['patient_demographics']['age_distribution']['mean_age']:.1f}")
        print(f"Mean Personalized Risk: {report['risk_distribution']['mean_personalized_risk']:.3f}")
        print("="*60)
    
    def create_ml_training_dataset(self, 
                                  output_file: str = None,
                                  target_variable: str = 'personalized_risk_score') -> str:
        """
        Create a dataset specifically formatted for ML training
        
        Args:
            output_file (str): Output filename
            target_variable (str): Target variable for ML training
            
        Returns:
            str: Path to generated CSV file
        """
        logger.info("Creating ML training dataset...")
        
        # Generate personalized dataset first
        personalized_file = self.generate_personalized_dataset(n_patients=3000)
        df = pd.read_csv(personalized_file)
        
        # Select features for ML training
        feature_columns = [
            # Patient features
            'age', 'gender', 'blood_group', 'bmi', 'systolic_bp', 'diastolic_bp',
            
            # Gene features
            'gene_id', 'gene_symbol', 'disease_class_encoded',
            
            # Association features
            'score', 'ei', 'combined_score', 'evidence_strength', 'association_age', 'research_activity',
            
            # Risk factors
            'age_factor', 'gender_factor', 'medical_factor', 'family_factor', 'lifestyle_factor', 'bmi_factor'
        ]
        
        # Create ML dataset
        ml_df = df[feature_columns + [target_variable]].copy()
        
        # Encode categorical variables
        categorical_cols = ['gender', 'blood_group', 'gene_symbol']
        for col in categorical_cols:
            if col in ml_df.columns:
                ml_df[col] = ml_df[col].astype('category').cat.codes
        
        # Handle missing values
        ml_df = ml_df.fillna(ml_df.median())
        
        # Save ML dataset
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"ml_training_dataset_{timestamp}.csv"
        
        if not output_file.endswith('.csv'):
            output_file += '.csv'
        
        ml_df.to_csv(output_file, index=False, encoding='utf-8')
        
        logger.info(f"ML training dataset saved to: {output_file}")
        logger.info(f"Features: {len(feature_columns)}, Target: {target_variable}")
        logger.info(f"Records: {len(ml_df)}")
        
        return output_file


def main():
    """
    Main function to demonstrate the personalized data collector
    """
    try:
        # Initialize collector
        collector = PersonalizedGeneDiseaseCollector()
        
        # Generate personalized dataset
        print("Generating personalized gene-disease dataset...")
        personalized_file = collector.generate_personalized_dataset(n_patients=2000)
        
        # Create ML training dataset
        print("\nCreating ML training dataset...")
        ml_file = collector.create_ml_training_dataset()
        
        print(f"\n✅ Successfully generated datasets:")
        print(f"Personalized Dataset: {personalized_file}")
        print(f"ML Training Dataset: {ml_file}")
        print("\nYou can now use these datasets for personalized gene-disease prediction!")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
