import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import base64

# 1. Page Customization
st.set_page_config(page_title="Kiara AI", page_icon="🎙️", layout="centered")

# 🎨 Premium UI Customization CSS (റോബോട്ട് ഐക്കൺ ഇല്ലാത്ത ക്ലീൻ ചാറ്റ്)
st.markdown("""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Poppins:wght@400;600&display=swap');
    
    .stApp { background-color: #131314; }
    
    .logo-text-container {
        text-align: center;
        margin-top: 40px;
        margin-bottom: 40px;
    }
    
    /* ലോഡിങ് പൾസ് ആнимаേഷൻ ടൈറ്റിൽ */
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
    
    /* 🌟 കസ്റ്റം ചാറ്റ് ബോക്സ് ഡിസൈൻ (ഒരു ഐക്കണും ഉണ്ടാകില്ല) */
    .custom-chat-user {
        background-color: #303132;
        color: #E3E3E3;
        padding: 14px 18px;
        border-radius: 18px 18px 2px 18px;
        margin-bottom: 15px;
        max-width: 80%;
        margin-left: auto; /* യൂസർ മെസ്സേജ് വലതുവശത്ത് */
        font-family: 'Poppins', sans-serif;
    }
    
    .custom-chat-kiara {
        background-color: #1E1F20;
        color: #E3E3E3;
        padding: 14px 18px;
        border-radius: 18px 18px 18px 2px;
        margin-bottom: 15px;
        max-width: 85%;
        margin-right: auto; /* കിആര മെസ്സേജ് ഇടതുവശത്ത് */
        font-family: 'Poppins', sans-serif;
        position: relative;
    }
    
    /* സ്പീക്കർ ഐക്കൺ സ്റ്റൈൽ */
    .audio-inline-btn {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1.2rem;
        margin-left: 10px;
        vertical-align: middle;
    }
    
    .stChatInput { 
        background-color: #1E1F20 !important;
        border-radius: 28px !important; 
        border: 1px solid #303132 !important;
    }
    .stSpinner p { color: #A8FFB2 !important; }
    </style>
""", unsafe_allow_html=True)

# ടൈറ്റിൽ
st.markdown('<div class="logo-text-container"><div class="kiara-animated-title">KIARA</div></div>', unsafe_allow_html=True)

# 🔑 Groq API Key
GROQ_API_KEY = "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"

if not GROQ_API_KEY:
    st.warning("🔑 Please add your Groq API Key!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# പഴയ ചാറ്റുകൾ ഐക്കൺ ഇല്ലാതെ ഡിസ്‌പ്ലേ ചെയ്യുന്നു
for idx, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f'<div class="custom-chat-user">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        # കിആരയുടെ മെസ്സേജ്
        st.markdown(f'<div class="custom-chat-kiara">{message["content"]}</div>', unsafe_allow_html=True)
        if "audio" in message:
            # വലിയ പ്ലെയറിന് പകരം ക്ലീൻ ആയി ചെറിയ ഒരു ഓഡിയോ ബാർ മാത്രം കാണിക്കുന്നു
            st.audio(message["audio"], format="audio/mp3")

# User Input
if user_query := st.chat_input("Kiara-യോട് സംസാരിക്കൂ..."):
    # യൂസർ മെസ്സേജ് കാണിക്കുന്നു
    st.markdown(f'<div class="custom-chat-user">{user_query}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Kiara's Response
    with st.spinner("Kiara ആലോചിക്കുന്നു..."):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Your name is Kiara. You are an extremely smart AI companion like Gemini, "
                            "but you talk like a passionate, deeply caring human best friend. Always address the user as 'Aadhii' "
                            "(NEVER call him kutty). "
                            "CRITICAL RULE FOR LANGUAGE: Match the user's input language exactly. "
                            "If the user types in English, reply in English. "
                            "If the user types in Malayalam script, reply in Malayalam script. "
                            "If the user types in Manglish (Malayalam using Latin letters), reply in natural, friendly Manglish. "
                            "Keep your answers concise, clear, and highly engaging."
                        )
                    },
                    {"role": "user", "content": user_query}
                )
            )
            ai_response = response.choices[0].message.content
            
            # ഓഡിയോ ഭാഷ കണ്ടെത്തുന്നു
            clean_text = ai_response.replace("*", "").replace("#", "")
            is_malayalam = any('\u0D00' <= char <= '\u0D7F' for char in clean_text)
            audio_lang = 'ml' if is_malayalam else 'en'
            
            # 🎙️ Audio Generation
            tts = gTTS(text=clean_text, lang=audio_lang, slow=False)
            tts.save("response.mp3")
            
            with open("response.mp3", "rb") as f:
                audio_bytes = f.read()
            
            # കിആരയുടെ മറുപടി ഡിസ്‌പ്ലേ ചെയ്യുന്നു
            st.markdown(f'<div class="custom-chat-kiara">{ai_response}</div>', unsafe_allow_html=True)
            st.audio(audio_bytes, format="audio/mp3") # പ്ലെയർ ചെറുതാക്കി താഴെ വെച്ചു
            
            st.session_state.messages.append({
                "role": "assistant", 
                "content": ai_response,
                "audio": audio_bytes
            })
            
            os.remove("response.mp3")
            st.rerun() # ചാറ്റ് ബോക്സ് കൃത്യമായി അപ്‌ഡേറ്റ് ചെയ്യാൻ
            
        except Exception as e:
            st.error(f"Error: {e}")