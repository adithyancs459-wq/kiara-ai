import streamlit as st
from groq import Groq
from gtts import gTTS
import os

# 1. Page Customization
st.set_page_config(page_title="Kiara AI", page_icon="🎙️", layout="centered")

# 🎨 Premium Google Font & Text-Logo Effect CSS
st.markdown("""
    /* Luxury Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Poppins:wght@400;600&display=swap');
    
    <style>
    .stApp { background-color: #131314; }
    
    /* 🌟 അക്ഷരങ്ങൾക്കുള്ളിൽ ലോഗോ വരാനുള്ള മാസ്സ് CSS */
    .logo-text-container {
        text-align: center;
        margin-top: 25px;
        margin-bottom: 35px;
    }
    
    .kiara-logo-title {
        font-family: 'Cinzel', serif; /* പ്രീമിയം ഫോണ്ട് സ്റ്റൈൽ */
        font-size: 4.5rem; /* നല്ല വലിപ്പമുള്ള അക്ഷരങ്ങൾ */
        font-weight: 700;
        letter-spacing: 6px;
        display: inline-block;
        color: transparent; /* അക്ഷരങ്ങളുടെ സ്വന്തം കളർ മാറ്റി സുതാര്യമാക്കുന്നു */
        background-image: url('https://i.postimg.cc/mDCHw6fS/1000027547.jpg');
        background-size: cover;
        background-position: center;
        -webkit-background-clip: text; 
        background-clip: text;
    }
    
    /* Clean Chat Box (No Avatars) */
    .stChatMessage { 
        background-color: #1E1F20 !important;
        border-radius: 16px !important; 
        padding: 16px !important; 
        margin-bottom: 15px !important; 
        color: #E3E3E3 !important;
        font-family: 'Poppins', sans-serif;
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

# മുകളിൽ 'KIARA' എന്ന അക്ഷരങ്ങളിൽ ലോഗോ സെറ്റ് ചെയ്യുന്നു
st.markdown("""
    <div class="logo-text-container">
        <div class="kiara-logo-title">KIARA</div>
    </div>
""", unsafe_allow_html=True)

# Groq API Key സെറ്റിങ്സ്
GROQ_API_KEY = "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"

if not GROQ_API_KEY:
    st.warning("🔑 Please add your Groq API Key!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying old chats
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=None):
        st.markdown(message["content"])
        if "audio" in message:
            st.audio(message["audio"], format="audio/mp3")

# User Input
if user_query := st.chat_input("Kiara-യോട് സംസാരിക്കൂ..."):
    with st.chat_message("user", avatar=None):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Kiara's Response
    with st.chat_message("assistant", avatar=None):
        with st.spinner("Kiara മറുപടി ആലോചിക്കുന്നു..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Your name is Kiara. You are an extremely smart AI companion like Gemini, but you talk like a passionate, deeply caring human best friend. Always address the user as 'Aadhii' (NEVER call him kutty). STRICTLY reply only in beautiful Malayalam script (മലയാളം ലിപിയിൽ മാത്രം മറുപടി നൽകുക). Never use Manglish or English text for replies. Keep answers concise, clear, and highly engaging."
                        },
                        {"role": "user", "content": user_query}
                    ]
                )
                ai_response = response.choices[0].message.content
                
                # 🎙️ Audio Generation
                clean_text = ai_response.replace("*", "").replace("#", "")
                tts = gTTS(text=clean_text, lang='ml', slow=False)
                tts.save("response.mp3")
                
                with open("response.mp3", "rb") as f:
                    audio_bytes = f.read()
                
                st.markdown(ai_response)
                st.audio(audio_bytes, format="audio/mp3")
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": ai_response,
                    "audio": audio_bytes
                })
                
                os.remove("response.mp3")
                
            except Exception as e:
                st.error(f"Error: {e}")