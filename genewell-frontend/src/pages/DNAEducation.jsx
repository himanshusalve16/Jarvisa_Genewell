import React from 'react';

const DNAEducation = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-green-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Understanding DNA Analysis
            </h1>
            <p className="text-xl md:text-2xl max-w-3xl mx-auto">
              Learn how genetic information is decoded to provide insights into your health and ancestry
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        
        {/* What is DNA Section */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">What is DNA?</h2>
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <p className="text-lg text-gray-700 mb-6">
                DNA (Deoxyribonucleic Acid) is the hereditary material in humans and almost all other organisms. 
                It contains the instructions needed to develop, live and reproduce.
              </p>
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-xl font-semibold text-blue-600 mb-4">Key Facts:</h3>
                <ul className="space-y-2 text-gray-700">
                  <li>• DNA is made up of four chemical bases: A, T, G, C</li>
                  <li>• Human DNA consists of about 3 billion base pairs</li>
                  <li>• 99.9% of DNA is identical between all humans</li>
                  <li>• The 0.1% difference makes each person unique</li>
                </ul>
              </div>
            </div>
            <div className="bg-white p-8 rounded-lg shadow-lg">
              <div className="text-center">
                <div className="text-6xl mb-4">🧬</div>
                <h3 className="text-2xl font-bold text-gray-800 mb-4">DNA Double Helix</h3>
                <p className="text-gray-600">
                  The iconic twisted ladder structure discovered by Watson and Crick
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* How DNA Analysis Works */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">How DNA Analysis Works</h2>
          <div className="grid md:grid-cols-3 gap-8">
            
            {/* Step 1 */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-center mb-4">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-blue-600">1</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-800">Sample Collection</h3>
              </div>
              <p className="text-gray-700">
                DNA is extracted from saliva, blood, or tissue samples. The sample is processed to isolate 
                the genetic material from other cellular components.
              </p>
            </div>

            {/* Step 2 */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-center mb-4">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-green-600">2</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-800">Sequencing</h3>
              </div>
              <p className="text-gray-700">
                Advanced sequencing machines read the DNA code, determining the order of the four bases 
                (A, T, G, C) across the genome.
              </p>
            </div>

            {/* Step 3 */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-center mb-4">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-2xl font-bold text-purple-600">3</span>
                </div>
                <h3 className="text-xl font-semibold text-gray-800">Analysis</h3>
              </div>
              <p className="text-gray-700">
                Sophisticated algorithms compare your DNA to reference databases to identify variants 
                and their potential health implications.
              </p>
            </div>
          </div>
        </section>

        {/* Types of Genetic Variants */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Types of Genetic Variants</h2>
          <div className="grid md:grid-cols-2 gap-8">
            
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold text-blue-600 mb-4">Single Nucleotide Polymorphisms (SNPs)</h3>
              <p className="text-gray-700 mb-4">
                The most common type of genetic variation, where a single DNA building block differs 
                between individuals.
              </p>
              <div className="bg-gray-50 p-4 rounded">
                <p className="text-sm text-gray-600">
                  <strong>Example:</strong> Where most people have the sequence "AAGCCTA", 
                  you might have "AAGCTTA" (C→T change)
                </p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold text-green-600 mb-4">Copy Number Variations (CNVs)</h3>
              <p className="text-gray-700 mb-4">
                Segments of DNA that are repeated a different number of times in different people.
              </p>
              <div className="bg-gray-50 p-4 rounded">
                <p className="text-sm text-gray-600">
                  <strong>Impact:</strong> Can affect gene dosage and protein production levels
                </p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold text-purple-600 mb-4">Insertions/Deletions (Indels)</h3>
              <p className="text-gray-700 mb-4">
                Small insertions or deletions of DNA sequences that can shift the reading frame.
              </p>
              <div className="bg-gray-50 p-4 rounded">
                <p className="text-sm text-gray-600">
                  <strong>Effect:</strong> Can cause frameshift mutations affecting protein function
                </p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <h3 className="text-xl font-semibold text-red-600 mb-4">Structural Variants</h3>
              <p className="text-gray-700 mb-4">
                Large-scale changes including inversions, translocations, and large deletions.
              </p>
              <div className="bg-gray-50 p-4 rounded">
                <p className="text-sm text-gray-600">
                  <strong>Significance:</strong> Often associated with genetic disorders
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* How We Draw Conclusions */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">How We Draw Conclusions</h2>
          
          <div className="bg-white p-8 rounded-lg shadow-lg mb-8">
            <h3 className="text-2xl font-semibold text-blue-600 mb-6">Our Analysis Process</h3>
            
            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-sm font-bold text-blue-600">1</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800">Reference Database Comparison</h4>
                  <p className="text-gray-700">
                    We compare your genetic variants against extensive databases like ClinVar, 
                    OMIM, and population frequency databases.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-sm font-bold text-green-600">2</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800">Scientific Literature Review</h4>
                  <p className="text-gray-700">
                    Each variant is cross-referenced with peer-reviewed research studies 
                    to understand its clinical significance.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-sm font-bold text-purple-600">3</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800">Population Frequency Analysis</h4>
                  <p className="text-gray-700">
                    We analyze how common or rare your variants are in different populations 
                    to assess their potential impact.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-sm font-bold text-red-600">4</span>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800">Functional Impact Prediction</h4>
                  <p className="text-gray-700">
                    Advanced algorithms predict how variants might affect protein structure 
                    and function using computational models.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Risk Categories */}
          <div className="grid md:grid-cols-4 gap-6">
            <div className="bg-red-50 p-6 rounded-lg border-l-4 border-red-500">
              <h4 className="font-semibold text-red-700 mb-2">Pathogenic</h4>
              <p className="text-sm text-red-600">
                Strong evidence for disease causation
              </p>
            </div>
            <div className="bg-orange-50 p-6 rounded-lg border-l-4 border-orange-500">
              <h4 className="font-semibold text-orange-700 mb-2">Likely Pathogenic</h4>
              <p className="text-sm text-orange-600">
                Moderate evidence for disease risk
              </p>
            </div>
            <div className="bg-gray-50 p-6 rounded-lg border-l-4 border-gray-500">
              <h4 className="font-semibold text-gray-700 mb-2">Uncertain</h4>
              <p className="text-sm text-gray-600">
                Insufficient evidence to classify
              </p>
            </div>
            <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-500">
              <h4 className="font-semibold text-green-700 mb-2">Benign</h4>
              <p className="text-sm text-green-600">
                No evidence of disease association
              </p>
            </div>
          </div>
        </section>

        {/* Limitations and Considerations */}
        <section className="mb-16">
          <h2 className="text-3xl font-bold text-gray-800 mb-8 text-center">Important Considerations</h2>
          
          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg">
            <h3 className="text-xl font-semibold text-yellow-800 mb-4">Understanding Limitations</h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold text-yellow-700 mb-2">Genetic vs. Environmental</h4>
                <p className="text-yellow-700 text-sm">
                  Most health conditions result from complex interactions between genetics, 
                  lifestyle, and environmental factors.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-yellow-700 mb-2">Evolving Science</h4>
                <p className="text-yellow-700 text-sm">
                  Our understanding of genetic variants continues to evolve as new research 
                  emerges and databases expand.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-yellow-700 mb-2">Population Bias</h4>
                <p className="text-yellow-700 text-sm">
                  Most genetic research has focused on European populations, which may 
                  limit accuracy for other ethnicities.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-yellow-700 mb-2">Penetrance Variability</h4>
                <p className="text-yellow-700 text-sm">
                  Having a genetic variant doesn't guarantee you'll develop a condition - 
                  penetrance varies widely.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Call to Action */}
        <section className="text-center">
          <div className="bg-gradient-to-r from-blue-600 to-green-600 text-white p-8 rounded-lg">
            <h2 className="text-3xl font-bold mb-4">Ready to Explore Your Genetics?</h2>
            <p className="text-xl mb-6">
              Upload your genetic data and discover personalized insights about your health
            </p>
            <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition duration-300">
              Get Started
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};

export default DNAEducation;
