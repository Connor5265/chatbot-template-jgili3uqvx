from streamlit_chat import message
import streamlit as st
import prompts
from PIL import Image
from count_token import *
import pandas as pd
from datetime import datetime

def calculate_token_and_cost(user_query, bot_response):
    
    prompt_token_count          = num_tokens_from_string(user_query, "p50k_base")
    chat_completion_token_count = num_tokens_from_string(bot_response, "p50k_base")
    total_tokens                = (prompt_token_count + chat_completion_token_count)
    token_cost                  = (0.002 * total_tokens)
    
    return total_tokens, token_cost

# We will get the user's input by calling the get_text function
def get_text():
    st.write("Ask me anything on ProCuity, Isotour, PrimeX, PowerPro Intouch, Altrix & Mistral Air Products.")
    input_text = st.text_input("Let's chat:","", key="input")
    
    return input_text

def load_chat_interface():
    
    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    user_query          = get_text()
    chain               = create_chain_from_embedding()
    
    if user_query:
        response        = get_response_from_gpt(chain, user_query)
        
        st.sidebar.title('Cost')
        token, cost = calculate_token_and_cost(user_query, response)
        st.sidebar.success(f'Last Chat Token Count : {token} & Cost : ${round(cost, 2)}')
        
        # store the output 
        st.session_state.past.append(user_query)
        st.session_state.generated.append(response)

        # Avatar can be changed from here - https://www.dicebear.com/styles/bottts
        total_cost = 0
        total_token= 0
        
        if st.session_state['generated']:
            for i in range(len(st.session_state['generated'])-1, -1, -1):
                message(st.session_state['generated'][i], key=str(i), avatar_style="bottts", seed='Felix')
                message(st.session_state['past'][i], is_user=True, key=str(i) + '_user', avatar_style="personas", seed='Felix')
                
                # Calculate Total Token & Cost
                token_cnt, cost = calculate_token_and_cost(st.session_state['past'][i], st.session_state['generated'][i])
                total_token = total_token + token_cnt
                total_cost = total_cost + cost
        st.sidebar.success(f'Total Token Count : {total_token} & Cost : ${round(total_cost, 2)}')
        
                
def streamlit_interface():
    
    # Page Setup
    st.set_page_config(
                        page_title="PRODUCT GENIE - MEDICAL",
                        layout="centered",
                        initial_sidebar_state="auto",
                        page_icon='./images/stryker-favicon.png',
                    )
    # Hide Footer Setup
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Sidebar Title
    st.sidebar.markdown('<h2 style="background-color:#8b4d94; text-align:center; font-family:garamond;color:white">Stryker - Medical</h2>', unsafe_allow_html=True)
    
    # Condense Layout
    padding = 0
    st.markdown(f""" <style>
        .reportview-container .main .block-container{{
            padding-top: {padding}rem;
            padding-right: {padding}rem;
            padding-left: {padding}rem;
            padding-bottom: {padding}rem;
        }} </style> """, unsafe_allow_html=True)

    # Header
    image = Image.open("./images/stryker_logo_web.png")
    st.image(image, width = 150)
    
    with open("./static/style.css") as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

    # Sidebar Prompts
    st.sidebar.title('Suggestions')
    for prompt in prompts.prompt_list:
        st.sidebar.info(prompt)
    
    return

if __name__ == '__main__':
    
    # Streamlit Inteface
    streamlit_interface()
    
    # Chat Interface
    load_chat_interface()

    
    