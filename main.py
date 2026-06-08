# Start Program
#         ↓
# Parse Arguments
#         ↓
# Initialize Logger
#         ↓
# Initialize RAGBrain
#         ↓
# (Optional)
# Scrape Data
#         ↓
# Choose Mode
#  ┌──────────────┴──────────────┐
#  ↓                             ↓
# Test Mode                Interactive Mode
#  ↓                             ↓
# Predefined Queries       User Questions
#  ↓                             ↓
# process_user_query()     process_user_query()
#  ↓                             ↓
# Retrieve Context         Retrieve Context
#  ↓                             ↓
# Gemini Response          Gemini Response
#  ↓                             ↓
# Display Results          Display Results
#  ↓                             ↓
# End                     Exit on q


#RAG System Main Interface

import argparse
from core.rag_brain import RAGbrain
from core.logger import logger

def run_test_questions(rag):
    
    example_queries = [ #Run predefined test questions
        "What are the main tourist attractions in Kerala?",
        "Tell me about the history of Tamil Nadu",
        "What is the economy of Gujarat like?",
        "Describe the culture and traditions of Rajasthan",
        "What are the geographical features of Himachal Pradesh?"
    ]
    
    for query in example_queries:
        result = rag.process_user_query(query) #Call pipeline
        
        print("\n" + "="*80) #Prints separator line(================================================================================)
        print(f"QUERY: {query}")
        print("-"*80) #--------------------------------------------------------------------------------
        print(f"RESPONSE: {result['response']}")
        print("-"*80)
        print(f"SOURCES: {', '.join(result['sources'])}")
        print("="*80)

def interactive_mode(rag): #Interactive question-answer session
    print("\n" + "="*80)
    print("Indian States RAG System - Interactive Mode")
    print("Type 'exit', 'quit', or 'q' to end")
    print("="*80)
    
    while True:
        query = input("\nEnter your question: ")
        
        if query.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if query.strip(): #Clean input(Avoid empty input)
            result = rag.process_user_query(query)
            
            print("\n" + "-"*80)
            print(f"RESPONSE: {result['response']}")
            print("-"*80)
            print(f"SOURCES: {', '.join(result['sources'])}")
            print("-"*80)

def main():
    parser = argparse.ArgumentParser(description='RAG System for Indian States') #Allows commands like: Allows commands like: python main.py --mode interactive or python main.py --mode test 
    parser.add_argument('--mode', '-m', choices=['test', 'interactive'], default='interactive', #Possible commands : python main.py... by default by default : python main.py --mode test
                        help='Run mode (default: interactive)')
    parser.add_argument('--scrape', '-s', action='store_true',      #python main.py --scrape Will(scrape data,rebuild database)...present : python main.py --scrape
                        help='Scrape fresh data from Wikipedia')
    args = parser.parse_args() #Parse Arguments Reads terminal command....Example:python main.py --mode test --scrape
    
    logger.info("Starting RAG System")
    
    rag = RAGbrain(scraped_data=args.scrape)
    
    if args.mode == 'test':
        run_test_questions(rag)
    else:
        interactive_mode(rag)

if __name__ == "__main__": #Python standard entry point...Run main() only when python main.py
    main()
