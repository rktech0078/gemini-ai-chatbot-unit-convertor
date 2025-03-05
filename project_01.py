import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY") 

# API URL
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="https://imgproxy.attic.sh/5hURQUpXqihw4XlriaeP7i5ZbVF7QV3J5qxNpMVr1xo/rs:fit:128:128:1:1/t:1:FF00FF:false:false/pngo:false:true:256/aHR0cHM6Ly9hdHRp/Yy5zaC9ydW5wb2Qv/MTc4ZGIyYWMtMDUz/OC00MTJhLTllMWYt/YjE0ZDU5YTkwMjUz/LnBuZw.png"  ,
    layout="wide",
    initial_sidebar_state="expanded"
)



# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .chat-container {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stMarkdown {
        font-size: 16px;
    }
    div.stButton > button {
        border-radius: 20px;
        padding: 10px 25px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://media.licdn.com/dms/image/v2/D4E03AQFXfQe5Tnr32Q/profile-displayphoto-shrink_800_800/B4EZTQ6VWxGYAg-/0/1738671741728?e=1746057600&v=beta&t=GdPzW412NxSh7hBXfMOcrTyi1cUsyOZkcFlzyo_6D8E", width=100)
    st.title("Chat Settings")
    
    # Model selection
    model = st.selectbox(
        "Choose Mistral Model",
        ["mistral-small", "mistral-medium", "mistral-large"],
        index=1
    )
    
    # Chat preferences
    st.subheader("Preferences")
    show_timestamps = st.checkbox("Show Timestamps", value=True)
    enable_markdown = st.checkbox("Enable Markdown", value=True)
    
    
    # About section
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This is an enhanced AI chatbot powered by Mistral AI and Abdul Rafay Khan. Use it to get intelligent responses to your questions.")
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 14px;'>
        © 2025 <b>Abdul Rafay Khan</b>. All rights reserved.<br>
        This chatbot and its contents are protected by copyright law.<br>
        Unauthorized use or reproduction is strictly prohibited.
    </div>
    """, unsafe_allow_html=True)

st.success("Built with ❤️ by Abdul Rafay Khan | [Source Code](https://github.com/rktech0078)")
# Copyright notice


# Main chat interface
st.title(" 🌐  AI Assistant")
st.markdown("Welcome! I'm your AI assistant powered by **Abdul Rafay Khan**. How can I help you today?")
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
st.markdown("### Chat History")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])
        if show_timestamps and "timestamp" in msg:
            st.caption(f"Sent at {msg['timestamp']}")

# User input
user_input = st.chat_input("Type your message here...")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": st.session_state.get("current_time", "")
    })

    # Show typing indicator
    with st.spinner("AI is thinking..."):
        # Call Mistral API
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": user_input}]
        }
        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            bot_reply = response.json()["choices"][0]["message"]["content"]
        else:
            bot_reply = "⚠️ Error: Unable to get response from Mistral API, our engineers resolve the issue soon. Please try again."

    # Add bot message to chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply,
        "timestamp": st.session_state.get("current_time", "")
    })

    # Display bot reply
    with st.chat_message("assistant", avatar="🤖"):
        if enable_markdown:
            st.markdown(bot_reply)
        else:
            st.write(bot_reply)

# Footer
# st.markdown("---")
# st.markdown(
#     """
#     <div style='text-align: center; color: #666;'>
#         <p>Built with ❤️ using Streamlit and Mistral AI</p>
#     </div>
#     """,
#     unsafe_allow_html=True
# )
