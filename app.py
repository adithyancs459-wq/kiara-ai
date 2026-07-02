import streamlit as st
from groq import Groq

# Page Customization (Just Kiara!)
st.set_page_config(page_title="Kiara AI", page_icon="🎙️", layout="centered")

# Custom CSS for Alexa Premium Interface
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; }
    h1 { color: #00A8E8; font-family: 'Poppins', sans-serif; text-align: center; font-size: 3rem; }
    .stChatMessage { border-radius: 20px; padding: 12px; margin-bottom: 10px; }
    .stChatInput { border-radius: 25px; }
    </style>
""", unsafe_allow_html=True)

# 🔑 Groq API Key
GROQ_API_KEY = "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"

st.title("Kiara")

if not GROQ_API_KEY:
    st.warning("🔑 Please add your Groq API Key!")
    st.stop()

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying old chats
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Text Input
if user_query := st.chat_input("Type here..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # AI Response Logic (Using super fast & latest Llama 3.3)
    with st.chat_message("assistant"):
        with st.spinner("Kiara is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Your name is Kiara. You are an Alexa-like personal AI friend. Chat passionately and friendly in Manglish or English like a human best friend."},
                        {"role": "user", "content": user_query}
                    ]
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Error: {e}")