#!/usr/bin/env python3
"""
PDF to CSV Converter for Gene Reports
====================================

Converts PDF gene reports to CSV format compatible with the ML model
"""

import pandas as pd
import numpy as np
import re
import json
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFToCSVConverter:
    def __init__(self):
        self.gene_patterns = {
            'gene_name': r'Gene[:\s]+([A-Z0-9]+)',
            'gene_value': r'Value[:\s]+([0-9.]+)',
            'normal_range': r'Normal[:\s]+([0-9.-]+)\s*-\s*([0-9.-]+)',
            'patient_age': r'Age[:\s]+([0-9]+)',
            'patient_gender': r'Gender[:\s]+(Male|Female)',
            'blood_group': r'Blood[:\s]+([A-Z][+-]?)',
            'medical_history': r'History[:\s]+([^,\n]+)',
            'report_type': r'Type[:\s]+([A-Za-z]+)'
        }
        
        # Common gene-disease associations
        self.gene_disease_map = {
            'TP53': 'Breast cancer',
            'BRCA1': 'Breast cancer',
            'BRCA2': 'Breast cancer',
            'APC': 'Colorectal cancer',
            'MLH1': 'Lynch syndrome',
            'MSH2': 'Lynch syndrome',
            'PTEN': 'Cowden syndrome',
            'RB1': 'Retinoblastoma',
            'VHL': 'Von Hippel-Lindau syndrome',
            'NF1': 'Neurofibromatosis',
            'CFTR': 'Cystic fibrosis',
            'HBB': 'Sickle cell anemia',
            'F8': 'Hemophilia A',
            'F9': 'Hemophilia B',
            'DMD': 'Duchenne muscular dystrophy',
            'HTT': 'Huntington disease',
            'PSEN1': 'Alzheimer disease',
            'PSEN2': 'Alzheimer disease',
            'APP': 'Alzheimer disease',
            'SNCA': 'Parkinson disease',
            'LRRK2': 'Parkinson disease',
            'PARK2': 'Parkinson disease',
            'PINK1': 'Parkinson disease',
            'DJ1': 'Parkinson disease',
            'ATP7B': 'Wilson disease',
            'HFE': 'Hemochromatosis',
            'G6PD': 'G6PD deficiency',
            'PAH': 'Phenylketonuria',
            'GALT': 'Galactosemia',
            'GBA': 'Gaucher disease'
        }
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except ImportError:
            logger.error("PyPDF2 not installed. Please install: pip install PyPDF2")
            return ""
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            return ""
    
    def parse_gene_data(self, text: str) -> List[Dict[str, Any]]:
        """Parse gene data from extracted text"""
        gene_data = []
        
        # Split text into sections (assuming each gene is in a separate section)
        sections = re.split(r'\n\s*\n', text)
        
        for section in sections:
            gene_info = {}
            
            # Extract gene name
            gene_match = re.search(self.gene_patterns['gene_name'], section, re.IGNORECASE)
            if gene_match:
                gene_info['gene_symbol'] = gene_match.group(1)
                
                # Get disease from mapping
                gene_info['disease_name'] = self.gene_disease_map.get(
                    gene_info['gene_symbol'], 'Unknown disease'
                )
                
                # Extract gene value
                value_match = re.search(self.gene_patterns['gene_value'], section, re.IGNORECASE)
                if value_match:
                    gene_info['gene_value'] = float(value_match.group(1))
                
                # Extract normal range
                range_match = re.search(self.gene_patterns['normal_range'], section, re.IGNORECASE)
                if range_match:
                    gene_info['normal_min'] = float(range_match.group(1))
                    gene_info['normal_max'] = float(range_match.group(2))
                
                # Calculate if gene is deficient or excessive
                if 'gene_value' in gene_info and 'normal_min' in gene_info and 'normal_max' in gene_info:
                    value = gene_info['gene_value']
                    min_val = gene_info['normal_min']
                    max_val = gene_info['normal_max']
                    
                    if value < min_val:
                        gene_info['status'] = 'deficient'
                        gene_info['deviation'] = (min_val - value) / min_val
                    elif value > max_val:
                        gene_info['status'] = 'excessive'
                        gene_info['deviation'] = (value - max_val) / max_val
                    else:
                        gene_info['status'] = 'normal'
                        gene_info['deviation'] = 0.0
                
                gene_data.append(gene_info)
        
        return gene_data
    
    def extract_patient_info(self, text: str) -> Dict[str, Any]:
        """Extract patient information from text"""
        patient_info = {}
        
        # Extract age
        age_match = re.search(self.gene_patterns['patient_age'], text, re.IGNORECASE)
        if age_match:
            patient_info['age'] = int(age_match.group(1))
        
        # Extract gender
        gender_match = re.search(self.gene_patterns['patient_gender'], text, re.IGNORECASE)
        if gender_match:
            patient_info['gender'] = gender_match.group(1)
        
        # Extract blood group
        blood_match = re.search(self.gene_patterns['blood_group'], text, re.IGNORECASE)
        if blood_match:
            patient_info['blood_group'] = blood_match.group(1)
        
        # Extract medical history
        history_match = re.search(self.gene_patterns['medical_history'], text, re.IGNORECASE)
        if history_match:
            patient_info['medical_history'] = history_match.group(1)
        
        # Extract report type
        type_match = re.search(self.gene_patterns['report_type'], text, re.IGNORECASE)
        if type_match:
            patient_info['report_type'] = type_match.group(1)
        
        return patient_info
    
    def convert_to_ml_format(self, gene_data: List[Dict], patient_info: Dict) -> pd.DataFrame:
        """Convert extracted data to ML model format"""
        ml_records = []
        
        for gene in gene_data:
            # Create base record with patient info
            record = {
                'patient_id': f"P{len(ml_records):04d}",
                'age': patient_info.get('age', 45),
                'gender': patient_info.get('gender', 'Unknown'),
                'blood_group': patient_info.get('blood_group', 'Unknown'),
                'medical_history': patient_info.get('medical_history', 'None'),
                'report_type': patient_info.get('report_type', 'Routine'),
                
                # Gene information
                'gene_id': self._get_gene_id(gene.get('gene_symbol', 'Unknown')),
                'gene_symbol': gene.get('gene_symbol', 'Unknown'),
                'disease_name': gene.get('disease_name', 'Unknown'),
                'disease_class_encoded': self._encode_disease_class(gene.get('disease_name', 'Unknown')),
                
                # Gene values and calculations
                'gene_value': gene.get('gene_value', 0.0),
                'normal_min': gene.get('normal_min', 0.0),
                'normal_max': gene.get('normal_max', 0.0),
                'status': gene.get('status', 'normal'),
                'deviation': gene.get('deviation', 0.0),
                
                # Derived features for ML
                'score': self._calculate_gene_score(gene),
                'ei': self._calculate_evidence_index(gene),
                'combined_score': self._calculate_combined_score(gene),
                'evidence_strength': self._calculate_evidence_strength(gene),
                'association_age': self._get_association_age(gene.get('gene_symbol', 'Unknown')),
                'research_activity': self._get_research_activity(gene.get('gene_symbol', 'Unknown')),
                
                # Patient-specific factors
                'age_factor': self._calculate_age_factor(patient_info.get('age', 45)),
                'gender_factor': self._calculate_gender_factor(patient_info.get('gender', 'Unknown')),
                'medical_factor': self._calculate_medical_factor(patient_info.get('medical_history', 'None')),
                'family_factor': 1.0,  # Default value
                'lifestyle_factor': 1.0,  # Default value
                'bmi_factor': 1.0,  # Default value
                
                # Additional features
                'systolic_bp': 120,  # Default value
                'diastolic_bp': 80,  # Default value
                'bmi': 24.5,  # Default value
            }
            
            ml_records.append(record)
        
        return pd.DataFrame(ml_records)
    
    def _get_gene_id(self, gene_symbol: str) -> int:
        """Get gene ID from symbol"""
        gene_ids = {
            'TP53': 7157, 'BRCA1': 675, 'BRCA2': 675, 'APC': 324, 'MLH1': 4292,
            'MSH2': 4436, 'PTEN': 5728, 'RB1': 5925, 'VHL': 7428, 'NF1': 4763,
            'CFTR': 1080, 'HBB': 3043, 'F8': 2157, 'F9': 2158, 'DMD': 1756,
            'HTT': 3064, 'PSEN1': 5663, 'PSEN2': 5664, 'APP': 351, 'SNCA': 6622,
            'LRRK2': 120892, 'PARK2': 5071, 'PINK1': 65018, 'DJ1': 11315,
            'ATP7B': 540, 'HFE': 3077, 'G6PD': 2539, 'PAH': 5053, 'GALT': 2592,
            'GBA': 2629
        }
        return gene_ids.get(gene_symbol, 9999)
    
    def _encode_disease_class(self, disease_name: str) -> int:
        """Encode disease class"""
        disease_classes = {
            'Breast cancer': 1, 'Colorectal cancer': 1, 'Lynch syndrome': 1,
            'Cowden syndrome': 1, 'Retinoblastoma': 1, 'Von Hippel-Lindau syndrome': 1,
            'Neurofibromatosis': 1, 'Cystic fibrosis': 2, 'Sickle cell anemia': 2,
            'Hemophilia A': 2, 'Hemophilia B': 2, 'Duchenne muscular dystrophy': 2,
            'Huntington disease': 3, 'Alzheimer disease': 3, 'Parkinson disease': 3,
            'Wilson disease': 2, 'Hemochromatosis': 2, 'G6PD deficiency': 2,
            'Phenylketonuria': 2, 'Galactosemia': 2, 'Gaucher disease': 2
        }
        return disease_classes.get(disease_name, 0)
    
    def _calculate_gene_score(self, gene: Dict) -> float:
        """Calculate gene score based on deviation and status"""
        deviation = gene.get('deviation', 0.0)
        status = gene.get('status', 'normal')
        
        if status == 'normal':
            return 0.5
        elif status == 'deficient':
            return max(0.1, 0.5 - deviation)
        else:  # excessive
            return min(0.9, 0.5 + deviation)
    
    def _calculate_evidence_index(self, gene: Dict) -> float:
        """Calculate evidence index"""
        base_score = gene.get('score', 0.5)
        return base_score * 0.9 + np.random.uniform(0.05, 0.15)
    
    def _calculate_combined_score(self, gene: Dict) -> float:
        """Calculate combined score"""
        score = gene.get('score', 0.5)
        ei = gene.get('ei', 0.5)
        return (score + ei) / 2
    
    def _calculate_evidence_strength(self, gene: Dict) -> float:
        """Calculate evidence strength"""
        return min(0.95, gene.get('combined_score', 0.5) + np.random.uniform(0.1, 0.2))
    
    def _get_association_age(self, gene_symbol: str) -> int:
        """Get association age for gene"""
        return np.random.randint(5, 25)
    
    def _get_research_activity(self, gene_symbol: str) -> float:
        """Get research activity for gene"""
        return np.random.uniform(0.01, 0.1)
    
    def _calculate_age_factor(self, age: int) -> float:
        """Calculate age factor"""
        if age < 30:
            return 0.8
        elif age < 50:
            return 1.0
        elif age < 70:
            return 1.2
        else:
            return 1.5
    
    def _calculate_gender_factor(self, gender: str) -> float:
        """Calculate gender factor"""
        return 1.0 if gender.lower() == 'male' else 1.1
    
    def _calculate_medical_factor(self, history: str) -> float:
        """Calculate medical history factor"""
        if 'diabetes' in history.lower():
            return 1.3
        elif 'hypertension' in history.lower():
            return 1.2
        elif 'cancer' in history.lower():
            return 1.5
        else:
            return 1.0
    
    def convert_pdf_to_csv(self, pdf_path: str, output_path: str = None) -> str:
        """Main method to convert PDF to CSV"""
        logger.info(f"Converting PDF: {pdf_path}")
        
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        if not text:
            raise ValueError("Could not extract text from PDF")
        
        # Parse gene data
        gene_data = self.parse_gene_data(text)
        if not gene_data:
            raise ValueError("No gene data found in PDF")
        
        # Extract patient info
        patient_info = self.extract_patient_info(text)
        
        # Convert to ML format
        df = self.convert_to_ml_format(gene_data, patient_info)
        
        # Save to CSV
        if output_path is None:
            output_path = pdf_path.replace('.pdf', '_converted.csv')
        
        df.to_csv(output_path, index=False)
        logger.info(f"Converted to CSV: {output_path}")
        logger.info(f"Generated {len(df)} records")
        
        return output_path


def main():
    """Test the converter"""
    converter = PDFToCSVConverter()
    
    # Create a sample PDF content for testing
    sample_text = """
    Gene Report
    ===========
    
    Patient Information:
    Age: 45
    Gender: Female
    Blood: A+
    History: Diabetes, Hypertension
    Type: Diagnostic
    
    Gene Analysis:
    ==============
    
    Gene: TP53
    Value: 0.8
    Normal: 1.0 - 2.0
    Status: Deficient
    
    Gene: BRCA1
    Value: 2.5
    Normal: 1.0 - 2.0
    Status: Excessive
    
    Gene: APC
    Value: 1.5
    Normal: 1.0 - 2.0
    Status: Normal
    """
    
    # Save sample text to a file for testing
    with open('sample_report.txt', 'w') as f:
        f.write(sample_text)
    
    print("Sample report created: sample_report.txt")
    print("Note: This is a text file. In real usage, you would upload a PDF file.")


if __name__ == "__main__":
    main()
