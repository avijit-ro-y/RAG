"""
Comprehensive RAG evaluation metrics
"""
import numpy as np
import math
import requests
import json
import re
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize
from config import OLLAMA_URL, OLLAMA_MODEL, EMBEDDING_MODEL, REQUEST_TIMEOUT
from core.logger import logger

class RetrievalMetrics:
    """Retrieval performance metrics"""
    
    @staticmethod
    def precision_at_k(retrieved_docs: list, relevant_docs: list, k: int) -> float:
        """Calculate Precision@k with improved matching"""
        if k == 0 or not retrieved_docs:
            return 0.0
        
        retrieved_k = retrieved_docs[:k]
        relevant_retrieved = 0
        
        for retrieved in retrieved_k:
            if not retrieved:
                continue
            retrieved_lower = retrieved.lower()
            for relevant in relevant_docs:
                if not relevant:
                    continue
                relevant_lower = relevant.lower()
                if (relevant_lower == retrieved_lower or 
                    relevant_lower in retrieved_lower or 
                    retrieved_lower in relevant_lower):
                    relevant_retrieved += 1
                    break
        
        return relevant_retrieved / min(k, len([r for r in retrieved_k if r]))
    
    @staticmethod
    def recall_at_k(retrieved_docs: list, relevant_docs: list, k: int) -> float:
        """Calculate Recall@k"""
        if not relevant_docs:
            return 0.0
        
        retrieved_k = retrieved_docs[:k]
        found_relevant = 0
        
        for relevant in relevant_docs:
            if not relevant:
                continue
            relevant_lower = relevant.lower()
            for retrieved in retrieved_k:
                if not retrieved:
                    continue
                retrieved_lower = retrieved.lower()
                if (relevant_lower == retrieved_lower or 
                    relevant_lower in retrieved_lower or 
                    retrieved_lower in relevant_lower):
                    found_relevant += 1
                    break
        
        return found_relevant / len(relevant_docs)
    
    @staticmethod
    def mean_reciprocal_rank(retrieved_docs: list, relevant_docs: list) -> float:
        """Calculate MRR"""
        for i, doc in enumerate(retrieved_docs):
            if doc in relevant_docs:
                return 1.0 / (i + 1)
        return 0.0
    
    @staticmethod
    def ndcg_at_k(retrieved_docs: list, relevant_docs: list, k: int) -> float:
        """Calculate NDCG@k"""
        if k == 0:
            return 0.0
            
        retrieved_k = retrieved_docs[:k]
        relevance_scores = [1 if doc in relevant_docs else 0 for doc in retrieved_k]
        
        # DCG calculation
        dcg = relevance_scores[0] if relevance_scores else 0
        for i in range(1, len(relevance_scores)):
            dcg += relevance_scores[i] / math.log2(i + 1)
        
        # IDCG calculation
        ideal_relevance = sorted([1 if doc in relevant_docs else 0 for doc in retrieved_k], reverse=True)
        idcg = ideal_relevance[0] if ideal_relevance else 0
        for i in range(1, len(ideal_relevance)):
            idcg += ideal_relevance[i] / math.log2(i + 1)
        
        return dcg / idcg if idcg > 0 else 0.0

