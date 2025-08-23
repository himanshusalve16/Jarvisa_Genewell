# GeneWell Frontend

A React-based frontend application for the GeneWell ML system that provides a user-friendly interface for uploading genomic reports and viewing personalized risk assessments.

## Features

- **File Upload**: Upload CSV or PDF genomic reports
- **Real-time Analysis**: Get instant ML-powered risk assessments
- **Interactive Dashboards**: View detailed risk scores and health insights
- **Backend Integration**: Seamless connection with Flask backend API
- **Responsive Design**: Modern UI that works on all devices

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend server running on port 5000

## Installation

1. Install dependencies:
```bash
npm install
```

2. Configure backend URL (optional):
Create a `.env` file in the root directory:
```
REACT_APP_API_URL=http://localhost:5000
```

3. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Backend Integration

The frontend is configured to connect to the GeneWell backend API running on port 5000. Make sure the backend server is running before using the frontend.

### API Endpoints Used

- `GET /health` - Health check
- `GET /model-info` - Get model information
- `POST /train` - Train the ML model
- `POST /predict` - Upload file and get predictions
- `POST /convert-pdf` - Convert PDF to CSV
- `GET /sample-data` - Download sample data

### File Upload

The frontend supports uploading:
- **CSV files**: Direct genomic data files
- **PDF files**: Gene reports that will be converted to CSV

Maximum file size: 50MB

## Project Structure

```
src/
├── components/          # Reusable UI components
├── pages/              # Page components
├── services/           # API service layer
├── config/             # Configuration files
└── App.jsx            # Main application component
```

## Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

### Key Components

- **UploadReport**: File upload and analysis interface
- **RiskScore**: Risk assessment visualization dashboard
- **apiService**: Backend API communication layer
- **API_CONFIG**: Configuration for API endpoints

## Troubleshooting

### Backend Connection Issues

If you see "Backend is not connected" errors:

1. Ensure the backend server is running on port 5000
2. Check that CORS is properly configured in the backend
3. Verify the API URL in the configuration

### File Upload Issues

- Ensure file size is under 50MB
- Check that file format is supported (CSV or PDF)
- Verify backend model is trained

## Production Deployment

1. Build the application:
```bash
npm run build
```

2. Deploy the `build` folder to your web server

3. Update the `REACT_APP_API_URL` environment variable to point to your production backend

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the GeneWell ML system.
