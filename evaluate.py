#!/usr/bin/env python3
"""
RAG System Evaluation Script

Evaluates RAG system using comprehensive metrics:
- Retrieval: Precision@k, Recall@k, MRR, NDCG@k  
- Generation: BLEU, BERTScore, Hallucination Rate, Perplexity

Usage: python evaluate_rag.py [--format html] [--output-dir DIR] [--scrape]
"""
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv
import requests

sys.path.append(str(Path(__file__).parent))

from core.rag_brain import RAGbrain
from core.logger import logger
from evaluation.test_datasets import EVALUATION_QUERIES
from evaluation.metrics import RAGEvaluator
from evaluation.report_generator import ReportGenerator
from config import OLLAMA_URL, OLLAMA_MODEL, REPORTS_DIR

def check_ollama():
    """Check Ollama availability and install Mistral if needed"""
    try:
        response = requests.get(f"{OLLAMA_URL}/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            mistral_available = any('mistral' in model.get('name', '').lower() for model in models)
            
            if not mistral_available:
                logger.warning("Installing Mistral model...")
                install_response = requests.post(
                    f"{OLLAMA_URL}/pull", 
                    json={"name": OLLAMA_MODEL},
                    timeout=300
                )
                if install_response.status_code != 200:
                    return False
                logger.info("Mistral model installed")
            
            return True
        return False
    except requests.RequestException as e:
        logger.error(f"Ollama connection failed: {e}")
        return False

def run_evaluation(rag_pipeline: RAGbrain, evaluator: RAGEvaluator) -> dict:
    """Run complete evaluation process"""
    logger.info("Starting evaluation...")
    evaluation_data = []
    
    for i, query_data in enumerate(EVALUATION_QUERIES):
        logger.info(f"Processing query {i+1}/{len(EVALUATION_QUERIES)}")
        
        result = rag_pipeline.process_user_query(query_data['query'])
        
        eval_item = {
            "query": query_data['query'],
            "generated_response": result['response'] or "No response",
            "ground_truth": query_data['ground_truth'],
            "retrieved_sources": result['sources'] or [],
            "relevant_sources": query_data['relevant_states'],
            "context": "\n".join(result.get('retrived_documents', [])),
            "difficulty": query_data.get('difficulty', 'medium')
        }
        
        evaluation_data.append(eval_item)
    
    logger.info("Computing retrieval metrics...")
    retrieval_results = evaluator.evaluate_retrieval(evaluation_data)
    
    logger.info("Computing generation metrics...")
    generation_results = evaluator.evaluate_generation(evaluation_data)
    
    return {
        "retrieval_metrics": retrieval_results,
        "generation_metrics": generation_results,
        "total_queries": len(evaluation_data),
        "evaluation_data": evaluation_data
    }

def main():
    parser = argparse.ArgumentParser(description='Evaluate RAG System Performance')
    parser.add_argument('--format', '-f', default='html', help='Report format (html)')
    parser.add_argument('--output-dir', '-o', default=str(REPORTS_DIR), help='Output directory')
    parser.add_argument('--scrape', '-s', action='store_true', help='Scrape fresh data')
    args = parser.parse_args()
    
    load_dotenv()
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    logger.info("🚀 Starting RAG Evaluation")
    
    if not check_ollama():
        logger.error("❌ Ollama/Mistral unavailable. Install: https://ollama.ai/")
        logger.error("Then run: ollama pull mistral")
        sys.exit(1)
    
    try:
        logger.info("Initializing RAG pipeline...")
        rag_pipeline = RAGbrain(scraped_data=args.scrape)
        
        logger.info("Initializing evaluator...")
        evaluator = RAGEvaluator()
        
        logger.info("Running evaluation...")
        results = run_evaluation(rag_pipeline, evaluator)
        
        logger.info("Generating reports...")
        report_generator = ReportGenerator(args.output_dir)
        report_paths = report_generator.generate_report(results, args.format)
        
        # Results summary
        logger.info("📊 Evaluation Complete!")
        logger.info("="*60)
        
        gen_metrics = results['generation_metrics']
        logger.info(f"BLEU Score: {gen_metrics.get('avg_bleu_score', 0):.4f}")
        logger.info(f"BERT Score: {gen_metrics.get('avg_bert_score', 0):.4f}")
        logger.info(f"Hallucination Rate: {gen_metrics.get('hallucination_rate', 0):.2%}")
        logger.info(f"Perplexity: {gen_metrics.get('avg_perplexity', 0):.2f}")
        
        logger.info(f"\n📄 Report: {report_paths.get('html', 'N/A')}")
        logger.info("✅ Evaluation completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Evaluation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()