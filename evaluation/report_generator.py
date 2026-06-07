"""
Generate comprehensive evaluation reports
"""

import datetime
from typing import Dict, Any
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from config import REPORTS_DIR

class ReportGenerator:
    """Generate comprehensive evaluation reports"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else REPORTS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def generate_visualizations(self, results: Dict[str, Any]) -> Dict[str, str]:
        """Generate visualization plots"""
        plots = {}
        
        # Retrieval metrics chart
        retrieval_metrics = {
            k.replace('avg_', ''): v for k, v in results.get('retrieval_metrics', {}).items() 
            if k.startswith('avg_')
        }
        
        if retrieval_metrics:
            fig, ax = plt.subplots(figsize=(12, 6))
            metrics = list(retrieval_metrics.keys())
            values = list(retrieval_metrics.values())
            
            bars = ax.bar(metrics, values, color=sns.color_palette("husl", len(metrics)))
            ax.set_title('Retrieval Metrics Performance', fontsize=16, fontweight='bold')
            ax.set_xlabel('Metrics')
            ax.set_ylabel('Score')
            ax.set_ylim(0, 1.0)
            
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                       f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            retrieval_plot = 'retrieval_metrics.png'
            plt.savefig(retrieval_plot, dpi=300, bbox_inches='tight')
            plt.close()
            plots['retrieval_metrics'] = str(retrieval_plot)
        
        # Generation metrics chart
        generation_metrics = {
            'BLEU Score': results.get('generation_metrics', {}).get('avg_bleu_score', 0),
            'BERT Score': results.get('generation_metrics', {}).get('avg_bert_score', 0),
            'Hallucination Rate': results.get('generation_metrics', {}).get('hallucination_rate', 0),
            'Perplexity (norm)': min(results.get('generation_metrics', {}).get('avg_perplexity', 100) / 100, 1.0)
        }
        
        fig, ax = plt.subplots(figsize=(10, 6))
        metrics = list(generation_metrics.keys())
        values = list(generation_metrics.values())
        
        colors = ['green' if 'Hallucination' not in metric else 'red' for metric in metrics]
        bars = ax.bar(metrics, values, color=colors, alpha=0.7)
        
        ax.set_title('Generation Metrics Performance', fontsize=16, fontweight='bold')
        ax.set_xlabel('Metrics')
        ax.set_ylabel('Score')
        ax.set_ylim(0, 1.0)
        
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                   f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        generation_plot = 'generation_metrics.png'
        plt.savefig(generation_plot, dpi=300, bbox_inches='tight')
        plt.close()
        plots['generation_metrics'] = str(generation_plot)
        
        # Interactive dashboard
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Precision@K', 'Recall@K', 'NDCG@K', 'Overall Performance'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "domain"}]]
        )
        
        k_values = [1, 3, 5]
        precision_values = [results.get('retrieval_metrics', {}).get(f'avg_precision@{k}', 0) for k in k_values]
        recall_values = [results.get('retrieval_metrics', {}).get(f'avg_recall@{k}', 0) for k in k_values]
        ndcg_values = [results.get('retrieval_metrics', {}).get(f'avg_ndcg@{k}', 0) for k in k_values]
        
        fig.add_trace(go.Scatter(x=k_values, y=precision_values, mode='lines+markers', name='Precision@K'), row=1, col=1)
        fig.add_trace(go.Scatter(x=k_values, y=recall_values, mode='lines+markers', name='Recall@K'), row=1, col=2)
        fig.add_trace(go.Scatter(x=k_values, y=ndcg_values, mode='lines+markers', name='NDCG@K'), row=2, col=1)
        
        overall_scores = [
            results.get('generation_metrics', {}).get('avg_bleu_score', 0),
            results.get('generation_metrics', {}).get('avg_bert_score', 0),
            1 - results.get('generation_metrics', {}).get('hallucination_rate', 0),
            results.get('retrieval_metrics', {}).get('avg_precision@5', 0)
        ]
        fig.add_trace(go.Pie(labels=['BLEU', 'BERT', 'Non-Hallucination', 'Precision@5'], 
                           values=overall_scores, name="Overall Performance"), row=2, col=2)
        
        fig.update_layout(height=800, showlegend=True, title_text="RAG Performance Dashboard")
        
        interactive_plot = 'interactive_dashboard.html'
        fig.write_html(str(interactive_plot))
        plots['interactive_dashboard'] = str(interactive_plot)
        
        return plots
    
    def generate_html_report(self, results: Dict[str, Any], plots: Dict[str, str]) -> str:
        """Generate HTML report"""
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAG System Evaluation Report</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; border-left: 5px solid #3498db; padding-left: 15px; margin-top: 30px; }
        .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; margin-bottom: 10px; }
        .metric-name { font-size: 1.1em; opacity: 0.9; }
        .chart-container { text-align: center; margin: 30px 0; }
        .chart-container img { max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .summary-box { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .timestamp { text-align: center; color: #7f8c8d; font-style: italic; margin-top: 30px; }
        .details-table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        .details-table th, .details-table td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        .details-table th { background-color: #3498db; color: white; }
        .details-table tr:nth-child(even) { background-color: #f9f9f9; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 RAG System Evaluation Report</h1>
        
        <div class="summary-box">
            <h2>📊 Executive Summary</h2>
            <p>Comprehensive evaluation of Retrieval-Augmented Generation system performance across retrieval accuracy, generation quality, and hallucination detection.</p>
            <p><strong>Total Queries:</strong> {{ total_queries }}</p>
            <p><strong>Date:</strong> {{ timestamp }}</p>
        </div>

        <h2>🎯 Retrieval Performance</h2>
        <div class="metric-grid">
            {% for metric, value in retrieval_metrics.items() %}
            {% if metric.startswith('avg_') %}
            <div class="metric-card">
                <div class="metric-value">{{ "%.3f"|format(value) }}</div>
                <div class="metric-name">{{ metric.replace('avg_', '').replace('_', ' ').title() }}</div>
            </div>
            {% endif %}
            {% endfor %}
        </div>

        {% if plots.retrieval_metrics %}
        <div class="chart-container">
            <img src="{{ plots.retrieval_metrics }}" alt="Retrieval Metrics">
        </div>
        {% endif %}

        <h2>✨ Generation Quality</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{{ "%.3f"|format(generation_metrics.avg_bleu_score or 0) }}</div>
                <div class="metric-name">BLEU Score</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ "%.3f"|format(generation_metrics.avg_bert_score or 0) }}</div>
                <div class="metric-name">BERT Score</div>
            </div>
            <div class="metric-card" style="background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);">
                <div class="metric-value">{{ "%.1f"|format((generation_metrics.hallucination_rate or 0) * 100) }}%</div>
                <div class="metric-name">Hallucination Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ "%.1f"|format(generation_metrics.avg_perplexity or 0) }}</div>
                <div class="metric-name">Perplexity</div>
            </div>
        </div>

        {% if plots.generation_metrics %}
        <div class="chart-container">
            <img src="{{ plots.generation_metrics }}" alt="Generation Metrics">
        </div>
        {% endif %}

        <div class="timestamp">
            Report generated on {{ timestamp }}
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(html_template)
        html_content = template.render(
            retrieval_metrics=results.get('retrieval_metrics', {}),
            generation_metrics=results.get('generation_metrics', {}),
            plots=plots,
            total_queries=results.get('total_queries', 0),
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        html_path = 'evaluation_report.html'
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(html_path)
    
    def generate_report(self, results: Dict[str, Any], format_type: str = "html") -> Dict[str, str]:
        """Generate report in specified format"""
        plots = self.generate_visualizations(results)
        html_path = self.generate_html_report(results, plots)
        
        return {"html": html_path, **plots}