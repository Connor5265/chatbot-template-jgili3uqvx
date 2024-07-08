import os
from dotenv import find_dotenv, load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain
from langchain.llms import AzureOpenAI
import config
from langchain.vectorstores import FAISS
import tiktoken

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

# Environment Variables
os.environ["OPENAI_API_TYPE"]         = os.getenv("OPENAI_API_TYPE")
os.environ["OPENAI_API_VERSION"]      = os.getenv("OPENAI_API_VERSION")
os.environ["OPENAI_API_BASE"]         = os.getenv("OPENAI_API_BASE")
os.environ["OPENAI_API_KEY"]          = os.getenv("OPENAI_API_KEY")
# azure_open_ai_deployment_name         = "athena-gpt-35"
azure_open_ai_deployment_name         = "daVinci3"

def num_tokens_from_string(string: str, encoding_name: str) -> int:

    """Returns the number of tokens in a text string."""

    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    
    return num_tokens

def get_response_from_gpt(chain, query):    
    
    ''' Function to respond to user query '''
    
    # query_result = chain({"question": query}, return_only_outputs=True)
    
    return chain.run(query)

def create_chain_from_embedding():
    
    embeddings          = OpenAIEmbeddings(chunk_size=1)
    faiss_training_db   = FAISS.load_local(os.path.join(config.vector_db_location,"faiss_index"), embeddings)
    chain               = RetrievalQA.from_chain_type(
                                                llm=AzureOpenAI(deployment_name=azure_open_ai_deployment_name), 
                                                chain_type='stuff', 
                                                retriever=faiss_training_db.as_retriever()
                                            )
    return chain

if __name__ == '__main__':
    
    usr_query       = input('Whats your questions ?')

    chain           = create_chain_from_embedding()
    response        = get_response_from_gpt(chain, usr_query)
    print(response)
    
    # Analytics:
    token_count     = num_tokens_from_string(usr_query, "p50k_base")
    token_cost      = (0.002 * token_count)
    print("Token Count : ", token_count, "Cost : $", token_cost)