import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY") or "f4JAFvDHZ7qkFEnbSMPPh74SMAVtzA2K"

# API URL
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Streamlit UI
st.title("🤖 Mistral AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask something...")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call Mistral API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-medium",  # You can use "mistral-small" or "mistral-large"
        "messages": [{"role": "user", "content": user_input}]
    }
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        bot_reply = response.json()["choices"][0]["message"]["content"]
    else:
        bot_reply = "Error: Unable to get response from Mistral API."

    # Add bot message to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Display bot reply
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
