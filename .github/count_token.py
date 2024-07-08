import tiktoken
import prompts
from infer_user_query import *

def calculate_token_and_cost(user_query, bot_response):
    
    prompt_token_count          = num_tokens_from_string(user_query, "p50k_base")
    chat_completion_token_count = num_tokens_from_string(bot_response, "p50k_base")
    total_tokens                = (prompt_token_count + chat_completion_token_count)
    token_cost                  = (0.002 * total_tokens)
    
    return total_tokens, token_cost