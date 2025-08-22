/**
 * GeneWell ML API Integration Example
 * This file shows how to integrate the ML backend with your React frontend
 */

// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// API Service Class
class GeneWellAPI {
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
    }

    // Health check
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            return await response.json();
        } catch (error) {
            console.error('Health check failed:', error);
            throw error;
        }
    }

    // Get model information
    async getModelInfo() {
        try {
            const response = await fetch(`${this.baseURL}/model-info`);
            return await response.json();
        } catch (error) {
            console.error('Failed to get model info:', error);
            throw error;
        }
    }

    // Download sample data
    async downloadSampleData() {
        try {
            const response = await fetch(`${this.baseURL}/sample-data`);
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'sample_gene_data.csv';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            console.error('Failed to download sample data:', error);
            throw error;
        }
    }

    // Upload CSV file and get predictions
    async predictFromFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${this.baseURL}/predict`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Prediction failed:', error);
            throw error;
        }
    }

    // Batch prediction from JSON data
    async predictBatch(patients) {
        try {
            const response = await fetch(`${this.baseURL}/predict-batch`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ patients })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Batch prediction failed:', error);
            throw error;
        }
    }

    // Export report
    async exportReport(results) {
        try {
            const response = await fetch(`${this.baseURL}/export-report`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ results })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Report export failed:', error);
            throw error;
        }
    }
}

// React Hook for API Integration
export const useGeneWellAPI = () => {
    const api = new GeneWellAPI();

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const executeAPI = async (apiCall) => {
        setLoading(true);
        setError(null);
        try {
            const result = await apiCall();
            return result;
        } catch (err) {
            setError(err.message);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return {
        api,
        loading,
        error,
        executeAPI
    };
};

// Example React Components

// Health Check Component
export const HealthCheck = () => {
    const { api, loading, error, executeAPI } = useGeneWellAPI();
    const [health, setHealth] = useState(null);

    const checkHealth = async () => {
        try {
            const result = await executeAPI(() => api.checkHealth());
            setHealth(result);
        } catch (err) {
            console.error('Health check failed:', err);
        }
    };

    useEffect(() => {
        checkHealth();
    }, []);

    if (loading) return <div>Checking API health...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className="health-check">
            <h3>API Health Status</h3>
            {health && (
                <div>
                    <p>Status: {health.status}</p>
                    <p>Model Loaded: {health.model_loaded ? 'Yes' : 'No'}</p>
                    <p>Timestamp: {new Date(health.timestamp).toLocaleString()}</p>
                </div>
            )}
        </div>
    );
};

// File Upload Component
export const FileUpload = ({ onPredictions }) => {
    const { api, loading, error, executeAPI } = useGeneWellAPI();
    const [file, setFile] = useState(null);

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (selectedFile && selectedFile.type === 'text/csv') {
            setFile(selectedFile);
        } else {
            alert('Please select a valid CSV file');
        }
    };

    const handleUpload = async () => {
        if (!file) {
            alert('Please select a file first');
            return;
        }

        try {
            const result = await executeAPI(() => api.predictFromFile(file));
            onPredictions(result.results);
        } catch (err) {
            console.error('Upload failed:', err);
        }
    };

    const downloadSample = async () => {
        try {
            await executeAPI(() => api.downloadSampleData());
        } catch (err) {
            console.error('Download failed:', err);
        }
    };

    return (
        <div className="file-upload">
            <h3>Upload Gene Report</h3>
            
            <div className="upload-section">
                <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    disabled={loading}
                />
                <button onClick={handleUpload} disabled={!file || loading}>
                    {loading ? 'Processing...' : 'Upload & Predict'}
                </button>
            </div>

            <div className="sample-section">
                <p>Don't have a file? Download a sample:</p>
                <button onClick={downloadSample} disabled={loading}>
                    Download Sample Data
                </button>
            </div>

            {error && <div className="error">Error: {error}</div>}
        </div>
    );
};

// Results Display Component
export const ResultsDisplay = ({ results }) => {
    if (!results || results.length === 0) {
        return <div>No results to display</div>;
    }

    return (
        <div className="results-display">
            <h3>Prediction Results</h3>
            
            {results.map((result, index) => (
                <div key={index} className="patient-result">
                    <h4>Patient: {result.patient_id}</h4>
                    <p>Health Status: <span className={`status-${result.health_status.toLowerCase().replace(' ', '-')}`}>
                        {result.health_status}
                    </span></p>
                    
                    {result.risk_factors.length > 0 && (
                        <div className="risk-factors">
                            <h5>Risk Factors:</h5>
                            <ul>
                                {result.risk_factors.map((factor, i) => (
                                    <li key={i}>{factor}</li>
                                ))}
                            </ul>
                        </div>
                    )}

                    <div className="predictions">
                        <h5>Disease Predictions:</h5>
                        <div className="disease-grid">
                            {Object.entries(result.predictions)
                                .sort(([,a], [,b]) => b.probability - a.probability)
                                .slice(0, 5)
                                .map(([disease, info]) => (
                                    <div key={disease} className="disease-item">
                                        <span className="disease-name">{disease}</span>
                                        <span className={`probability ${info.probability > 0.7 ? 'high-risk' : info.probability > 0.4 ? 'moderate-risk' : 'low-risk'}`}>
                                            {(info.probability * 100).toFixed(1)}%
                                        </span>
                                        <span className="predicted">{info.predicted ? 'Yes' : 'No'}</span>
                                    </div>
                                ))}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

// Main App Component Example
export const GeneWellApp = () => {
    const [predictions, setPredictions] = useState(null);

    return (
        <div className="genewell-app">
            <header>
                <h1>GeneWell Disease Prediction</h1>
                <HealthCheck />
            </header>

            <main>
                <FileUpload onPredictions={setPredictions} />
                {predictions && <ResultsDisplay results={predictions} />}
            </main>
        </div>
    );
};

// CSS Styles (you can add this to your CSS file)
const styles = `
.genewell-app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.health-check {
    background: #f5f5f5;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
}

.file-upload {
    background: white;
    padding: 20px;
    border: 2px dashed #ccc;
    border-radius: 8px;
    margin-bottom: 20px;
}

.upload-section {
    margin-bottom: 15px;
}

.upload-section button {
    margin-left: 10px;
    padding: 8px 16px;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.upload-section button:disabled {
    background: #ccc;
    cursor: not-allowed;
}

.sample-section {
    border-top: 1px solid #eee;
    padding-top: 15px;
}

.sample-section button {
    padding: 6px 12px;
    background: #28a745;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.error {
    color: #dc3545;
    margin-top: 10px;
    padding: 10px;
    background: #f8d7da;
    border-radius: 4px;
}

.results-display {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.patient-result {
    border: 1px solid #eee;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 6px;
}

.status-normal { color: #28a745; font-weight: bold; }
.status-at-risk { color: #ffc107; font-weight: bold; }
.status-high-risk { color: #dc3545; font-weight: bold; }

.risk-factors ul {
    margin: 5px 0;
    padding-left: 20px;
}

.disease-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 10px;
    margin-top: 10px;
}

.disease-item {
    display: contents;
}

.disease-name {
    font-weight: 500;
}

.probability {
    text-align: center;
    font-weight: bold;
}

.probability.high-risk { color: #dc3545; }
.probability.moderate-risk { color: #ffc107; }
.probability.low-risk { color: #28a745; }

.predicted {
    text-align: center;
    font-weight: bold;
}
`;

// Export the API class for direct use
export default GeneWellAPI;
