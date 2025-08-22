import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import axios from 'axios';

const RiskScore = () => {
  const [riskData, setRiskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Mock data for genomic risk scores
  const mockRiskData = {
    overallScore: 72,
    categories: [
      { name: 'Cardiovascular', risk: 68, color: '#ef4444', status: 'moderate' },
      { name: 'Diabetes', risk: 45, color: '#f59e0b', status: 'low' },
      { name: 'Cancer', risk: 82, color: '#dc2626', status: 'high' },
      { name: 'Alzheimer\'s', risk: 35, color: '#10b981', status: 'low' },
      { name: 'Obesity', risk: 58, color: '#f59e0b', status: 'moderate' },
      { name: 'Mental Health', risk: 41, color: '#10b981', status: 'low' }
    ],
    detailedMetrics: [
      { condition: 'Heart Disease', risk: 68, population: 45, variants: 12 },
      { condition: 'Type 2 Diabetes', risk: 45, population: 38, variants: 8 },
      { condition: 'Breast Cancer', risk: 82, population: 12, variants: 15 },
      { condition: 'Colorectal Cancer', risk: 55, population: 25, variants: 7 },
      { condition: 'Alzheimer\'s Disease', risk: 35, population: 28, variants: 5 },
      { condition: 'Depression', risk: 41, population: 35, variants: 9 }
    ]
  };

  useEffect(() => {
    // Simulate API call to fetch risk scores
    const fetchRiskData = async () => {
      setLoading(true);
      try {
        // Mock API call
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // In a real app, this would be:
        // const response = await axios.get('/api/risk-score');
        // setRiskData(response.data);
        
        setRiskData(mockRiskData);
      } catch (error) {
        console.error('Error fetching risk data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRiskData();
  }, []);

  const getRiskLevel = (score) => {
    if (score >= 70) return { level: 'High', color: 'text-red-600', bg: 'bg-red-50' };
    if (score >= 50) return { level: 'Moderate', color: 'text-yellow-600', bg: 'bg-yellow-50' };
    return { level: 'Low', color: 'text-green-600', bg: 'bg-green-50' };
  };

  const getScoreColor = (score) => {
    if (score >= 70) return '#dc2626';
    if (score >= 50) return '#f59e0b';
    return '#10b981';
  };

  if (loading) {
    return (
      <div className="min-h-screen gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-healthcare-600 text-lg">Analyzing your genomic data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen gradient-bg py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-healthcare-900 mb-4">
            Your Genomic Risk Assessment
          </h1>
          <p className="text-xl text-healthcare-600 max-w-3xl mx-auto">
            AI-powered analysis of your genetic variants to assess disease risks and provide 
            personalized health insights based on current genomic research.
          </p>
        </div>

        {/* Overall Score Card */}
        <div className="card mb-8 text-center">
          <h2 className="text-2xl font-semibold text-healthcare-800 mb-6">Overall Risk Score</h2>
          <div className="flex items-center justify-center space-x-8">
            <div className="relative w-32 h-32">
              <svg className="w-32 h-32 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke="#e5e7eb"
                  strokeWidth="3"
                />
                <path
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  fill="none"
                  stroke={getScoreColor(riskData.overallScore)}
                  strokeWidth="3"
                  strokeDasharray={`${riskData.overallScore}, 100`}
                  strokeLinecap="round"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-3xl font-bold text-healthcare-800">{riskData.overallScore}</span>
              </div>
            </div>
            <div className="text-left">
              <div className={`inline-block px-4 py-2 rounded-full text-sm font-medium ${getRiskLevel(riskData.overallScore).bg} ${getRiskLevel(riskData.overallScore).color}`}>
                {getRiskLevel(riskData.overallScore).level} Risk
              </div>
              <p className="text-healthcare-600 mt-2 max-w-md">
                Your overall genetic risk score is based on analysis of multiple health conditions 
                and genetic variants compared to the general population.
              </p>
            </div>
          </div>
        </div>

        {/* Risk Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {riskData.categories.map((category, index) => (
            <div key={index} className="card hover:shadow-xl transition-shadow">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-healthcare-800">{category.name}</h3>
                <div className={`px-3 py-1 rounded-full text-xs font-medium ${getRiskLevel(category.risk).bg} ${getRiskLevel(category.risk).color}`}>
                  {getRiskLevel(category.risk).level}
                </div>
              </div>
              <div className="mb-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-healthcare-600">Risk Score</span>
                  <span className="text-lg font-bold text-healthcare-800">{category.risk}%</span>
                </div>
                <div className="w-full bg-healthcare-200 rounded-full h-2">
                  <div 
                    className="h-2 rounded-full transition-all duration-500"
                    style={{ 
                      width: `${category.risk}%`,
                      backgroundColor: category.color
                    }}
                  ></div>
                </div>
              </div>
              <p className="text-sm text-healthcare-600">
                Based on {Math.floor(Math.random() * 20) + 5} genetic variants associated with {category.name.toLowerCase()}.
              </p>
            </div>
          ))}
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Bar Chart */}
          <div className="card">
            <h3 className="text-xl font-semibold text-healthcare-800 mb-6">Risk Comparison</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={riskData.detailedMetrics}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="condition" 
                  angle={-45}
                  textAnchor="end"
                  height={100}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => [`${value}%`, name === 'risk' ? 'Your Risk' : 'Population Average']}
                />
                <Bar dataKey="risk" fill="#0ea5e9" name="Your Risk" />
                <Bar dataKey="population" fill="#94a3b8" name="Population Average" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Pie Chart */}
          <div className="card">
            <h3 className="text-xl font-semibold text-healthcare-800 mb-6">Risk Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={riskData.categories}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, risk }) => `${name}: ${risk}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="risk"
                >
                  {riskData.categories.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`${value}%`, 'Risk Score']} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Detailed Metrics Table */}
        <div className="card">
          <h3 className="text-xl font-semibold text-healthcare-800 mb-6">Detailed Risk Analysis</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-healthcare-200">
                  <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Condition</th>
                  <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Your Risk</th>
                  <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Population Avg</th>
                  <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Variants</th>
                  <th className="text-left py-3 px-4 font-semibold text-healthcare-800">Status</th>
                </tr>
              </thead>
              <tbody>
                {riskData.detailedMetrics.map((metric, index) => (
                  <tr key={index} className="border-b border-healthcare-100 hover:bg-healthcare-50">
                    <td className="py-3 px-4 font-medium text-healthcare-800">{metric.condition}</td>
                    <td className="py-3 px-4">
                      <span className={`font-semibold ${getRiskLevel(metric.risk).color}`}>
                        {metric.risk}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-healthcare-600">{metric.population}%</td>
                    <td className="py-3 px-4 text-healthcare-600">{metric.variants}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskLevel(metric.risk).bg} ${getRiskLevel(metric.risk).color}`}>
                        {getRiskLevel(metric.risk).level}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Recommendations */}
        <div className="card mt-8">
          <h3 className="text-xl font-semibold text-healthcare-800 mb-6">Personalized Recommendations</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-2">Lifestyle Modifications</h4>
              <ul className="text-blue-700 text-sm space-y-1">
                <li>• Regular cardiovascular exercise (150 min/week)</li>
                <li>• Mediterranean diet with omega-3 rich foods</li>
                <li>• Stress management and adequate sleep</li>
                <li>• Limit alcohol consumption</li>
              </ul>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <h4 className="font-semibold text-green-800 mb-2">Screening Recommendations</h4>
              <ul className="text-green-700 text-sm space-y-1">
                <li>• Annual cardiovascular screening</li>
                <li>• Enhanced cancer screening protocols</li>
                <li>• Regular blood glucose monitoring</li>
                <li>• Consult with genetic counselor</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};


export default RiskScore;
