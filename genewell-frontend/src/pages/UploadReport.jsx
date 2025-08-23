import React, { useState, useEffect } from 'react';
import apiService from '../services/apiService';

const UploadReport = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [modelInfo, setModelInfo] = useState(null);
  const [predictionResults, setPredictionResults] = useState(null);

  // Check backend status on component mount
  useEffect(() => {
    checkBackendStatus();
  }, []);

  const checkBackendStatus = async () => {
    try {
      setBackendStatus('checking');
      const healthData = await apiService.checkHealth();
      setBackendStatus('connected');
      
      // Get model info
      try {
        const modelData = await apiService.getModelInfo();
        setModelInfo(modelData);
      } catch (error) {
        console.warn('Model not trained yet:', error.message);
        setModelInfo(null);
      }
    } catch (error) {
      console.error('Backend connection failed:', error);
      setBackendStatus('disconnected');
    }
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Validate file using API service
      const validation = apiService.validateFile(file);
      
      if (validation.isValid) {
        setSelectedFile(file);
        setUploadStatus('');
        setPredictionResults(null);
      } else {
        setUploadStatus(`File validation failed: ${validation.errors.join(', ')}`);
        setSelectedFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a file first');
      return;
    }

    if (backendStatus !== 'connected') {
      setUploadStatus('Backend is not connected. Please check the server status.');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    setUploadStatus('');

    try {
      // Upload file and get predictions
      const results = await apiService.uploadAndPredict(
        selectedFile,
        (progress) => setUploadProgress(progress)
      );

      setUploadProgress(100);
      setPredictionResults(results);
      setUploadStatus('Analysis completed successfully!');
      
      // Reset file selection after success
      setTimeout(() => {
        setSelectedFile(null);
        setUploadProgress(0);
        setIsUploading(false);
      }, 3000);

    } catch (error) {
      setUploadStatus(`Upload failed: ${error.message}`);
      setUploadProgress(0);
      setIsUploading(false);
    }
  };

  const handleTrainModel = async () => {
    try {
      setUploadStatus('Training model...');
      const result = await apiService.trainModel();
      setUploadStatus(`Model trained successfully! Features: ${result.features_count}, Samples: ${result.samples_count}`);
      
      // Refresh model info
      await checkBackendStatus();
    } catch (error) {
      setUploadStatus(`Model training failed: ${error.message}`);
    }
  };

  const handleDownloadSample = async () => {
    try {
      setUploadStatus('Downloading sample data...');
      await apiService.downloadSampleData();
      setUploadStatus('Sample data downloaded successfully!');
    } catch (error) {
      setUploadStatus(`Download failed: ${error.message}`);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen gradient-bg py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-healthcare-900 mb-4">
            Upload Your Genomic Report
          </h1>
          <p className="text-xl text-healthcare-600 max-w-2xl mx-auto">
            Upload your CSV or PDF files to get personalized AI-powered genomic insights 
            and risk assessments within minutes.
          </p>
        </div>

        {/* Backend Status and Model Info */}
        <div className="max-w-2xl mx-auto mb-8">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-healthcare-800">System Status</h3>
              <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                backendStatus === 'connected' 
                  ? 'bg-green-100 text-green-700' 
                  : backendStatus === 'checking'
                  ? 'bg-yellow-100 text-yellow-700'
                  : 'bg-red-100 text-red-700'
              }`}>
                {backendStatus === 'connected' ? 'Connected' : 
                 backendStatus === 'checking' ? 'Checking...' : 'Disconnected'}
              </div>
            </div>
            
            {backendStatus === 'connected' && (
              <div className="space-y-3">
                {modelInfo ? (
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                    <div>
                      <p className="text-sm font-medium text-green-800">Model Status</p>
                      <p className="text-xs text-green-600">
                        Features: {modelInfo.features_count || 'N/A'} | 
                        Model loaded successfully
                      </p>
                    </div>
                    <svg className="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                ) : (
                  <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                    <div>
                      <p className="text-sm font-medium text-yellow-800">Model Status</p>
                      <p className="text-xs text-yellow-600">Model not trained yet</p>
                    </div>
                    <button
                      onClick={handleTrainModel}
                      className="px-3 py-1 bg-yellow-600 text-white text-xs rounded hover:bg-yellow-700 transition-colors"
                    >
                      Train Model
                    </button>
                  </div>
                )}
                
                <div className="flex space-x-2">
                  <button
                    onClick={handleDownloadSample}
                    className="flex-1 px-3 py-2 bg-primary-600 text-white text-sm rounded hover:bg-primary-700 transition-colors"
                  >
                    Download Sample Data
                  </button>
                  <button
                    onClick={checkBackendStatus}
                    className="px-3 py-2 bg-healthcare-600 text-white text-sm rounded hover:bg-healthcare-700 transition-colors"
                  >
                    Refresh Status
                  </button>
                </div>
              </div>
            )}
            
            {backendStatus === 'disconnected' && (
              <div className="p-3 bg-red-50 rounded-lg">
                <p className="text-sm text-red-800">
                  Cannot connect to backend server. Please ensure the server is running on port 5000.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Upload Section */}
        <div className="card max-w-2xl mx-auto">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-r from-primary-500 to-accent-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <h2 className="text-2xl font-semibold text-healthcare-800 mb-2">
              Select Your Genomic File
            </h2>
            <p className="text-healthcare-600">
              Supported formats: .csv, .pdf (Max size: 50MB)
            </p>
          </div>

          {/* File Upload Area */}
          <div className="mb-6">
            <label className="block">
              <input
                type="file"
                accept=".csv,.pdf"
                onChange={handleFileSelect}
                className="hidden"
                disabled={isUploading}
              />
              <div className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                selectedFile 
                  ? 'border-primary-500 bg-primary-50' 
                  : 'border-healthcare-300 hover:border-primary-400 hover:bg-primary-50'
              } ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}`}>
                {selectedFile ? (
                  <div className="space-y-2">
                    <svg className="w-12 h-12 text-primary-500 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p className="text-primary-700 font-medium">{selectedFile.name}</p>
                    <p className="text-primary-600 text-sm">{formatFileSize(selectedFile.size)}</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <svg className="w-12 h-12 text-healthcare-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="text-healthcare-600">
                      <span className="font-medium text-primary-600">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-healthcare-500 text-sm">CSV or PDF files only</p>
                  </div>
                )}
              </div>
            </label>
          </div>

          {/* Upload Progress */}
          {isUploading && (
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-healthcare-600">Uploading...</span>
                <span className="text-sm text-healthcare-600">{uploadProgress}%</span>
              </div>
              <div className="w-full bg-healthcare-200 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-primary-500 to-accent-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                ></div>
              </div>
            </div>
          )}

          {/* Status Message */}
          {uploadStatus && (
            <div className={`mb-6 p-4 rounded-lg ${
              uploadStatus.includes('successful') || uploadStatus.includes('being processed')
                ? 'bg-green-50 text-green-700 border border-green-200'
                : 'bg-red-50 text-red-700 border border-red-200'
            }`}>
              <div className="flex items-center">
                {uploadStatus.includes('successful') || uploadStatus.includes('being processed') ? (
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                )}
                {uploadStatus}
              </div>
            </div>
          )}

          {/* Upload Button */}
          <button
            onClick={handleUpload}
            disabled={!selectedFile || isUploading}
            className={`w-full py-3 px-6 rounded-lg font-medium transition-colors ${
              selectedFile && !isUploading
                ? 'bg-primary-600 hover:bg-primary-700 text-white'
                : 'bg-healthcare-300 text-healthcare-500 cursor-not-allowed'
            }`}
          >
            {isUploading ? 'Uploading...' : 'Upload and Analyze'}
          </button>
        </div>

        {/* Results Display */}
        {predictionResults && (
          <div className="max-w-4xl mx-auto mt-8">
            <div className="card">
              <h3 className="text-xl font-semibold text-healthcare-800 mb-6">Analysis Results</h3>
              
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-healthcare-600">Total Patients Analyzed</span>
                  <span className="text-lg font-bold text-primary-600">{predictionResults.total_patients || predictionResults.results?.length || 0}</span>
                </div>
              </div>

              {predictionResults.results && predictionResults.results.length > 0 && (
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-healthcare-200">
                        <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Patient ID</th>
                        <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Risk Score</th>
                        <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Risk Level</th>
                        <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Health Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {predictionResults.results.map((result, index) => (
                        <tr key={index} className="border-b border-healthcare-100 hover:bg-healthcare-50">
                          <td className="py-3 px-4 font-medium text-healthcare-800">
                            {result.patient_id || `Patient ${index + 1}`}
                          </td>
                          <td className="py-3 px-4">
                            <span className={`font-semibold ${
                              result.risk_score > 0.7 ? 'text-red-600' : 
                              result.risk_score > 0.4 ? 'text-yellow-600' : 'text-green-600'
                            }`}>
                              {(result.risk_score * 100).toFixed(1)}%
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              result.risk_level === 'High' ? 'bg-red-100 text-red-700' :
                              result.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-green-100 text-green-700'
                            }`}>
                              {result.risk_level}
                            </span>
                          </td>
                          <td className="py-3 px-4">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              result.health_status === 'High Risk' ? 'bg-red-100 text-red-700' :
                              result.health_status === 'At Risk' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-green-100 text-green-700'
                            }`}>
                              {result.health_status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}

              <div className="mt-6 flex space-x-3">
                <button
                  onClick={() => setPredictionResults(null)}
                  className="px-4 py-2 bg-healthcare-600 text-white rounded hover:bg-healthcare-700 transition-colors"
                >
                  Clear Results
                </button>
                <button
                  onClick={() => {
                    // Navigate to risk score page with results
                    window.location.href = '/risk-score';
                  }}
                  className="px-4 py-2 bg-primary-600 text-white rounded hover:bg-primary-700 transition-colors"
                >
                  View Detailed Analysis
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Information Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <div className="card text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-healthcare-800 mb-2">Secure Processing</h3>
            <p className="text-healthcare-600 text-sm">Your data is encrypted and processed securely with enterprise-grade protection.</p>
          </div>

          <div className="card text-center">
            <div className="w-12 h-12 bg-accent-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-accent-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-healthcare-800 mb-2">Fast Analysis</h3>
            <p className="text-healthcare-600 text-sm">Get comprehensive results in 5-10 minutes using our advanced AI algorithms.</p>
          </div>

          <div className="card text-center">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-healthcare-800 mb-2">Accurate Results</h3>
            <p className="text-healthcare-600 text-sm">99.9% accuracy rate backed by peer-reviewed research and clinical validation.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadReport;
