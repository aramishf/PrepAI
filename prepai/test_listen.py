import streamlit as st
from voice.listen import render_voice_input

# Page Configuration Setup
st.set_page_config(page_title="PrepAI voice input Test", layout="centered")
st.title("🎙️ PrepAI Voice input Test")
st.write("Perform a speak-to-text test using the microphone button or the fallback input box below.")

# Render voice input component + text area fallback
result = render_voice_input()

# Display the transcript returned by the voice input helper on submission
if result:
    st.success(f"🎉 **You said / typed**: {result}")
