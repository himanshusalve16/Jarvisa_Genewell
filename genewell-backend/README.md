# GeneWell ML Backend - Gene-based Disease Prediction System

A comprehensive machine learning pipeline for predicting diseases based on gene expression data and patient metadata.

## 🚀 Features

- **Multi-disease Prediction**: Predicts risk for 12 common genetically influenced diseases
- **Advanced Feature Engineering**: Creates derived features from gene expression patterns
- **Multiple ML Models**: Compares Logistic Regression, Random Forest, and XGBoost
- **Hyperparameter Tuning**: Optimizes model performance using GridSearchCV
- **RESTful API**: Flask-based API for easy integration
- **Interactive Visualizations**: Plotly-based dashboards and reports
- **Export Capabilities**: Excel and PDF report generation

## 🏥 Supported Diseases

1. **Diabetes Type 1** - Insulin gene (INS) deficiency
2. **Diabetes Type 2** - Multiple genes (GCK, HNF1A, etc.)
3. **Hypertension** - Age and medical history based
4. **Breast Cancer** - BRCA1/BRCA2 genes
5. **Colon Cancer** - APC, KRAS genes
6. **Lung Cancer** - EGFR, BRAF genes
7. **Cardiovascular Disease** - Age and lifestyle factors
8. **Alzheimer's Disease** - APOE gene and age
9. **Hemophilia A** - F8 gene deficiency
10. **Hemophilia B** - F9 gene deficiency
11. **Cystic Fibrosis** - CFTR gene
12. **Sickle Cell Anemia** - HBB gene

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies

## 🛠️ Installation

1. **Clone the repository**:
```bash
cd Jarvisa_Genewell/genewell-backend
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the ML pipeline**:
```bash
python gene_disease_predictor.py
```

4. **Start the API server**:
```bash
python app.py
```

## 📊 Data Format

### Input CSV Structure

Your CSV file should contain the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `Patient_ID` | Unique patient identifier | P0001 |
| `Age` | Patient age | 45 |
| `Gender` | Patient gender | Male/Female |
| `Blood_Group` | Blood group | A+, B-, O+, etc. |
| `Medical_History` | Previous conditions | None, Hypertension, Diabetes |
| `Report_Type` | Type of report | Routine, Diagnostic, Screening |
| `{GENE}_Value` | Gene expression level | 1.25 |
| `{GENE}_Normal_Min` | Normal range minimum | 0.8 |
| `{GENE}_Normal_Max` | Normal range maximum | 1.5 |

### Supported Genes

- **Cancer Genes**: BRCA1, BRCA2, TP53, APC, KRAS, BRAF, EGFR, HER2
- **Metabolic Genes**: INS, GCK, HNF1A, HNF4A, PPARG, KCNJ11, ABCC8
- **Neurological Genes**: APP, PSEN1, PSEN2, APOE
- **Blood Disorder Genes**: F8, F9, HBB
- **Other**: CFTR

## 🔧 API Endpoints

### Base URL: `http://localhost:5000`

#### 1. Health Check
```http
GET /health
```
Returns API health status and model loading status.

#### 2. Train Model
```http
POST /train
```
Trains the ML model with synthetic data (automatically called on startup).

#### 3. Upload and Predict
```http
POST /predict
Content-Type: multipart/form-data

file: your_gene_data.csv
```
Upload a CSV file and get disease predictions.

#### 4. Model Information
```http
GET /model-info
```
Get model performance metrics and feature information.

#### 5. Download Sample Data
```http
GET /sample-data
```
Download a sample CSV file for testing.

#### 6. Batch Prediction
```http
POST /predict-batch
Content-Type: application/json

{
  "patients": [
    {
      "Patient_ID": "P0001",
      "Age": 45,
      "Gender": "Male",
      "Blood_Group": "A+",
      "Medical_History": "None",
      "Report_Type": "Routine",
      "BRCA1_Value": 1.2,
      "BRCA1_Normal_Min": 0.8,
      "BRCA1_Normal_Max": 1.5,
      ...
    }
  ]
}
```

#### 7. Export Report
```http
POST /export-report
Content-Type: application/json

{
  "results": [...]
}
```
Generate a detailed report from prediction results.

## 📈 Usage Examples

### Python Script Usage

