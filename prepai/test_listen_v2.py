import streamlit as st
import time
from voice.listen import render_voice_input

# Page layout configuration
st.set_page_config(page_title="PrepAI Voice Input Test V2", layout="centered")
st.title("🎙️ PrepAI Voice Input Test V2")
st.write("Test the Flask-based local standalone voice capturer below.")

# 1. Start Flask background server if not already running in this session
if "flask_server_started" not in st.session_state:
    from voice.listen_server import start_flask
    try:
        start_flask()
        st.session_state.flask_server_started = True
    except Exception as e:
        st.error(f"Error starting local voice server: {e}")
        st.session_state.flask_server_started = False

# 2. Render the mic iframe and poll for updates
result = render_voice_input()

# 3. Handle returned transcript
if result:
    st.success(f"✅ You said: {result}")
else:
    # If waiting for input, delay 1 second and rerun the app to poll Flask again
    time.sleep(1)
    st.rerun()
