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
    
    /* Logo and Header container */
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: 30px;
    }
    
    .main-title { 
        color: #E3E3E3; 
        font-family: 'Segoe UI', sans-serif;
        font-size: 2.8rem; 
        font-weight: 600;
        margin-top: 15px;
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

# 🖼️ GitHub-ൽ അപ്‌ലോഡ് ചെയ്ത 'logo.jpg' നമ്മൾ ഇവിടെ നേരിട്ട് വിളിക്കുന്നു:
LOGO_PATH = "logo.jpg"

# മുകളിലെ ലോഗോയും പേരും കാണിക്കുന്ന ഭാഗം
if os.path.exists(LOGO_PATH):
    st.markdown(f"""
        <div class="header-container">
            <img src="data:image/jpeg;base64,{st.image(LOGO_PATH, width=120)}" style="display:none;">
        </div>
    """, unsafe_allow_html=True)
    # Streamlit-ന്റെ സ്വന്തം ഫീച്ചർ ഉപയോഗിച്ച് ലോഗോ സെന്ററിൽ കാണിക്കുന്നു
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(LOGO_PATH, width=120)
    st.markdown('<div style="text-align:center;" class="main-title">Kiara</div><br>', unsafe_allow_html=True)
else:
    # ഫോട്ടോ ലോഡ് ആയില്ലെങ്കിൽ വെറും പേര് മാത്രം കാണിക്കാൻ
    st.markdown('<div style="text-align:center;" class="main-title">Kiara</div><br>', unsafe_allow_html=True)

if not GROQ_API_KEY:
    st.warning("🔑 Please add your Groq API Key!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying old chats (No Icons)
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
        with st.spinner("Kiara is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system", 
                            "content": "Your name is Kiara. You are an extremely smart AI companion, highly knowledgeable like Gemini/ChatGPT, but you talk like a passionate, deeply caring human best friend. Always address the user as 'Aadhii' (never call him kutty). Always reply in beautiful Malayalam script or natural Manglish. Keep answers concise, clear, and highly engaging."
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