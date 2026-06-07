# Processed Text Chunks
#         ↓
# Load SentenceTransformer Model
#         ↓
# Validate Input Text
#         ↓
# Pass Chunks to Model
#         ↓
# Convert Text → Numerical Vectors
#         ↓
# Generate Embeddings
#         ↓
# Return Embedding Collection
#         ↓
# Ready for Vector Database Storage


from sentence_transformers import SentenceTransformer
from logger import logger
from config import EMBEDDING_MODEL

class Embedder: #embeddings → “How text becomes numbers”...Generates embeddings for text chunks
    
    # logger.info(f"Loading embedding model : {EMBEDDING_MODEL}")         
    # st_model = SentenceTransformer(EMBEDDING_MODEL)                   Problem: This runs the moment Python imports the file — even if you never create an Embedder object. Also st_model becomes a class variable (shared across all instances) instead of an instance variable.

    def __init__(self): 
        logger.info(f"Loading embedding model : {EMBEDDING_MODEL}")
        self.st_model = SentenceTransformer(EMBEDDING_MODEL)

    def generate_embeddings(self,texts): #it takes the chunks as a list
        if not texts: #is the list is empty or not
            logger.warning("No texts or chunks are provided for embedding")
            return []
        
        logger.info(f"Generating embeddings for {len(texts)} texts")
        embeddings = self.st_model.encode(texts)
        return embeddings