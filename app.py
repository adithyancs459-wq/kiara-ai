import streamlit as st
from google import genai
from google.genai import types

# Page Customization (Just Kiara!)
st.set_page_config(page_title="Kiara AI", page_icon="🎙️", layout="centered")

# Custom CSS for Alexa Premium Interface
st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; }
    h1 { color: #00A8E8; font-family: 'Poppins', sans-serif; text-align: center; font-size: 3rem; }
    .stChatMessage { border-radius: 20px; padding: 12px; margin-bottom: 10px; }
    .alexa-mic { text-align: center; margin: 25px 0; }
    .stChatInput { border-radius: 25px; }
    </style>
""", unsafe_allow_html=True)

# ⚠️ നാളെ നമ്മൾ കണ്ടുപിടിക്കുന്ന AIzaSy കീ ഇവിടെയാണ് ഇടേണ്ടത്:
GEMINI_API_KEY = "IVIDE_PUTHIYA_KEY_IDUKA"

st.title("Kiara AI")
st.caption("<p style='text-align: center;'>Your voice companion. Click the mic and speak!</p>", unsafe_allow_html=True)

if not GEMINI_API_KEY or GEMINI_API_KEY == "IVIDE_PUTHIYA_KEY_IDUKA":
    st.warning("🔑 Please add your valid Gemini API Key inside the code tomorrow!")
    st.stop()

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying old chats
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─── VOICE INPUT (MICROPHONE) ───
st.markdown("<div class='alexa-mic'>", unsafe_allow_html=True)
audio_value = st.audio_input("Click to Speak")
st.markdown("</div>", unsafe_allow_html=True)

user_query = ""

if text_input := st.chat_input("Type here..."):
    user_query = text_input

if audio_value:
    with st.spinner("Listening... 🎧"):
        try:
            audio_bytes = audio_value.read()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                    "The user is speaking to you. Reply back to them like a best friend in Manglish or English."
                ]
            )
            user_query = "[Voice Message]"
            ai_response = response.text
        except Exception as e:
            st.error(f"Audio processing error: {e}")
            user_query = ""

if user_query:
    if user_query != "[Voice Message]":
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.messages.append({"role": "user", "content": user_query})
        
        config = types.GenerateContentConfig(
            system_instruction="Your name is Kiara. You are an Alexa-like personal AI friend. Chat in Manglish or English."
        )
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_query,
            config=config
        )
        ai_response = response.text

    with st.chat_message("assistant"):
        st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Alexa Voice Reply
        with st.spinner("Speaking... 🔊"):
            try:
                audio_config = types.GenerateContentConfig(
                    response_mime_type="audio/mp3",
                    system_instruction="Read this text aloud with a friendly female voice like Alexa: " + ai_response
                )
                voice_response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=ai_response,
                    config=audio_config
                )
                st.audio(voice_response.text, autoplay=True)
            except Exception as e:
                pass