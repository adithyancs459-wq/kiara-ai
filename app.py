import streamlit as st
from groq import Groq

# Page Customization
st.set_page_config(page_title="Kiara AI", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E14; }
    h1 { color: #00A8E8; font-family: 'Poppins', sans-serif; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 🔑 നിന്റെ കറക്റ്റ് Groq കീ ഞാൻ ഇവിടെ സെറ്റ് ചെയ്തിട്ടുണ്ട്
GROQ_API_KEY = "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"

st.title("Kiara")

if not GROQ_API_KEY:
    st.warning("🔑 Please add your Groq API Key!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_query := st.chat_input("Type here..."):
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    with st.chat_message("assistant"):
        with st.spinner("Kiara is thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[
                        {"role": "system", "content": "Your name is Kiara. You are a friendly AI companion. Reply in passionately friendly Manglish or English."},
                        {"role": "user", "content": user_query}
                    ]
                )
                ai_response = response.choices[0].message.content
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Error: {e}")