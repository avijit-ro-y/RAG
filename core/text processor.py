# Load Raw State Files (.txt)
#          ↓
# Check Data Directory Exists
#          ↓
# Read State File Content
#          ↓
# Text File Content Cleaning
                #       ↓
                # Remove Citations ([1], [2], ...)
                #       ↓
                # Remove URLs
                #       ↓
                # Normalize Whitespace
                #       ↓
                # Remove Extra Blank Lines
                #       ↓
                # Return Clean Text
#          ↓
# Configure Chunking (Chunk Size + Chunk Overlap)
#          ↓
# Apply RecursiveCharacterTextSplitter
                #       ↓
                # Split Large Text
                #       ↓
                # Generate Multiple Chunks
#          ↓
# Create Metadata for Each Chunk
                #       ↓
                # State Name
                #       ↓
                # Source Information
                #       ↓
                # Chunk ID
#          ↓
# Store Chunks in all_chunks
#          ↓
# Store Metadata in meta_data
#          ↓
# Repeat for All State Files
#          ↓
# Return Chunks + Metadata
#          ↓
# Ready for Embedding Generation


import re
from logger import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_OVERLAP,CHUNK_SIZE,DATA_DIR


class TextProcessor :
    Text_Splitter = RecursiveCharacterTextSplitter(  #Handles text cleaning and chunking
        chunk_size = CHUNK_SIZE, #Split text into pieces of 1000 characters
        chunk_overlap = CHUNK_OVERLAP, #Last n chars of previous chunk will be copied....Without overlap(Chunk 1:Kerala is famous for, Chunk 2: backwaters and tourism)...With overlap (Chunk 1:Kerala is famous for ,Chunk 2: famous for backwaters and tourism)
        length_function = len,
        separators=["\n\n","\n",". ",""," "] #This tells LangChain:"Where should I try to cut the text?"
    )

    def clean_text(self,text): #Clean and preprocess text
        text = re.sub(r'\[\d+]','',text) # Remove citations....re.sub(pattern, replacement, text)...Before: Kerala is beautiful [1]...After: Kerala is beautiful
        text = re.sub(r'\s+',' ',text) #Remove Multiple spaces...\s Means space, tab, newline...+ Means one or more...Before: Hello       World...After: Hello World
        text = re.sub(r'http[s]?://\S+','',text) #Remove URLs
        text = re.sub(r'\n+','\n',text) #Remove multiple blank lines
        
        return text.strip() #strip() Removes Leading spaces, Trailing spaces ...Before:"   Kerala   "...After:  "Kerala"
    
    def chunk_text(self,text): #Split text into chunks(chunk text came from the clean text method)
        cleaned_text = self.clean_text(text=text)
        chunks = self.Text_Splitter.split_text(cleaned_text) #this will create chunks of the cleaned texts....
        logger.info(F"Created {len(chunks)} chunks!")
        return chunks 
    
    def process_all_state_data(self): #Process all .txt files and produce all_chunks, metadata
        all_chunks = [] #This will store ALL chunks of ALL states... chunks of all states are stored here (all_chunks = ["Kerala chunk 1", "Tamil Nadu chunk 1",.....])
        meta_data = [] #Stores information about each chunk....metadata = [{ "state": "Kerala", "chunk_id": 0}, {...}]

        if not DATA_DIR.exists(): #Checks whether folder exists.
            logger.error(f"Data directory {DATA_DIR} doesn't exist!")
            return [],[]
        
        for state in DATA_DIR.glob("*.txt"): #Get every .txt file(Kerala.txt,......).....glob("*.txt") Means “Get all files ending with .txt”
            state_name = state.stem.replace("_"," ") #Removes extension.(Tamil_Nadu.txt to Tamil_Nadu to Tamil Nadu)....stem Gets filename without extension

            with open(state,"r",encoding="utf-8") as f:
                text = f.read() #all information of teh state is now here

            chunks = self.chunk_text(text=text) #it will store chunks of each state

            for i, chunk in enumerate(chunks): #Loop Through Chunks....enumerate(chunks) gives (0, "chunk1"), (1, "chunk2")....i = index, chunk = actual text
                all_chunks.append(chunk)
                meta_data.append({ #Creates dictionary.
                    "source"  : str(state_name),
                    "state"   : state_name,
                    "chunk_id": i
                })
        logger.info(f"Processed {len(all_chunks)} chunks...")
        return all_chunks,meta_data
