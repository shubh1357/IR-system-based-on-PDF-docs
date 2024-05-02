# IR-system-based-on-PDF-docs
## Description
Information retreval and response / (RAG) based on local documents (llm_papers.zip) using openAI embedding and chroma Vector Database.  
##### Note: For testing One can use precreated vector DB with 15 PDF files for sample i.e., chroma1.zip file
Go through below process by installing dependencies and how to run to execute on your system.  

## Dependencies
##### Create OpenAI account and get an API key for the same.
### Prequisite libraries
##### OpenAi
install using - `pip install openai`
##### langchain
install using - `pip install langchain`
##### tiktoken
install using - `pip install tiktoken`
##### chromadb
install using - `pip install --upgrade chromadb==0.4.14`
##### tesseract binary file
for linux env - `apt-get install libleptonica-dev tesseract-ocr libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn`
##### pytesseract
install using  - `pip install pytesseract`
##### poppler
for linux env - `apt-get install poppler-utils`
##### unstructured
install using - `pip install "unstructured[pdf]"`  
## How to run
#### Step1
Import Configure_Create_Database class using - `from Configure_Create_Database import *`
#### Step2
create configure_create_database object with parameters  
          1. database path, where database will be stored  
          2. Directory path, directory where pdfs are stored  
          3. openapi api key  
**sample:**   
          `db = configure_create_database(DB_PATH,DATA_PATH,OpenApi_apikey)`  
**Note : incase running on collab, link your drive using  
         `from google.colab import drive`  
         `drive.mount("/content/drive")`  
       your path would be "./drive/MyDrive/<folder_name>"**
#### Step3
Call the class function in this order  
          1. `db.load_docs()`  
          2. `db.doc_splitter()`  
          3. `db.save_db()`  
This will store the embedding on the database location
#### Step4
Import Query_processing  
          `from Query_processing import *`  
create Query_processing object with parameters  
          1. database path, where database is stored from the previous step.  
          2. openapi api key  
**Sample:**  
          `query_rep = query_processing(DB_PATH,openapi_key)`  
if you are using the precreated db (chroma1.zip) unzip it, your DB_PATH = './chroma1'
#### Step5
Call the function as shown below  
          1. `query_rep.load_db()`  
          2. `query_rep.query_db(query_string)` -> will return 3 variables  
                a. prompt - top 3 matching chuncks  
                b. response - response for the query  
                c. source - set of source documents refered for the promopts and response.   
