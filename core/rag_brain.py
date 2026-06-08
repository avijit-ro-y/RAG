# Create Scraper
#         ↓
# Create Text Processor
#         ↓
# Create Embedder
#         ↓
# Connect ChromaDB
#         ↓
# Load Gemini
#         ↓
# (Optional)
# Scrape Data
#         ↓
# Chunk Data
#         ↓
# Generate Embeddings
#         ↓
# Store in ChromaDB
#         ↓
# User Query
#         ↓
# Generate Query Embedding
#         ↓
# Search ChromaDB
#         ↓
# Retrieve Documents
#         ↓
# Build Context
#         ↓
# Send Query + Context to Gemini
#         ↓
# Generate Answer
#         ↓
# Collect Unique Sources
#         ↓
# Return Result


from .logger import logger
from config import N_RESULTS
from .scraper import WikipediaScraper
from .text_processor import TextProcessor
from .embedder import Embedder
from .vector_store import VectorStore
from .llm import GeminiLLM

class RAGbrain: #This is the brain of the entire system. Manage entire RAG workflow
    def __init__(self,scraped_data = False):
        logger.info("Initializing RAG brain!")

        self.scraper = WikipediaScraper()
        self.text_processor = TextProcessor()
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.llm = GeminiLLM()

        if scraped_data:  #Only if scrape_data=True, it immediately runs the full data ingestion pipeline.
            logger.info("Scraping freash data...!")
            self.scrape_and_process()

    def scrape_and_process(self):
        self.scraper.scrape_all_state_data()
        all_chunks, metadata = self.text_processor.process_all_state_data()
        embeddings = self.embedder.generate_embeddings(all_chunks)
        self.vector_store.store_data_in_ChromaDB(all_chunks,embeddings,metadata)
        logger.info("Scraping, processing and storing done!")

    def process_user_query(self,query,no_of_results = N_RESULTS):
        logger.info(f"Processing : {query}")

        query_embedding = self.embedder.generate_embeddings([query])[0]
        documents, metadatas = self.vector_store.users_query(query,query_embedding,no_of_results)

        context = "\n\n".join([ #Why Build Context? Because Gemini needs: Question + Retrieved Knowledge
            f"Source : {meta['state']}\n{doc}" #here state and its data are given!
            for doc, meta in zip(documents,metadatas)
        ])

        response = self.llm.generate_response(query,context) #Sends both the question and the assembled context to Gemini. Gemini reads all the retrieved chunks and generates a grounded answer based on them.

        sources = [] #Prepare unique state list
        seen = set() 
        for meta in metadatas:
            state = meta['state']
            if state not in seen:
                sources.append(state)
                seen.add(state)
        
        return {
            "query":query,
            "response":response,
            "sources":sources,
            "retrived_documents":documents,
        }
 