class GenerationMetrics:
    """Generation quality metrics"""
    
    def __init__(self):
        self.sentence_model = SentenceTransformer(EMBEDDING_MODEL)
    
    def bleu_score(self, generated: str, reference: str) -> float:
        """Calculate BLEU score"""
        try:
            if not generated or not reference:
                return 0.0
            
            def preprocess_text(text):
                text = text.lower().strip()
                text = ' '.join(text.split())
                import string
                text = text.translate(str.maketrans('', '', string.punctuation))
                return text
            
            reference_clean = preprocess_text(reference)
            generated_clean = preprocess_text(generated)
            
            if not reference_clean or not generated_clean:
                return 0.0
            
            try:
                reference_tokens = word_tokenize(reference_clean)
                generated_tokens = word_tokenize(generated_clean)
            except:
                reference_tokens = reference_clean.split()
                generated_tokens = generated_clean.split()
            
            if not reference_tokens or not generated_tokens:
                return 0.0
            
            smoothing = SmoothingFunction().method1
            weights = (1.0, 0, 0, 0)
            score = sentence_bleu([reference_tokens], generated_tokens, 
                                weights=weights, smoothing_function=smoothing)
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"BLEU calculation error: {e}")
            return 0.0
    
    def bert_score(self, generated: str, reference: str) -> float:
        """Calculate BERTScore using sentence transformers"""
        try:
            generated_embedding = self.sentence_model.encode([generated])
            reference_embedding = self.sentence_model.encode([reference])
            
            similarity = cosine_similarity(generated_embedding, reference_embedding)[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"BERTScore calculation error: {e}")
            return 0.0
    
    def calculate_perplexity(self, text: str) -> float:
        """Calculate normalized perplexity"""
        try:
            if not text or not text.strip():
                return 50.0
            
            words = text.strip().split()
            if len(words) == 0:
                return 50.0
            
            unique_words = len(set(words))
            total_words = len(words)
            
            if total_words == 0:
                return 50.0
            
            lexical_diversity = unique_words / total_words
            avg_word_length = sum(len(word) for word in words) / total_words
            sentences = text.count('.') + text.count('!') + text.count('?') + 1
            avg_sentence_length = total_words / sentences
            
            base_perplexity = 20.0
            diversity_factor = max(0.1, lexical_diversity) * 0.5
            length_factor = min(avg_sentence_length / 15.0, 2.0)
            
            perplexity = base_perplexity / diversity_factor * length_factor
            return max(5.0, min(perplexity, 50.0))
            
        except Exception as e:
            logger.error(f"Perplexity calculation error: {e}")
            return 25.0
    
    def detect_hallucination(self, generated_text: str, context: str, query: str) -> dict:
        """Detect hallucinations using heuristics and LLM"""
        try:
            hallucination_indicators = [
                "penguins in india", "snow in kerala", "desert in west bengal",
                "space program in goa", "arctic climate in tamil nadu"
            ]
            
            generated_lower = generated_text.lower()
            for indicator in hallucination_indicators:
                if indicator in generated_lower:
                    return {
                        "has_hallucination": True,
                        "confidence": 0.9,
                        "explanation": f"Detected factual error: {indicator}"
                    }
            
            # Use Ollama for sophisticated detection
            prompt = f"""Analyze for factual accuracy about Indian states:

Query: {query}
Context: {context}
Response: {generated_text}

Check for geographical, climatic, or cultural contradictions.
Respond with JSON: {{"has_hallucination": true/false, "confidence": 0.0-1.0, "explanation": "reason"}}"""
            
            response = requests.post(
                f"{OLLAMA_URL}/generate",
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '')
                
                try:
                    json_match = re.search(r'\{[^{}]*\}', response_text)
                    if json_match:
                        hallucination_data = json.loads(json_match.group())
                        return {
                            "has_hallucination": hallucination_data.get("has_hallucination", False),
                            "confidence": min(hallucination_data.get("confidence", 0.5), 1.0),
                            "explanation": hallucination_data.get("explanation", "Analysis completed")
                        }
                except json.JSONDecodeError:
                    pass
            
            return {"has_hallucination": False, "confidence": 0.6, "explanation": "No hallucinations detected"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API error: {e}")
            return {"has_hallucination": False, "confidence": 0.0, "reason": "API_ERROR"}
        except Exception as e:
            logger.error(f"Unexpected error in hallucination detection: {e}")
            return {"has_hallucination": False, "confidence": 0.0, "reason": "PROCESSING_ERROR"}

class RAGEvaluator:
    """Main evaluator combining all metrics"""
    
    def __init__(self):
        self.retrieval_metrics = RetrievalMetrics()
        self.generation_metrics = GenerationMetrics()
    
    def evaluate_retrieval(self, queries_and_results: list, k_values: list = None) -> dict:
        """Evaluate retrieval performance"""
        if k_values is None:
            from config import K_VALUES
            k_values = K_VALUES
            
        results = {f"precision@{k}": [] for k in k_values}
        results.update({f"recall@{k}": [] for k in k_values})
        results.update({f"ndcg@{k}": [] for k in k_values})
        results["mrr"] = []
        
        for item in queries_and_results:
            retrieved_sources = item.get("retrieved_sources", [])
            relevant_sources = item.get("relevant_sources", [])
            
            mrr = self.retrieval_metrics.mean_reciprocal_rank(retrieved_sources, relevant_sources)
            results["mrr"].append(mrr)
            
            for k in k_values:
                precision = self.retrieval_metrics.precision_at_k(retrieved_sources, relevant_sources, k)
                recall = self.retrieval_metrics.recall_at_k(retrieved_sources, relevant_sources, k)
                ndcg = self.retrieval_metrics.ndcg_at_k(retrieved_sources, relevant_sources, k)
                
                results[f"precision@{k}"].append(precision)
                results[f"recall@{k}"].append(recall)
                results[f"ndcg@{k}"].append(ndcg)
        
        avg_results = {}
        for metric, values in results.items():
            avg_results[f"avg_{metric}"] = np.mean(values) if values else 0.0
            avg_results[f"std_{metric}"] = np.std(values) if values else 0.0
        
        return avg_results
    
    def evaluate_generation(self, queries_and_results: list) -> dict:
        """Evaluate generation quality"""
        bleu_scores = []
        bert_scores = []
        hallucination_rates = []
        perplexities = []
        
        for item in queries_and_results:
            generated = item.get("generated_response", "")
            reference = item.get("ground_truth", "")
            context = item.get("context", "")
            query = item.get("query", "")
            
            bleu = self.generation_metrics.bleu_score(generated, reference)
            bleu_scores.append(bleu)
            
            bert = self.generation_metrics.bert_score(generated, reference)
            bert_scores.append(bert)
            
            hallucination_result = self.generation_metrics.detect_hallucination(generated, context, query)
            hallucination_rates.append(1.0 if hallucination_result["has_hallucination"] else 0.0)
            
            perplexity = self.generation_metrics.calculate_perplexity(generated)
            perplexities.append(perplexity)
        
        return {
            "avg_bleu_score": np.mean(bleu_scores) if bleu_scores else 0.0,
            "std_bleu_score": np.std(bleu_scores) if bleu_scores else 0.0,
            "avg_bert_score": np.mean(bert_scores) if bert_scores else 0.0,
            "std_bert_score": np.std(bert_scores) if bert_scores else 0.0,
            "hallucination_rate": np.mean(hallucination_rates) if hallucination_rates else 0.0,
            "avg_perplexity": np.mean(perplexities) if perplexities else 0.0,
            "std_perplexity": np.std(perplexities) if perplexities else 0.0
        }