import os
import streamlit as st
from groq import Groq
from gtts import gTTS

# 1. Page Customization
st.set_page_config(page_title="Kiara AI", page_icon="🎙️", layout="centered")

# 🎨 Gemini Premium Layout CSS
st.markdown("""
    <style>
    .stApp { background-color: #131314; }
    
    /* Logo and Title inline വരാൻ വേണ്ടിയുള്ള container */
    .header-inline {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px; 
        margin-top: 20px;
        margin-bottom: 30px;
    }
    
    /* വെള്ള ബാക്ക്ഗ്രൗണ്ട് ഒഴിവാക്കാനുള്ള ഡിസൈൻ */
    .header-inline img {
        width: 70px; 
        height: auto;
        border-radius: 8px; 
        mix-blend-mode: multiply; /* 🌟 വെള്ള ബാക്ക്ഗ്രൗണ്ട് തനിയെ മായും */
    }
    
    .main-title-inline { 
        color: #E3E3E3; 
        font-family: 'Segoe UI', sans-serif;
        font-size: 3rem; 
        font-weight: 600;
    }
    
    /* Clean Chat Box (No Avatars) */
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

# 🖼️ GitHub-ൽ നീ ഇട്ട ലോഗോ
LOGO_PATH = "logo.jpg"

# ലോഗോയും പേരും മുകളിൽ കാണിക്കുന്ന ഭാഗം
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    if os.path.exists(LOGO_PATH):
        # GitHub-ൽ logo.jpg ഉണ്ടെങ്കിൽ അത് ഇന്റർനെറ്റ് ലിങ്കിലേക്ക് മാപ്പ് ചെയ്ത് കാണിക്കുന്നു
        st.markdown(f"""
            <div class="header-inline">
                <img src="https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main/logo.jpg" onerror="this.src='https://i.postimg.cc/mDCHw6fS/1000027547.jpg'">
                <div class="main-title-inline">Kiara</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="main-title-inline" style="text-align:center;">Kiara</div>', unsafe_allow_html=True)

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
                # 🧠 ഇവിടെയാണ് പേരും (Aadhii) മലയാളം ടൈപ്പിംഗും കൺട്രോൾ ചെയ്യുന്നത്
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