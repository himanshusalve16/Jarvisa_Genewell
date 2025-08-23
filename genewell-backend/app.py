from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import pandas as pd
import json
from werkzeug.utils import secure_filename
from personalized_predictor import PersonalizedPredictor
from pdf_to_csv_converter import PDFToCSVConverter
import tempfile
import zipfile
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'pdf'}
MODEL_PATH = 'personalized_model.pkl'

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize predictor and converter
predictor = PersonalizedPredictor()
pdf_converter = PDFToCSVConverter()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return jsonify({
        'message': 'GeneWell ML API',
        'version': '1.0.0',
        'description': 'Personalized Gene-Disease Risk Prediction System',
        'workflow': [
            '1. Upload PDF gene report',
            '2. System converts PDF to CSV format',
            '3. ML model predicts disease risks',
            '4. Returns personalized risk scores'
        ],
        'endpoints': {
            '/convert-pdf': 'Convert PDF gene report to CSV format',
            '/predict': 'Make predictions from CSV or PDF file',
            '/train': 'Train the ML model with personalized data',
            '/health': 'Check API health',
            '/model-info': 'Get model information and performance',
            '/sample-data': 'Download sample data for testing'
        }
    })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor.model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/train', methods=['POST'])
def train_model():
    """
    Train the ML model with personalized data
    """
    try:
        # Check if model already exists
        if os.path.exists(MODEL_PATH):
            predictor.load_model(MODEL_PATH)
            return jsonify({
                'message': 'Model already trained and loaded',
                'model_path': MODEL_PATH
            })
        
        # Load and preprocess data
        print("Loading and preprocessing data...")
        X, y = predictor.load_and_preprocess()
        
        # Train model
        print("Training model...")
        predictor.train_model(X, y)
        
        # Save model
        print("Saving model...")
        predictor.save_model(MODEL_PATH)
        
        return jsonify({
            'message': 'Model trained successfully',
            'model_path': MODEL_PATH,
            'features_count': X.shape[1],
            'samples_count': X.shape[0]
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make predictions from uploaded CSV file
    """
    try:
        # Check if model is trained
        if predictor.model is None:
            if os.path.exists(MODEL_PATH):
                predictor.load_model(MODEL_PATH)
            else:
                return jsonify({
                    'error': 'Model not trained. Please train the model first using /train endpoint.'
                }), 400
        
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type. Please upload a CSV or PDF file.'
            }), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Convert PDF to CSV if needed
        if filename.lower().endswith('.pdf'):
            try:
                csv_path = pdf_converter.convert_pdf_to_csv(filepath)
                # Use the converted CSV for predictions
                results = predictor.predict_from_csv(csv_path)
                # Clean up both files
                os.remove(filepath)
                os.remove(csv_path)
            except Exception as e:
                # Clean up PDF file
                os.remove(filepath)
                return jsonify({
                    'error': f'Error converting PDF: {str(e)}'
                }), 500
        else:
            # Direct CSV processing
            results = predictor.predict_from_csv(filepath)
            # Clean up uploaded file
            os.remove(filepath)
        
        return jsonify({
            'message': 'Predictions completed successfully',
            'results': results,
            'total_patients': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/convert-pdf', methods=['POST'])
def convert_pdf():
    """
    Convert PDF gene report to CSV format
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'No file selected'
            }), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({
                'error': 'Please upload a PDF file'
            }), 400
        
        # Save uploaded PDF
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(pdf_path)
        
        # Convert PDF to CSV
        csv_path = pdf_converter.convert_pdf_to_csv(pdf_path)
        
        # Read the converted CSV to get preview
        df = pd.read_csv(csv_path)
        preview = df.head(5).to_dict('records')
        
        # Clean up PDF file
        os.remove(pdf_path)
        
        return jsonify({
            'message': 'PDF converted successfully',
            'csv_path': csv_path,
            'total_records': len(df),
            'preview': preview,
            'columns': df.columns.tolist()
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/model-info')
def model_info():
    """
    Get model information and performance metrics
    """
    try:
        if predictor.model is None:
            if os.path.exists(MODEL_PATH):
                predictor.load_model(MODEL_PATH)
            else:
                return jsonify({
                    'error': 'Model not trained'
                }), 400
        
        return jsonify({
            'model_loaded': True,
            'features_count': len(predictor.feature_names) if hasattr(predictor, 'feature_names') else 0,
            'model_path': MODEL_PATH
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/sample-data')
def get_sample_data():
    """
    Generate and return sample data for testing
    """
    try:
        # Generate sample data for personalized prediction
        import pandas as pd
        import numpy as np
        
        sample_data = {
            'gene_id': [7157, 675, 7157, 675],
            'gene_symbol': ['TP53', 'BRCA1', 'TP53', 'BRCA1'],
            'disease_name': ['Breast cancer', 'Breast cancer', 'Ovarian cancer', 'Ovarian cancer'],
            'disease_class_encoded': [1, 1, 1, 1],
            'score': [0.85, 0.92, 0.78, 0.88],
            'ei': [0.78, 0.88, 0.72, 0.85],
            'combined_score': [0.82, 0.90, 0.75, 0.87],
            'evidence_strength': [0.9, 0.95, 0.85, 0.92],
            'association_age': [15, 20, 12, 18],
            'research_activity': [0.06, 0.08, 0.05, 0.07],
            'age': [45, 52, 38, 41],
            'gender': ['Female', 'Female', 'Male', 'Male'],
            'blood_group': ['A+', 'B+', 'O+', 'AB+'],
            'medical_history': ['Diabetes', 'None', 'Hypertension', 'None'],
            'bmi': [24.5, 26.8, 23.2, 25.1]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        df.to_csv(temp_file.name, index=False)
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name='sample_gene_data.csv',
            mimetype='text/csv'
        )
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    """
    Handle batch predictions from JSON data
    """
    try:
        # Check if model is trained
        if predictor.model is None:
            if os.path.exists(MODEL_PATH):
                predictor.load_model(MODEL_PATH)
            else:
                return jsonify({
                    'error': 'Model not trained. Please train the model first.'
                }), 400
        
        # Get JSON data
        data = request.get_json()
        
        if not data or 'patients' not in data:
            return jsonify({
                'error': 'No patient data provided'
            }), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(data['patients'])
        
        # Save to temporary CSV
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        df.to_csv(temp_file.name, index=False)
        
        # Make predictions
        results = predictor.predict_from_csv(temp_file.name)
        
        # Clean up
        os.remove(temp_file.name)
        
        return jsonify({
            'message': 'Batch predictions completed',
            'results': results,
            'total_patients': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/export-report', methods=['POST'])
def export_report():
    """
    Export prediction results as a detailed report
    """
    try:
        data = request.get_json()
        
        if not data or 'results' not in data:
            return jsonify({
                'error': 'No results data provided'
            }), 400
        
        results = data['results']
        
        # Create detailed report
        report = {
            'report_generated': datetime.now().isoformat(),
            'total_patients': len(results),
            'summary': {
                'high_risk': len([r for r in results if r['health_status'] == 'High Risk']),
                'at_risk': len([r for r in results if r['health_status'] == 'At Risk']),
                'normal': len([r for r in results if r['health_status'] == 'Normal'])
            },
            'patients': results
        }
        
        return jsonify(report)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Train model on startup if not exists
    if not os.path.exists(MODEL_PATH):
        print("Training model on startup...")
        try:
            # Load and preprocess data
            X, y = predictor.load_and_preprocess()
            
            # Train model
            predictor.train_model(X, y)
            
            # Save model
            predictor.save_model(MODEL_PATH)
            print("Model trained and saved successfully!")
            
        except Exception as e:
            print(f"Error training model: {e}")
    
    print("Starting GeneWell ML API server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
