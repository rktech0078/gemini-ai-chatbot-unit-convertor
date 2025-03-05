import streamlit as st
import requests
import os
from dotenv import load_dotenv

# environment variables Load Karne kay liye
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY") or "f4JAFvDHZ7qkFEnbSMPPh74SMAVtzA2K"

# API URL (Mistral API Endpoint) hai
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Streamlit UI Kay Kuch Functions 
st.success("Made with ❤️ by Abdul Rafay Khan")
st.title("🤖 AI Chatbot And Unit Convertor")

# chat history Initialize Yha par hogi.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Pichle messages yha display hongay.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User se input yha par lengay. 
user_input = st.chat_input("Ask something...")
if user_input:
    #  user kay messages ko chat history may save karna 
    st.session_state.messages.append({"role": "user", "content": user_input})

    # loading state yha par show hogi
    with st.spinner("AI is thinking..."):
        # Calling Mistral API
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

    # AI kay messages ko chat history may add karna
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Yha AI ka response show hoga
    with st.chat_message("assistant"):
        st.markdown(bot_reply)



