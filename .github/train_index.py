import os
from io import BytesIO
from dotenv import find_dotenv, load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import config
from time import perf_counter

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Environment Variables
os.environ["OPENAI_API_TYPE"]         = os.getenv("OPENAI_API_TYPE")
os.environ["OPENAI_API_VERSION"]      = os.getenv("OPENAI_API_VERSION")
os.environ["OPENAI_API_BASE"]         = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"]          = os.getenv("OPENAI_API_KEY")

def train_brochure_data(training_data_location, vector_db_location):
    
    ''' Function to create Vector database thru Chroma DB ''' 
    
    start_time = perf_counter()
            
    # Load the training data
    loader = PyPDFDirectoryLoader(training_data_location)
    documents = loader.load()
    
    # Split Text
    text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    # Create Word Chain
    embeddings      = OpenAIEmbeddings(chunk_size=1)
    doc_search      = FAISS.from_documents(texts, embeddings)
    
    # Create Persistant Vector DB
    doc_search.save_local(os.path.join(vector_db_location,"faiss_index"))
    
    # Performance Timing
    end_time = perf_counter()
    run_time = end_time - start_time
    
    print('Indexing Complete with run time :', run_time)
    
    return
    
if __name__ == '__main__':
    
    train_brochure_data(config.training_data_location, config.vector_db_location)
    
    