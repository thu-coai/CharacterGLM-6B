"""
This is a demo of using Streamlit to build a CharacterGLM conversation.
The list of roles is defined in character.json, and each role contains the following fields:
- user_info: user information, can be null
- bot_info: robot information
- bot_name: robot name
- user_name: username, if user_info is null, the user_name params should set "user"
- greeting: robot's greeting

If you want to set a new character, you can add a new character in character.json.
Please note that your conversational patterns need to adapt to the model's training data formate.

"""
import os
import json
import streamlit as st
import torch
from transformers import AutoModel, AutoTokenizer

MODEL_PATH = os.environ.get('MODEL_PATH', 'LingxinAI/CharacterGLM2-6b')
TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)
with open('character.json', 'r', encoding='utf-8') as file:
    characters = json.load(file)

st.set_page_config(
    page_title="CharacterGLM-6B Streamlit Simple Demo",
    page_icon=":robot:",
    layout="wide"
)


@st.cache_resource
def get_model():
    tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
    model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True, device_map="auto").eval()
    return tokenizer, model


tokenizer, model = get_model()
# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "past_key_values" not in st.session_state:
    st.session_state.past_key_values = None
if "session_meta" not in st.session_state:
    st.session_state.session_meta = {
        "user_info": "",
        "bot_info": "",
        "bot_name": "",
        "user_name": ""
    }
if "character_choice" not in st.session_state:
    st.session_state["character_choice"] = None

def _init_session(character_choice, init_history: bool):
    if character_choice:
        character_data = characters[character_choice]
        st.session_state.session_meta["user_info"] = character_data["user_info"]
        st.session_state.session_meta["bot_info"] = character_data["bot_info"]
        st.session_state.session_meta["bot_name"] = character_data["bot_name"]
        st.session_state.session_meta["user_name"] = character_data["user_name"]
        greeting = character_data.get("greeting", "")
        
        if init_history:
            st.session_state.history = []
            if greeting:
                st.session_state.history.append(("", greeting))
            st.session_state.past_key_values = None

# Sidebar for character selection
st.sidebar.header("Select Character")
character_choice = st.sidebar.selectbox("Choose a character", list(characters.keys()))
update_character_choice = character_choice != st.session_state["character_choice"]
st.session_state["character_choice"] = character_choice
_init_session(character_choice, init_history=update_character_choice)

# Sidebar for model parameters
max_length = st.sidebar.slider("Max Length", 0, 4096, 2048, step=1)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 0.8, step=0.01)
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.9, step=0.01)
repetition_penalty = st.sidebar.slider("Repetition Penalty", 0.1, 2.0, 1.0, step=0.1)

# Button to clear
buttonClean = st.sidebar.button("清理会话历史", key="clean")
if buttonClean:
    _init_session(st.session_state["character_choice"], init_history=True)
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    st.rerun()

for i, (user_message, bot_response) in enumerate(st.session_state.history):
    if user_message:
        with st.chat_message(name="user", avatar="user"):
            st.text(user_message)
    if bot_response:
        with st.chat_message(name="assistant", avatar="assistant"):
            st.text(bot_response)

with st.chat_message(name="user", avatar="user"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="assistant"):
    message_placeholder = st.empty()

query = st.chat_input("开始对话吧")
if query:
    input_placeholder.text(query)
    history = st.session_state.history
    past_key_values = st.session_state.past_key_values
    for response, history, past_key_values in model.stream_chat(
            tokenizer=tokenizer,
            session_meta=st.session_state.session_meta,
            query=query,
            history=history,
            past_key_values=past_key_values,
            max_length=max_length,
            top_p=top_p,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            return_past_key_values=True,
    ):
        message_placeholder.text(response)
    st.session_state.history = history
    st.session_state.past_key_values = past_key_values
