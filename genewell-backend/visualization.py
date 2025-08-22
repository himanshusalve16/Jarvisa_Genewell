import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

class GeneDiseaseVisualizer:
    """
    Visualization tools for gene-based disease prediction results
    """
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_model_performance(self, performance_data, save_path=None):
        """
        Plot model performance comparison
        """
        models = list(performance_data.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.ravel()
        
        for i, metric in enumerate(metrics):
            values = [performance_data[model][metric] for model in models]
            
            bars = axes[i].bar(models, values, color=sns.color_palette("husl", len(models)))
            axes[i].set_title(f'{metric.upper()} Comparison')
            axes[i].set_ylabel(metric.upper())
            axes[i].tick_params(axis='x', rotation=45)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                axes[i].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                           f'{value:.3f}', ha='center', va='bottom')
        
        # Remove extra subplot
        axes[-1].remove()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_disease_distribution(self, results, save_path=None):
        """
        Plot distribution of predicted diseases
        """
        # Extract disease predictions
        disease_counts = {}
        for result in results:
            for disease, info in result['predictions'].items():
                if info['predicted']:
                    disease_counts[disease] = disease_counts.get(disease, 0) + 1
        
        if not disease_counts:
            print("No diseases predicted in the results")
            return
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Bar plot
        diseases = list(disease_counts.keys())
        counts = list(disease_counts.values())
        
        bars = ax1.bar(diseases, counts, color=sns.color_palette("husl", len(diseases)))
        ax1.set_title('Disease Prediction Distribution')
        ax1.set_ylabel('Number of Patients')
        ax1.tick_params(axis='x', rotation=45)
        
        # Pie chart
        ax2.pie(counts, labels=diseases, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Disease Prediction Proportions')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_risk_distribution(self, results, save_path=None):
        """
        Plot health risk distribution
        """
        risk_counts = {}
        for result in results:
            status = result['health_status']
            risk_counts[status] = risk_counts.get(status, 0) + 1
        
        # Create plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Bar plot
        statuses = list(risk_counts.keys())
        counts = list(risk_counts.values())
        colors = ['green', 'orange', 'red']
        
        bars = ax1.bar(statuses, counts, color=colors[:len(statuses)])
        ax1.set_title('Health Risk Distribution')
        ax1.set_ylabel('Number of Patients')
        
        # Add value labels
        for bar, count in zip(bars, counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom')
        
        # Pie chart
        ax2.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=90, colors=colors[:len(statuses)])
        ax2.set_title('Health Risk Proportions')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def create_interactive_dashboard(self, results, save_path=None):
        """
        Create an interactive dashboard using Plotly
        """
        # Prepare data
        diseases = set()
        risk_data = []
        
        for result in results:
            for disease, info in result['predictions'].items():
                diseases.add(disease)
                risk_data.append({
                    'patient_id': result['patient_id'],
                    'disease': disease,
                    'probability': info['probability'],
                    'predicted': info['predicted'],
                    'health_status': result['health_status']
                })
        
        df = pd.DataFrame(risk_data)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Disease Risk Heatmap', 'Health Status Distribution', 
                          'Top Disease Probabilities', 'Risk Level by Disease'),
            specs=[[{"type": "heatmap"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "box"}]]
        )
        
        # 1. Disease Risk Heatmap
        pivot_data = df.pivot_table(
            values='probability', 
            index='patient_id', 
            columns='disease', 
            aggfunc='mean'
        ).fillna(0)
        
        fig.add_trace(
            go.Heatmap(
                z=pivot_data.values,
                x=pivot_data.columns,
                y=pivot_data.index,
                colorscale='RdYlBu_r',
                name='Risk Heatmap'
            ),
            row=1, col=1
        )
        
        # 2. Health Status Distribution
        status_counts = df['health_status'].value_counts()
        fig.add_trace(
            go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                name='Health Status'
            ),
            row=1, col=2
        )
        
        # 3. Top Disease Probabilities
        top_diseases = df.groupby('disease')['probability'].mean().sort_values(ascending=False).head(10)
        fig.add_trace(
            go.Bar(
                x=top_diseases.index,
                y=top_diseases.values,
                name='Avg Disease Probability'
            ),
            row=2, col=1
        )
        
        # 4. Risk Level by Disease
        fig.add_trace(
            go.Box(
                x=df['disease'],
                y=df['probability'],
                name='Risk Distribution'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            title_text="GeneWell Disease Prediction Dashboard",
            showlegend=False
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def generate_patient_report(self, patient_result, save_path=None):
        """
        Generate a detailed report for a single patient
        """
        # Create figure
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Disease Risk Probabilities', 'Health Status Overview',
                          'Risk Factors', 'Top Predicted Diseases'),
            specs=[[{"type": "bar"}, {"type": "indicator"}],
                   [{"type": "bar"}, {"type": "pie"}]]
        )
        
        # 1. Disease Risk Probabilities
        diseases = list(patient_result['predictions'].keys())
        probabilities = [patient_result['predictions'][d]['probability'] for d in diseases]
        
        colors = ['red' if p > 0.7 else 'orange' if p > 0.4 else 'green' for p in probabilities]
        
        fig.add_trace(
            go.Bar(
                x=diseases,
                y=probabilities,
                marker_color=colors,
                name='Disease Risk'
            ),
            row=1, col=1
        )
        
        # 2. Health Status Indicator
        status_colors = {'Normal': 'green', 'At Risk': 'orange', 'High Risk': 'red'}
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=len([p for p in probabilities if p > 0.7]),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "High Risk Diseases"},
                gauge={
                    'axis': {'range': [None, len(diseases)]},
                    'bar': {'color': status_colors[patient_result['health_status']]},
                    'steps': [
                        {'range': [0, 2], 'color': "lightgray"},
                        {'range': [2, 5], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 3
                    }
                }
            ),
            row=1, col=2
        )
        
        # 3. Risk Factors
        risk_factors = patient_result['risk_factors']
        if risk_factors:
            fig.add_trace(
                go.Bar(
                    x=['Risk Factors'],
                    y=[len(risk_factors)],
                    name='Risk Factors Count',
                    marker_color='red'
                ),
                row=2, col=1
            )
        
        # 4. Top Predicted Diseases
        top_diseases = sorted(
            patient_result['predictions'].items(),
            key=lambda x: x[1]['probability'],
            reverse=True
        )[:5]
        
        if top_diseases:
            top_names = [d[0] for d in top_diseases]
            top_probs = [d[1]['probability'] for d in top_diseases]
            
            fig.add_trace(
                go.Pie(
                    labels=top_names,
                    values=top_probs,
                    name='Top Diseases'
                ),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            height=600,
            title_text=f"Patient Report: {patient_result['patient_id']}",
            showlegend=False
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def export_results_to_excel(self, results, file_path):
        """
        Export prediction results to Excel with multiple sheets
        """
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = []
            for result in results:
                summary_data.append({
                    'Patient_ID': result['patient_id'],
                    'Health_Status': result['health_status'],
                    'Risk_Factors_Count': len(result['risk_factors']),
                    'High_Risk_Diseases': len([p for p in result['predictions'].values() if p['probability'] > 0.7]),
                    'Moderate_Risk_Diseases': len([p for p in result['predictions'].values() if 0.4 < p['probability'] <= 0.7])
                })
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Detailed predictions sheet
            detailed_data = []
            for result in results:
                for disease, info in result['predictions'].items():
                    detailed_data.append({
                        'Patient_ID': result['patient_id'],
                        'Disease': disease,
                        'Predicted': info['predicted'],
                        'Probability': info['probability'],
                        'Risk_Level': 'High' if info['probability'] > 0.7 else 'Moderate' if info['probability'] > 0.4 else 'Low'
                    })
            
            detailed_df = pd.DataFrame(detailed_data)
            detailed_df.to_excel(writer, sheet_name='Detailed_Predictions', index=False)
            
            # Risk factors sheet
            risk_data = []
            for result in results:
                for factor in result['risk_factors']:
                    risk_data.append({
                        'Patient_ID': result['patient_id'],
                        'Risk_Factor': factor,
                        'Health_Status': result['health_status']
                    })
            
            risk_df = pd.DataFrame(risk_data)
            risk_df.to_excel(writer, sheet_name='Risk_Factors', index=False)
        
        print(f"Results exported to {file_path}")

def main():
    """
    Example usage of the visualizer
    """
    # This would be used with actual results from the ML model
    print("GeneDiseaseVisualizer ready for use!")
    print("Use this class to create visualizations of prediction results.")

if __name__ == "__main__":
    main()
