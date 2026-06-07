# .env file
#    ↓
# load_dotenv()  (from utils.py)
#    ↓
# os.getenv()
#    ↓
# LOG_LEVEL set
#    ↓
# logging.basicConfig()
#    ↓
# logs formatted + filtered
#    ↓
# saved in LOG_DIR

import os
from pathlib import Path #Used for file paths
from dotenv import load_dotenv

load_dotenv() # Load .env file

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO") #os.getenv(...) Function to read environment variables...Syntax os.getenv("VARIABLE_NAME", default_value)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s" #It defines how logs will look

# Project Paths
PROJECT_ROOT = Path(__file__).parent #__file__ means current file path (Example project/config.py )...Path(__file__) converts string → Path object....parent gets folder
LOG_DIR = PROJECT_ROOT / "logs" #Combines path (project/ + logs)...Result project/logs/
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DB_DIR = PROJECT_ROOT / "chroma_db"
REPORTS_DIR = PROJECT_ROOT / "evaluation" / "reports"

# Text Processing
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Model Configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-2.0-flash"

# Vector Store
COLLECTION_NAME = "indian_states"
NUMBER_OF_RESULTS = 5

# API Config
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OLLAMA_URL = "http://localhost:11434/api"
OLLAMA_MODEL = "mistral"

# Evaluation Config
K_VALUES = [1, 3, 5]
N_RESULTS = 5
REQUEST_TIMEOUT = 30