import logging #Gives you logging.info(), logging.error(), handlers, formatters, etc.
from dotenv import load_dotenv #Imports a function that reads a .env file and loads variables into os.environ.
from config import LOG_LEVEL,LOG_FORMAT,LOG_DIR #LOG_LEVEL → INFO / DEBUG / ERROR...LOG_FORMAT → how logs look...LOG_DIR → where logs are stored

load_dotenv() #Loads variables from .env file into your program

def loging():
    LOG_DIR.mkdir(parents=True,exist_ok=True) #Create logs folder....mkdir() Creates a folder (directory)..parents=True create parent folders if missing...exist_ok=True don’t crash if folder already exists
    numeric_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig( #Configure logging behavior
        level=numeric_level, #Log Level Show INFO, WARNING, ERROR
        format=LOG_FORMAT,
        handlers=[  #Handlers Defines where logs go
            logging.FileHandler(LOG_DIR / "rag_system.log", encoding="utf-8"), #FileHandler Saves logs to file
            logging.StreamHandler() #StreamHandler Prints logs to terminal
        ]
    )
    return logging.getLogger(__name__) #getLogger() Creates or gets a logger object...__name__ Name of current file/module
logger = loging()