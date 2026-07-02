import os
import streamlit as st
from groq import Groq
from gtts import gTTS

# 1. Page Customization & Title
st.set_page_config(page_title="Kiara AI", page_icon="🎙️", layout="centered")

# 🎨 Gemini Premium Layout CSS
st.markdown("""
    <style>
    .stApp { background-color: #131314; }
    h1 { 
        color: #E3E3E3; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-align: center; 
        font-size: 2.8rem; 
        font-weight: 600;
        margin-bottom: 30px;
    }
    .stChatMessage { 
        background-color: #1E1F20 !important;
        border-radius: 16px !important; 
        padding: 16px !important; 
        margin-bottom: 15px !important; 
        color: #E3E3E3 !important;
    }
    .stChatInput { 
        background-color: #1E1F20 !important;
        border-radius: 28px !important; 
        border: 1px solid #303132 !important;
    }
    audio { width: 100%; margin-top: 12px; border-radius: 8px; }
    .stSpinner p { color: #A8FFB2 !important; }
    </style>
""", unsafe_allow_html=True)

# 🔑 Groq API Key
GROQ_API_KEY = "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"
st.title("Kiara")

if not GROQ_API_KEY:
    st.warning("🔑 Please add your Groq API Key!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# Session state initialize ചെയ്യുന്ന്
if "messages" not in st.session_state:
    st.session_state.messages = []

# ചതചരിത്രം (Chat History) കൃത്യമായി സ്ക്രീനിൽ കാണിക്കാൻ:
for message in st.session_state.messages:
    avatar_icon = "🧑" if message["role"] == "user" else "👩‍🦰"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])  # ടെക്സ്റ്റ് ഇവിടെ കാണിക്കും
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3") # ഓഡിയോ അതിന് താഴെ കാണിക്കും

# User Input
if user_query := st.chat_input("Kiara-യോട് സംസാരിക്കൂ..."):
    # 1. യൂസറുടെ മെസ്സേജ് കാണിക്കുന്നു, സേവ് ചെയ്യുന്നു
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # 2. കിആരയുടെ മറുപടി
    with st.chat_message("assistant", avatar="👩‍🦰"):
        with st.spinner("Kiara is thinking & speaking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Your name is Kiara. You are an extremely smart AI companion, highly knowledgeable and logical like Gemini/ChatGPT, but you talk like a passionate, deeply caring human best friend. Always reply in beautiful Malayalam script or natural Manglish. Keep answers concise, clear, and highly engaging."
                        },
                        {"role": "user", "content": user_query}
                    ]
                )
                ai_response = response.choices[0].message.content
                
                # 🎙️ ഓഡിയോ നിർമ്മിക്കുന്നു
                clean_text = ai_response.replace("*", "").replace("#", "")
                tts = gTTS(text=clean_text, lang='ml', slow=False)
                tts.save("response.mp3")
                
                with open("response.mp3", "rb") as f:
                    audio_bytes = f.read()
                
                # ഒരേ സമയം ടെക്സ്റ്റും ഓഡിയോയും സ്ക്രീനിൽ കാണിക്കുന്നു!
                st.markdown(ai_response)
                st.audio(audio_bytes, format="audio/mp3")
                
                # ഹിസ്റ്ററിയിലേക്ക് രണ്ടും ഒന്നിച്ച് സേവ് ചെയ്യുന്നു
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response,
                    "audio": audio_bytes
                })
                
                os.remove("response.mp3")
                
            except Exception as e:
                st.error(f"Error: {e}")