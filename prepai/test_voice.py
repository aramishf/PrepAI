import streamlit as st
from voice.speak import speak_text

# Page Layout Setup
st.set_page_config(page_title="PrepAI Voice Test", layout="centered")
st.title("🎙️ PrepAI Voice Test")
st.write("Click the button below to test the browser SpeechSynthesis API voice feature.")

# Single trigger button for the test case
if st.button("Test Speak Text"):
    # Speak the required confirmation message
    message = "Voice is working. PrepAI interview coach is ready."
    st.write(f"🔊 Playing message: *\"{message}\"*")
    speak_text(message, enabled=True)
