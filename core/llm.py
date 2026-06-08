from config import GOOGLE_API_KEY,GEMINI_MODEL
import google.generativeai as genai
from .logger import logger

class GeminiLLM:
    def __init__(self):
        if not GOOGLE_API_KEY:
            raise ValueError("Google API key not found!") #Stops execution immediately.
        
        genai.configure(api_key=GOOGLE_API_KEY) #Login to Gemini using your API key.
        logger.info("Configured successfully!")
        self.model = genai.GenerativeModel(GEMINI_MODEL) #Load Model
    
    def generate_response(self,query,context=None):
        try:
            if context: #if query given but context not given ...then it will not work
                prompt = f"""Based on the information, answer the question: 
                    
                    Question: {query} 

                    Context: {context}

                    Answer:""" #What this does? Combines Question,Retrieved knowledge and Sends to LLM
                
            else: #If no context → just ask directly(Problem This becomes normal chatbot (not RAG))
                prompt = query
            
            logger.info(f"Generating response for: {query[:50]}...")
            response = self.model.generate_content(prompt) #Prompt → Gemini → Output(Input(Question + Context))
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error: {str(e)}"