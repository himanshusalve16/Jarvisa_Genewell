import axios from 'axios';
import API_CONFIG, { getApiUrl } from '../config/api';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

class ApiService {
  // Health check
  async checkHealth() {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.HEALTH);
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }

  // Get model information
  async getModelInfo() {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.MODEL_INFO);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get model info: ${error.message}`);
    }
  }

  // Train model
  async trainModel() {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.TRAIN);
      return response.data;
    } catch (error) {
      throw new Error(`Model training failed: ${error.message}`);
    }
  }

  // Upload file and get predictions
  async uploadAndPredict(file, onProgress = null) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post(API_CONFIG.ENDPOINTS.PREDICT, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(percentCompleted);
          }
        }
      });

      return response.data;
    } catch (error) {
      throw new Error(`Prediction failed: ${error.response?.data?.error || error.message}`);
    }
  }

  // Convert PDF to CSV
  async convertPdfToCsv(file, onProgress = null) {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await apiClient.post(API_CONFIG.ENDPOINTS.CONVERT_PDF, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (onProgress) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(percentCompleted);
          }
        }
      });

      return response.data;
    } catch (error) {
      throw new Error(`PDF conversion failed: ${error.response?.data?.error || error.message}`);
    }
  }

  // Batch prediction from JSON data
  async predictBatch(patientData) {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.PREDICT_BATCH, {
        patients: patientData
      });
      return response.data;
    } catch (error) {
      throw new Error(`Batch prediction failed: ${error.response?.data?.error || error.message}`);
    }
  }

  // Export detailed report
  async exportReport(results) {
    try {
      const response = await apiClient.post(API_CONFIG.ENDPOINTS.EXPORT_REPORT, {
        results: results
      });
      return response.data;
    } catch (error) {
      throw new Error(`Report export failed: ${error.response?.data?.error || error.message}`);
    }
  }

  // Download sample data
  async downloadSampleData() {
    try {
      const response = await apiClient.get(API_CONFIG.ENDPOINTS.SAMPLE_DATA, {
        responseType: 'blob'
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'sample_gene_data.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      return { success: true, message: 'Sample data downloaded successfully' };
    } catch (error) {
      throw new Error(`Sample data download failed: ${error.message}`);
    }
  }

  // Validate file before upload
  validateFile(file) {
    const errors = [];

    // Check file size
    if (file.size > API_CONFIG.UPLOAD.MAX_FILE_SIZE) {
      errors.push(`File size (${(file.size / 1024 / 1024).toFixed(2)}MB) exceeds maximum allowed size (${API_CONFIG.UPLOAD.MAX_FILE_SIZE / 1024 / 1024}MB)`);
    }

    // Check file type
    const fileExtension = file.name.split('.').pop().toLowerCase();
    if (!API_CONFIG.UPLOAD.ALLOWED_TYPES.includes(fileExtension)) {
      errors.push(`File type (.${fileExtension}) is not supported. Allowed types: ${API_CONFIG.UPLOAD.ALLOWED_TYPES.join(', ')}`);
    }

    // Check MIME type
    if (!API_CONFIG.UPLOAD.ALLOWED_MIME_TYPES.includes(file.type)) {
      errors.push(`File MIME type (${file.type}) is not supported`);
    }

    return {
      isValid: errors.length === 0,
      errors: errors
    };
  }

  // Retry function with exponential backoff
  async retryRequest(requestFn, maxAttempts = API_CONFIG.RETRY.MAX_ATTEMPTS) {
    let lastError;
    
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return await requestFn();
      } catch (error) {
        lastError = error;
        
        if (attempt === maxAttempts) {
          throw error;
        }
        
        // Wait before retrying (exponential backoff)
        const delay = API_CONFIG.RETRY.DELAY * Math.pow(2, attempt - 1);
        await new Promise(resolve => setTimeout(resolve, delay));
        
        console.log(`Retry attempt ${attempt}/${maxAttempts} after ${delay}ms delay`);
      }
    }
    
    throw lastError;
  }
}

// Create singleton instance
const apiService = new ApiService();

export default apiService;
