// API Configuration for GeneWell Frontend
const API_CONFIG = {
  // Backend API base URL
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  
  // API Endpoints
  ENDPOINTS: {
    // Health check
    HEALTH: '/health',
    
    // Model information
    MODEL_INFO: '/model-info',
    
    // File upload and prediction
    PREDICT: '/predict',
    CONVERT_PDF: '/convert-pdf',
    
    // Model training
    TRAIN: '/train',
    
    // Sample data
    SAMPLE_DATA: '/sample-data',
    
    // Batch prediction
    PREDICT_BATCH: '/predict-batch',
    
    // Export report
    EXPORT_REPORT: '/export-report'
  },
  
  // File upload configuration
  UPLOAD: {
    MAX_FILE_SIZE: 50 * 1024 * 1024, // 50MB
    ALLOWED_TYPES: ['csv', 'pdf'],
    ALLOWED_MIME_TYPES: [
      'text/csv',
      'application/pdf',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]
  },
  
  // Request timeout
  TIMEOUT: 30000, // 30 seconds
  
  // Retry configuration
  RETRY: {
    MAX_ATTEMPTS: 3,
    DELAY: 1000 // 1 second
  }
};

// Helper function to get full API URL
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// Helper function to create axios instance with default config
export const createApiInstance = () => {
  const axios = require('axios');
  return axios.create({
    baseURL: API_CONFIG.BASE_URL,
    timeout: API_CONFIG.TIMEOUT,
    headers: {
      'Content-Type': 'application/json',
    }
  });
};

export default API_CONFIG;
