# GeneWell ML System - Complete Setup Guide

This guide will help you set up and run the complete GeneWell ML system with both backend and frontend components.

## System Overview

GeneWell is a personalized gene-disease risk prediction system that:
- Processes genomic data from CSV or PDF files
- Uses ML models to predict disease risks
- Provides interactive dashboards for risk visualization
- Offers personalized health recommendations

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd GeneWell!
```

### 2. Backend Setup

Navigate to the backend directory:
```bash
cd Jarvisa_Genewell/genewell-backend
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Train the ML model:
```bash
python run.py
```
Choose option 5 for "Full Setup" to automatically:
- Check dependencies
- Train the ML model
- Start the API server

The backend will be available at `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:
```bash
cd Jarvisa_Genewell/genewell-frontend
```

Install Node.js dependencies:
```bash
npm install
```

Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Detailed Setup Instructions

### Backend Configuration

#### Environment Setup

The backend uses the following key files:
- `app.py` - Main Flask application
- `personalized_predictor.py` - ML model implementation
- `pdf_to_csv_converter.py` - PDF processing utility
- `requirements.txt` - Python dependencies

#### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/model-info` | GET | Model status |
| `/train` | POST | Train ML model |
| `/predict` | POST | Upload file and predict |
| `/convert-pdf` | POST | Convert PDF to CSV |
| `/sample-data` | GET | Download sample data |

#### Model Training

The system automatically trains a Random Forest model using:
- Gene-disease association data
- Patient demographic information
- Medical history factors
- Lifestyle indicators

### Frontend Configuration

#### Environment Variables

Create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENV=development
REACT_APP_DEBUG=true
```

#### Key Components

- **UploadReport**: File upload interface
- **RiskScore**: Risk visualization dashboard
- **apiService**: Backend communication layer
- **API_CONFIG**: Endpoint configuration

#### Supported File Types

- **CSV**: Direct genomic data files
- **PDF**: Gene reports (automatically converted)

Maximum file size: 50MB

## Testing the System

### 1. Backend Health Check

Visit `http://localhost:5000/health` to verify the backend is running.

### 2. Model Status

Visit `http://localhost:5000/model-info` to check if the ML model is trained.

### 3. Frontend Integration

1. Open `http://localhost:3000`
2. Navigate to "Upload Report"
3. Check the "System Status" section
4. Download sample data for testing
5. Upload a file and view results

### 4. Sample Workflow

1. **Download Sample Data**: Use the "Download Sample Data" button
2. **Upload File**: Upload the downloaded CSV file
3. **View Results**: See the prediction results table
4. **Detailed Analysis**: Click "View Detailed Analysis" for charts

## Troubleshooting

### Backend Issues

#### Port Already in Use
```bash
# Find process using port 5000
lsof -i :5000
# Kill the process
kill -9 <PID>
```

#### Missing Dependencies
```bash
pip install -r requirements.txt
```

#### Model Training Errors
```bash
# Check if training data exists
ls *.csv
# Re-run training
python run.py
```

### Frontend Issues

#### Backend Connection Failed
1. Ensure backend is running on port 5000
2. Check CORS configuration in backend
3. Verify API URL in frontend config

#### File Upload Errors
1. Check file size (max 50MB)
2. Verify file format (CSV or PDF)
3. Ensure model is trained

#### Build Errors
```bash
# Clear npm cache
npm cache clean --force
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

## Development

### Backend Development

```bash
# Run in debug mode
python app.py

# Run tests
python test_pipeline.py
```

### Frontend Development

```bash
# Start development server
npm start

# Build for production
npm run build
```

## Production Deployment

### Backend Deployment

1. Use a production WSGI server (Gunicorn):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. Set up environment variables:
```bash
export FLASK_ENV=production
export FLASK_DEBUG=0
```

### Frontend Deployment

1. Build the application:
```bash
npm run build
```

2. Deploy the `build` folder to your web server

3. Update API URL for production backend

## API Documentation

### File Upload Format

The system expects CSV files with the following columns:
- `patient_id`: Unique patient identifier
- `age`: Patient age
- `gender`: Patient gender
- `blood_group`: Blood group
- `bmi`: Body mass index
- `gene_id`: Gene identifier
- `disease_name`: Disease name
- `score`: Association score
- Additional medical and genetic features

### Response Format

```json
{
  "message": "Predictions completed successfully",
  "results": [
    {
      "patient_id": "P001",
      "risk_score": 0.75,
      "risk_level": "High",
      "health_status": "High Risk"
    }
  ],
  "total_patients": 1
}
```

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in both backend and frontend
3. Ensure all prerequisites are met
4. Verify network connectivity between frontend and backend

## License

This project is part of the GeneWell ML system for personalized genomic risk assessment.
