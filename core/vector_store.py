# Processed Text Chunks
#         ↓
# Connect ChromaDB
#         ↓
# Create Collection
#         ↓
# Generate Unique IDs
#         ↓
# Store Documents,Embeddings,Metadata in ChromaDB
#         ↓
# User Query
#         ↓
# Generate Query Embedding
#         ↓
# Search Similar Vectors
# (Chroma Similarity Search)
#         ↓
# Retrieve Top Candidate Chunks
#         ↓
# Apply Source Diversification
# (Max 2 Chunks per State)
#         ↓
# Fill Remaining Results
# (if needed)
#         ↓
# Prepare Final Documents,Metadata
#         ↓
# Return Relevant Context
#         ↓
# Ready for LLM


from config import CHROMA_DB_DIR,COLLECTION_NAME,NUMBER_OF_RESULTS
from .logger import logger
import chromadb
import uuid

class VectorStore: #storing embeddings and retrieving similar ones
    def __init__(self):
        CHROMA_DB_DIR.mkdir(parents=True,exist_ok=True) #Creates the chroma_db/ folder on disk if it doesn't exist. ChromaDB needs a physical folder to save its files. parents=True creates missing parent folders. exist_ok=True doesn't crash if folder already exists. 
        
        logger.info(f"Initializing ChromaDB at {CHROMA_DB_DIR}")
        self.client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR)) #Creates a client to the connect with your databas. Two types of clients Client()( Lost on restart), PersistentClient() ( Saved to disk..for Production)
        self.collection = self.client.get_or_create_collection(COLLECTION_NAME) #A collection in ChromaDB is like a table in a normal database. It holds all your documents, embeddings, and metadata together. First run → creates a fresh collection named "indian_states". Second run → loads the existing collection (your data). This is why you don't need to re-scrape and re-embed every time you run the project

    def store_data_in_ChromaDB(self,texts,embeddings,metadata): #Takes three parallel lists — all the same length
        if not texts or len(embeddings) == 0 or not metadata: #if any of the list is empty then it return none
            logger.warning("Empty list!")
            return
        
        ids = [str(uuid.uuid4()) for i in texts] #Creates one unique ID for each chunk. uuid.uuid4() generates a random UUID object → str() converts it to a string like "a3f8c2d1-9b4e-...".

        logger.info(f"Adding {len(texts)} documents")

        self.collection.add(documents=texts,embeddings=embeddings.tolist(),metadatas=metadata,ids=ids) #Stores everything in ChromaDB (collection table) in one call. embeddings.tolist() — converts NumPy array to plain Python list.
        
        logger.info(f"Vector store contains {self.collection.count()} documents!")

    def users_query (self,query,query_embeddings,no_of_results=NUMBER_OF_RESULTS): #Returns a tuple of (documents, metadata).
        logger.info(f"Qureying for : {query[:30]}....") #slices first 30 characters. Prevents very long questions from flooding the logs.
        
        temporary_results = max(no_of_results*10,30) #Without this Fetch only 5 → all 5 might be Kerala chunks → no diversity 

        results = self.collection.query(query_embeddings=[query_embeddings.tolist()],n_results=temporary_results) #Here query will be automatically embedded.
        
        documents = results['documents'][0] #ChromaDB returns a dictionary with lists inside lists (results = { 'documents': [["Kerala chunk...", "Tamil chunk...", ...]], 'metadatas': [[{"state":"Kerala"}, {"state":"Tamil Nadu"}, ...]], 'distances': [[0.12, 0.18, 0.24, ...]]} )......Why [0]? Because Chroma returns list of queries
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]

        diversified_docs = [] # final selected documents
        diversified_metadatas = [] # their metadata
        source_count = {} # tracks how many chunks per state
        max_per_source = 2 # max 2 chunks allowed per state

        # First pass: prioritize source diversity
        for document, metadata, distance in zip(documents,metadatas,distances): #zip(documents, metadatas, distances) — loops through all three lists simultaneously
            if len(diversified_docs) >= no_of_results: #Stop as soon as you have enough results(5)
                break

            source = metadata.get('state','unknown') #meta is a dict like {"state": "Kerala", "chunk_id": 3}......get('state', 'unknown') safely reads the state key....f missing for some reason, returns 'unknown' as fallback.
            current_count = source_count.get(source,0) #return the number of sources...if none then default return 0

            # Add if we haven't seen this source yet, or if we have room for more from this source
            if current_count < max_per_source: #Only add this chunk if its state hasn't reached the limit of 2
                diversified_docs.append(document)
                diversified_metadatas.append(metadata)
                source_count[source] =current_count + 1

        # Second pass: fill remaining slots if needed (less strict on diversity)
        if len(diversified_docs) < no_of_results: #If not enough results after filtering(fills remaining slots.)
            for document, metadata in zip(documents,metadatas): 
                if len(diversified_docs) >= no_of_results: 
                    break

                if document not in  diversified_docs: #Only add this chunk if its state hasn't reached the limit of 2
                    diversified_docs.append(document)
                    diversified_metadatas.append(metadata)
                
        unique_sources = len(set(meta.get('state','unknown') for meta in diversified_metadatas)) #Counts how many different states are in the final results. set(...) — a set removes duplicates, so only unique state names remain. 
        logger.info(f"Retrived {len(diversified_docs)} documents from {unique_sources} unique sources!")
        return diversified_docs,diversified_metadatas