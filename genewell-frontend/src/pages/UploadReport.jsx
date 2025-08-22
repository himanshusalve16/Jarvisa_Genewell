import React, { useState } from 'react';
import axios from 'axios';

const UploadReport = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Check file type
      const allowedTypes = ['.vcf', '.fastq'];
      const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (allowedTypes.includes(fileExtension)) {
        setSelectedFile(file);
        setUploadStatus('');
      } else {
        setUploadStatus('Please select a valid .vcf or .fastq file');
        setSelectedFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a file first');
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    setUploadStatus('');

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      // Mock API call
      const formData = new FormData();
      formData.append('file', selectedFile);

      // Simulate API call with timeout
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Mock response
      const mockResponse = {
        data: {
          success: true,
          message: 'File uploaded successfully',
          fileId: 'gw_' + Math.random().toString(36).substr(2, 9),
          fileName: selectedFile.name,
          fileSize: selectedFile.size,
          estimatedProcessingTime: '5-10 minutes'
        }
      };

      clearInterval(progressInterval);
      setUploadProgress(100);
      setUploadStatus('Upload successful! Your genomic data is being processed.');
      
      // Reset after success
      setTimeout(() => {
        setSelectedFile(null);
        setUploadProgress(0);
        setIsUploading(false);
      }, 3000);

    } catch (error) {
      setUploadStatus('Upload failed. Please try again.');
      setUploadProgress(0);
      setIsUploading(false);
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
            Upload your .vcf or .fastq files to get personalized AI-powered genomic insights 
            and risk assessments within minutes.
          </p>
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
              Supported formats: .vcf, .fastq (Max size: 500MB)
            </p>
          </div>

          {/* File Upload Area */}
          <div className="mb-6">
            <label className="block">
              <input
                type="file"
                accept=".vcf,.fastq"
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
                    <p className="text-healthcare-500 text-sm">VCF or FASTQ files only</p>
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
