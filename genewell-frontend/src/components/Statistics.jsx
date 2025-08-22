import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Statistics = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        setLoading(true);
        const response = await axios.get('https://api-ab7f7fe4-2146-4794-b8bd-364d138db73c.com/statistics');
        setStats(response.data);
        setError(null);
      } catch (err) {
        setError('Failed to load statistics data');
        console.error('Error fetching statistics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStatistics();
  }, []);

  if (loading) {
    return (
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-primary-50 to-accent-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-healthcare-600">Loading statistics...</p>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-primary-50 to-accent-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center">
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-red-600">{error}</p>
          </div>
        </div>
      </section>
    );
  }

  // Default mock data structure if API doesn't return expected format
  const defaultStats = {
    totalAnalyses: 15420,
    activeUsers: 8750,
    accuracyRate: 99.7,
    avgProcessingTime: 2.3,
    topConditions: [
      { name: 'Cardiovascular Risk', count: 3420 },
      { name: 'Diabetes Susceptibility', count: 2890 },
      { name: 'Cancer Predisposition', count: 2150 }
    ],
    monthlyGrowth: 23.5
  };

  const displayStats = stats || defaultStats;

  const statCards = [
    {
      title: 'Total Analyses',
      value: displayStats.totalAnalyses?.toLocaleString() || '15,420',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      gradient: 'from-blue-500 to-blue-600'
    },
    {
      title: 'Active Users',
      value: displayStats.activeUsers?.toLocaleString() || '8,750',
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
        </svg>
      ),
      gradient: 'from-green-500 to-green-600'
    },
    {
      title: 'Accuracy Rate',
      value: `${displayStats.accuracyRate || 99.7}%`,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      gradient: 'from-purple-500 to-purple-600'
    },
    {
      title: 'Avg Processing Time',
      value: `${displayStats.avgProcessingTime || 2.3}min`,
      icon: (
        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
      gradient: 'from-orange-500 to-orange-600'
    }
  ];

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-primary-50 to-accent-50">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-healthcare-900 mb-4">
            Platform Statistics
          </h2>
          <p className="text-xl text-healthcare-600 max-w-3xl mx-auto">
            Real-time insights into our genomic analysis platform performance and user engagement
          </p>
        </div>

        {/* Main Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {statCards.map((stat, index) => (
            <div key={index} className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 bg-gradient-to-r ${stat.gradient} rounded-lg flex items-center justify-center text-white`}>
                  {stat.icon}
                </div>
                <div className="text-right">
                  <div className="text-2xl font-bold text-healthcare-900">{stat.value}</div>
                  <div className="text-sm text-healthcare-600">{stat.title}</div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Additional Statistics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Top Analyzed Conditions */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-semibold text-healthcare-900 mb-6 flex items-center">
              <svg className="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              Top Analyzed Conditions
            </h3>
            <div className="space-y-4">
              {(displayStats.topConditions || defaultStats.topConditions).map((condition, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full mr-3 ${
                      index === 0 ? 'bg-primary-500' : 
                      index === 1 ? 'bg-accent-500' : 'bg-healthcare-400'
                    }`}></div>
                    <span className="text-healthcare-700">{condition.name}</span>
                  </div>
                  <span className="font-semibold text-healthcare-900">{condition.count.toLocaleString()}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Growth Metrics */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-xl font-semibold text-healthcare-900 mb-6 flex items-center">
              <svg className="w-6 h-6 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 11l5-5m0 0l5 5m-5-5v12" />
              </svg>
              Growth Metrics
            </h3>
            <div className="space-y-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  +{displayStats.monthlyGrowth || 23.5}%
                </div>
                <div className="text-healthcare-600">Monthly User Growth</div>
              </div>
              <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-4">
                <div className="text-sm text-healthcare-600 mb-2">Platform Reliability</div>
                <div className="flex items-center">
                  <div className="flex-1 bg-healthcare-200 rounded-full h-2 mr-3">
                    <div className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full" style={{width: '99.7%'}}></div>
                  </div>
                  <span className="text-sm font-semibold text-healthcare-900">99.7%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center mt-12">
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h3 className="text-2xl font-bold text-healthcare-900 mb-4">
              Join Our Growing Community
            </h3>
            <p className="text-healthcare-600 mb-6 max-w-2xl mx-auto">
              Be part of the genomic revolution. Upload your report today and discover personalized health insights backed by cutting-edge AI technology.
            </p>
            <button className="btn-primary">
              Get Your Analysis
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Statistics;
