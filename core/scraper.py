# Choose Data Source (Wikipedia)
#          ↓
# Configuration Setup
#(States list + Base URL + Headers)
#          ↓
# Build Core Logic (Single State)
                #       ↓
                # Get Raw HTML Data of state (It consist with html tag and main content)
                #       ↓
                # Convert HTML data to Structured Tree
                #       ↓
                #Data Cleaning (Remove HTML Noise)
                    #          ↓
                    # Locate Main Content (div section) 
                    #          ↓
                    # Extract Useful Data (p tags)
                    #          ↓
                # Store all content in a string
#          ↓
# Scale Logic (Loop for all states)
#          ↓
# Store all state Data in a Dictionary 
#          ↓
# Open and create text file of each state and write data in the file
#          ↓
# Save Data (.txt files)


from logger import logger
import requests #Used to make HTTP requests
from bs4 import BeautifulSoup #Used to parse HTML
import time
from config import DATA_DIR

class WikipediaScraper: #Scrapping data from wikipedia

    Indian_States = [ #Listing all states of india
        "Andhra_Pradesh", "Arunachal_Pradesh", "Assam", "Bihar", 
        "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal_Pradesh", 
        "Jharkhand", "Karnataka", "Kerala", "Madhya_Pradesh", "Maharashtra", 
        "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", 
        "Rajasthan", "Sikkim", "Tamil_Nadu", "Telangana", "Tripura", 
        "Uttar_Pradesh", "Uttarakhand", "West_Bengal"
    ]

    Base_Url = "https://en.wikipedia.org/wiki/" #Creating a base URL and storing it inside your class using self... and now Base url is a class variable( as its under a class not any method)...self.base_url(becomes a variable inside your class)
    Browser_Header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" #This is a HTTP request header...It tells the website: “Who is making the request?”...When you do: requests.get(url) Websites like Wikipedia check Is this a real browser? Or a bot/script? ...Without headers Website may Block you, Return limited data,Detect you as a bot...."User-Agent" A special key in HTTP headers(It identifies the client (browser/app))...Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 This string mimics a real browser
    } 

    def scrape_state_data(self,state_name): #we can also use def scrape_state(self,state_name) then we have to use  @staticmethod keyword... self — is it necessary to make this as a instance method, ....without  self it will be static method and then we have to use  @staticmethod keyword to convert the static method to instance method and here self means WikipediaScraper class...and self is useing to access Base_Url and Headers
        Full_Url = self.Base_Url + state_name #we can also use url = WikipediaScraper.BASE_URL + state_name.... You cannot use Base_Url directly because it is not a local variable...You must access it through self/ class name... as Base_Url is a class variable so we can also acces it using "url = WikipediaScraper.BASE_URL"
        logger.info(f"Scraping {state_name}") #show state name whose data is scrapping

        try:
            Get_data_from_page = requests.get(url=Full_Url,headers=self.Browser_Header,timeout=10) #Send a request to a website and get the webpage data...requests.get(...) Fetch/download data from a URL...headers sent Extra information telling I am a browser not a bot...timeout=10 max wait...response = requests.get(url)(You ONLY downloaded the page,No filtering,No cleaning)
            Get_data_from_page.raise_for_status() #raises exception

            Convert_page_data_to_tree_structure = BeautifulSoup(Get_data_from_page.content, "html.parser") #If I already used requests.get() to get data, why do I need BeautifulSoup? ans : requests.get() gives you raw HTML but BeautifulSoup helps you to extract data from that HTML(by converting the downloded HTML into a tree structure)...response.content is the raw HTML of the webpage and html.parser Use Python’s HTML parser to converted HTML into a tree structure...BEFORE (raw) ("<html><body><p>Hello</p></body></html>") but AFTER (parsed tree) (html └─> body└── p → "Hello" )...
            
            Find_content_from_div = Convert_page_data_to_tree_structure.find("div",{"id":"mw-content-text"}) #Find the main content section of the Wikipedia page from <div> part....find(...) Find the FIRST HTML element that matches the condition(there's high chance that it might in div dection)...{'id': 'mw-content-text'} This is a filter condition (dictionary) it Find a <div> whose id is "mw-content-text"

            if not Find_content_from_div : #Check content existence..
                logger.error(f"No content found of {state_name}") #means not found
                return None
            
            Find_content_from_p = Find_content_from_div.find_all("p") #Find all (<p>) tags inside the main content section(div section) and return a list ([ <p>Kerala is a state...</p>, <p>It is known for...</p>, <p>It has culture...</p> ] )

            Contents_of_the_page = ""    #Store all paragraph( <p> ) texts and join them into one big string with line breaks
            for content in Find_content_from_p: 
                paragraph_text = content.get_text() # extract text from <p> tags (removes HTML tags)
                Contents_of_the_page = Contents_of_the_page + paragraph_text + "\n"

            Full_content_of_the_page = f"# {state_name.replace('_',' ')}\n\n{Contents_of_the_page}" #remove _ between state name (Tamil_Nadu to Tamil Nadu)...and it looks like (# Tamil Nadu ...Text...)
            time.sleep(1)
            return Full_content_of_the_page
        
        except Exception as e:
            logger.error(f"Error scraping {state_name} : {e}")
            return None
        
    def scrape_all_state_data(self):
        DATA_DIR.mkdir(parents=True,exist_ok=True) #Why are we using it here where we not use in scrape_state_data()? because here we are using with open(DATA_DIR / f"{state}.txt", "w") as f:

        data_of_all_state = {} #This will store results like {"Kerala": "...text...","Gujarat": "...text..."}

        for state in self.Indian_States: #Goes through each state one by one
            
            state_data = self.scrape_state_data(state) #Call scraper for each state

            if state_data:
                data_of_all_state[state] = state_data #Store the scraped data of a state inside a dictionary (Think of it like { key: value } )

                with open(DATA_DIR / f"{state}.txt","w",encoding="utf-8") as f: #Open (or create) a file , so I can write data into it...open(...) used to Open a file so we can read or write (open("file.txt", "w"))...DATA_DIR / f"{state}.txt" This part creates the file path...(with ... as f means Open file and assign it to variable f )...Automatically closes file after use
                    f.write(state_data) #Writes text into file
        
        logger.info(f"Scraped {len(data_of_all_state)} state information") #len(all_data) → number of successful states
        return data_of_all_state