```python
from gene_disease_predictor import GeneDiseasePredictor

# Initialize predictor
predictor = GeneDiseasePredictor()

# Generate synthetic data for testing
df = predictor.generate_synthetic_data(n_samples=1000)

# Train the model
X, y = predictor.preprocess_data(df)
X = predictor.engineer_features(X)
X_test, y_test = predictor.train_models(X, y)
predictor.hyperparameter_tuning(X, y)

# Save the model
predictor.save_model('my_model.pkl')

# Make predictions
results = predictor.predict_from_csv('patient_data.csv')
print(results)
```

### API Usage with Python

```python
import requests

# Upload CSV file
with open('patient_data.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5000/predict', files=files)

results = response.json()
print(results['results'])
```

### API Usage with JavaScript

```javascript
// Upload CSV file
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:5000/predict', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    console.log('Predictions:', data.results);
});
```

## 📊 Visualization

The system includes comprehensive visualization tools:

```python
from visualization import GeneDiseaseVisualizer

visualizer = GeneDiseaseVisualizer()

# Create interactive dashboard
fig = visualizer.create_interactive_dashboard(results)
fig.show()

# Generate patient report
patient_report = visualizer.generate_patient_report(results[0])
patient_report.show()

# Export to Excel
visualizer.export_results_to_excel(results, 'predictions.xlsx')
```

## 🔍 Model Performance

The system automatically compares multiple models:

- **Logistic Regression**: Baseline linear model
- **Random Forest**: Ensemble method with feature importance
- **XGBoost**: Gradient boosting with regularization

Performance metrics include:
- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC

## 🎯 Feature Engineering

The system creates derived features:

1. **Deficiency Flags**: Binary indicators for genes below normal range
2. **Excess Flags**: Binary indicators for genes above normal range
3. **Deviation Scores**: Normalized deviation from normal range
4. **Categorical Encoding**: Gender, blood group, medical history

## 📁 Project Structure

```
genewell-backend/
├── gene_disease_predictor.py  # Main ML pipeline
├── app.py                     # Flask API server
├── visualization.py           # Visualization tools
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── uploads/                   # Temporary file uploads
├── gene_disease_model.pkl     # Trained model (auto-generated)
└── sample_gene_data.csv       # Sample data (auto-generated)
```

## 🚀 Quick Start

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Start the server**:
```bash
python app.py
```

3. **Test the API**:
```bash
curl http://localhost:5000/health
```

4. **Download sample data**:
```bash
curl http://localhost:5000/sample-data -o sample.csv
```

5. **Make predictions**:
```bash
curl -X POST -F "file=@sample.csv" http://localhost:5000/predict
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file for configuration:

```env
FLASK_ENV=development
FLASK_DEBUG=True
UPLOAD_FOLDER=uploads
MODEL_PATH=gene_disease_model.pkl
```

### Model Parameters

Adjust model parameters in `gene_disease_predictor.py`:

```python
# Number of samples for training
n_samples = 1000

# Test split ratio
test_size = 0.2

# Cross-validation folds
cv_folds = 5

# Risk thresholds
HIGH_RISK_THRESHOLD = 0.7
MODERATE_RISK_THRESHOLD = 0.4
```

## 🧪 Testing

### Unit Tests

```bash
python -m pytest tests/
```

### API Tests

```bash
# Test health endpoint
curl http://localhost:5000/health

# Test model training
curl -X POST http://localhost:5000/train

# Test prediction
curl -X POST -F "file=@sample_gene_data.csv" http://localhost:5000/predict
```

## 📈 Performance Optimization

1. **Model Caching**: Trained models are automatically saved and loaded
2. **Batch Processing**: Handle multiple patients efficiently
3. **Memory Management**: Clean up temporary files automatically
4. **Parallel Processing**: Hyperparameter tuning uses multiple cores

## 🔒 Security Considerations

1. **File Validation**: Only CSV files are accepted
2. **Input Sanitization**: All inputs are validated and sanitized
3. **Temporary Files**: Uploaded files are automatically cleaned up
4. **CORS Configuration**: Configured for frontend integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

1. Check the documentation
2. Review the example code
3. Open an issue on GitHub
4. Contact the development team

## 🔮 Future Enhancements

- [ ] Deep learning models (Neural Networks)
- [ ] Real-time gene sequencing integration
- [ ] Mobile app support
- [ ] Advanced visualization dashboards
- [ ] Integration with medical databases
- [ ] Automated report generation
- [ ] Multi-language support

---

**Note**: This system is designed for educational and research purposes. For clinical use, additional validation and regulatory compliance may be required.
