import React from 'react';
import { Link } from 'react-router-dom';

const Hero = () => {
  return (
    <section className="gradient-bg py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left side - DNA Animation */}
          <div className="flex justify-center lg:justify-start">
            <div className="relative w-64 h-64 lg:w-80 lg:h-80">
              {/* DNA Strand Animation */}
              <div className="dna-strand absolute inset-0">
                <svg viewBox="0 0 200 200" className="w-full h-full">
                  {/* DNA Double Helix */}
                  <defs>
                    <linearGradient id="dnaGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stopColor="#0ea5e9" />
                      <stop offset="50%" stopColor="#d946ef" />
                      <stop offset="100%" stopColor="#0ea5e9" />
                    </linearGradient>
                  </defs>
                  
                  {/* Left helix */}
                  <path
                    d="M50 20 Q70 50 50 80 Q30 110 50 140 Q70 170 50 200"
                    stroke="url(#dnaGradient)"
                    strokeWidth="3"
                    fill="none"
                    className="helix-line"
                  />
                  
                  {/* Right helix */}
                  <path
                    d="M150 20 Q130 50 150 80 Q170 110 150 140 Q130 170 150 200"
                    stroke="url(#dnaGradient)"
                    strokeWidth="3"
                    fill="none"
                    className="helix-line"
                  />
                  
                  {/* Base pairs */}
                  {[30, 50, 70, 90, 110, 130, 150, 170].map((y, index) => (
                    <g key={index}>
                      <line
                        x1={50 + Math.sin((y - 20) * 0.1) * 20}
                        y1={y}
                        x2={150 - Math.sin((y - 20) * 0.1) * 20}
                        y2={y}
                        stroke="#64748b"
                        strokeWidth="2"
                        opacity="0.7"
                      />
                      <circle
                        cx={50 + Math.sin((y - 20) * 0.1) * 20}
                        cy={y}
                        r="3"
                        fill="#0ea5e9"
                      />
                      <circle
                        cx={150 - Math.sin((y - 20) * 0.1) * 20}
                        cy={y}
                        r="3"
                        fill="#d946ef"
                      />
                    </g>
                  ))}
                </svg>
              </div>
              
              {/* Floating particles */}
              <div className="absolute inset-0 overflow-hidden">
                {[...Array(6)].map((_, i) => (
                  <div
                    key={i}
                    className={`absolute w-2 h-2 bg-primary-400 rounded-full animate-pulse-slow`}
                    style={{
                      left: `${20 + i * 15}%`,
                      top: `${10 + (i % 3) * 30}%`,
                      animationDelay: `${i * 0.5}s`
                    }}
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Right side - Content */}
          <div className="text-center lg:text-left">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-healthcare-900 mb-6">
              Unlock Your
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-primary-600 to-accent-600">
                Genetic Potential
              </span>
            </h1>
            
            <p className="text-xl text-healthcare-600 mb-8 leading-relaxed">
              Genewell harnesses the power of AI to analyze your genomic data, 
              providing personalized health insights and risk assessments to help 
              you make informed decisions about your future.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Link to="/upload" className="btn-primary inline-flex items-center justify-center">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                Upload Report
              </Link>
              
              <Link to="/risk-score" className="btn-secondary inline-flex items-center justify-center">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                View Risk Score
              </Link>
            </div>
            
            <div className="mt-12 grid grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-2xl font-bold text-primary-600">10K+</div>
                <div className="text-sm text-healthcare-600">Reports Analyzed</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-primary-600">99.9%</div>
                <div className="text-sm text-healthcare-600">Accuracy Rate</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-primary-600">24/7</div>
                <div className="text-sm text-healthcare-600">AI Support</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
