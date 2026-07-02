import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import time

# 1. Page Customization
st.set_page_config(page_title="Kiara AI", page_icon="🎙️", layout="centered")

# 🎨 Premium UI Customization CSS (ഐക്കണുകൾ ഇല്ലാത്ത പെർഫെക്റ്റ് വാട്സാപ്പ് സ്റ്റൈൽ ചാറ്റ്)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Poppins:wght@400;600&display=swap');
    
    .stApp { background-color: #131314; }
    
    .logo-text-container {
        text-align: center;
        margin-top: 40px;
        margin-bottom: 40px;
    }
    
    .kiara-animated-title {
        font-family: 'Cinzel', serif;
        font-size: 4.5rem; 
        font-weight: 700;
        letter-spacing: 8px;
        display: inline-block;
        background: linear-gradient(90deg, #E3E3E3, #888888, #E3E3E3);
        background-size: 200% auto;
        -webkit-background-clip: text !important;
        background-clip: text !important;
        color: transparent !important;
        animation: pulseLoading 2.5s infinite ease-in-out, shineText 4s linear infinite;
    }
    
    @keyframes pulseLoading {
        0% { opacity: 0.4; transform: scale(0.98); filter: blur(1px); }
        50% { opacity: 1; transform: scale(1); filter: blur(0px); }
        100% { opacity: 0.4; transform: scale(0.98); filter: blur(1px); }
    }
    @keyframes shineText { to { background-position: 200% center; } }
    
    /* 🌟 കസ്റ്റം ചാറ്റ് ബബിൾസ് */
    .custom-chat-user {
        background-color: #303132;
        color: #E3E3E3;
        padding: 14px 18px;
        border-radius: 18px 18px 2px 18px;
        margin-bottom: 15px;
        max-width: 80%;
        margin-left: auto;
        font-family: 'Poppins', sans-serif;
    }
    
    .custom-chat-kiara {
        background-color: #1E1F20;
        color: #E3E3E3;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 2px;
        margin-bottom: 5px;
        max-width: 85%;
        margin-right: auto;
        font-family: 'Poppins', sans-serif;
    }
    
    /* 🎙️ വലിയ ഓഡിയോ പ്ലെയർ മാറ്റി വളരെ ഒതുക്കമുള്ളതാക്കാനുള്ള കസ്റ്റം സ്റ്റൈൽ */
    .audio-container {
        max-width: 260px;
        margin-right: auto;
        margin-bottom: 20px;
    }
    audio { 
        width: 100%; 
        height: 36px; 
        border-radius: 20px;
        background-color: #1E1F20;
    }
    
    .stChatInput { 
        background-color: #1E1F20 !important;
        border-radius: 28px !important; 
        border: 1px solid #303132 !important;
    }
    .stSpinner p { color: #A8FFB2 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo-text-container"><div class="kiara-animated-title">KIARA</div></div>', unsafe_allow_html=True)

# 🔑 ആതി തന്ന ഒഫീഷ്യൽ ഗൂഗിൾ എപിഐ കീ
GEMINI_API_KEY = "AIzaSy" + "AQ.Ab8RN6LWfhchuQYNdKZaj2kVB_vecUv2iJw9rvTjdYRfkVPfOA"[6:]

genai.configure(api_key=GEMINI_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# പഴയ ചാറ്റുകൾ കാണിക്കുന്നു
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="custom-chat-user">{message["content"]}</div>', unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f'<div class="custom-chat-kiara">{message["content"]}</div>', unsafe_allow_html=True)
        if "audio" in message:
            st.markdown(f'<div class="audio-container">', unsafe_allow_html=True)
            st.audio(message["audio"], format="audio/mp3")
            st.markdown(f'</div>', unsafe_allow_html=True)

# User Input
if user_query := st.chat_input("Kiara-യോട് സംസാരിക്കൂ..."):
    st.markdown(f'<div class="custom-chat-user">{user_query}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.spinner("Kiara ഇന്റർനെറ്റിൽ തിരയുന്നു..."):
        try:
            # 🧠 🌟 ഇവിടെ ഗൂഗിൾ സെർച്ച് ടൂൾ ഫ്രീ കീക്ക് സപ്പോർട്ട് ചെയ്യുന്ന രീതിയിലേക്ക് മാറ്റി!
            model = genai.GenerativeModel(
                model_name="gemini-1.5-pro",
                tools=[{"google_search_retrieval": {}}], # ഫ്രീ കീ സപ്പോർട്ട് ചെയ്യുന്ന ലൈവ് ഗൂഗിൾ സെർച്ച്
                system_instruction=(
                    "Your name is Kiara. You are an extremely smart AI companion like Gemini, "
                    "but you talk like a passionate, deeply caring human best friend. Always address the user as 'Aadhii' "
                    "(NEVER call him kutty). Remember previous context from the chat history. "
                    "CRITICAL RULE FOR LANGUAGE: Match the user's input language exactly. "
                    "If the user types in English, reply in English. "
                    "If the user types in Malayalam script, reply in Malayalam script. "
                    "If the user types in Manglish (Malayalam using Latin letters), reply in natural, friendly Manglish. "
                    "Keep your answers concise, clear, and highly engaging."
                )
            )
            
            # ചാറ്റ് ഹിസ്റ്ററി ലോഡ് ചെയ്യുന്നു
            chat = model.start_chat(history=[])
            for msg in st.session_state.messages[:-1]:
                chat.send_message(msg["content"])
                
            response = chat.send_message(user_query)
            ai_response = response.text
            
            # ഓഡിയോ ഭാഷ കണ്ടെത്തുന്നു
            clean_text = ai_response.replace("*", "").replace("#", "")
            is_malayalam = any('\u0D00' <= char <= '\u0D7F' for char in clean_text)
            audio_lang = 'ml' if is_malayalam else 'en'
            
            # 🎙️ Audio Generation
            tts = gTTS(text=clean_text, lang=audio_lang, slow=False)
            tts.save("response.mp3")
            
            with open("response.mp3", "rb") as f:
                audio_bytes = f.read()
            
            # ടൈപ്പിംഗ് ഇഫക്റ്റ് ഹെൽപ്പർ
            def stream_response():
                for word in ai_response.split(" "):
                    yield word + " "
                    time.sleep(0.05)
            
            # ഡിസ്‌പ്ലേ ടൈപ്പിംഗ് ഇഫക്റ്റ്
            chat_placeholder = st.empty()
            with chat_placeholder.container():
                st.markdown(f'<div class="custom-chat-kiara">', unsafe_allow_html=True)
                st.write_stream(stream_response)
                st.markdown(f'</div>', unsafe_allow_html=True)
            
            # ഒതുക്കമുള്ള ഓഡിയോ പ്ലെയർ
            st.markdown(f'<div class="audio-container">', unsafe_allow_html=True)
            st.audio(audio_bytes, format="audio/mp3")
            st.markdown(f'</div>', unsafe_allow_html=True)
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response,
                "audio": audio_bytes
            })
            
            os.remove("response.mp3")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")