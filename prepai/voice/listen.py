import streamlit as st
import streamlit.components.v1 as components
import requests
from voice.listen_server import start_flask

# Variable to track if Flask background thread has been launched
flask_server_started = False

def render_voice_input() -> str | None:
    """
    Renders the browser-based mic capture page via an iframe, polls the local
    Flask server for voice transcripts, and displays a text area fallback below.
    
    Returns:
        str | None: The final transcript string if submitted, otherwise None.
    """
    global flask_server_started
    
    # 1. Start the local Flask server on first call if not started yet
    if not flask_server_started:
        try:
            start_flask()
            flask_server_started = True
        except Exception as e:
            st.error(f"Error starting local voice server: {e}")

    st.write("### Speak Your Answer")
    
    # 2. Render the mic capture page inside a sandboxed iframe with microphone permissions allowed
    components.iframe("http://127.0.0.1:5050", height=220)

    # 3. Poll Flask server for any newly submitted transcript
    voice_value = None
    try:
        response = requests.get("http://127.0.0.1:5050/transcript", timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            voice_value = data.get("transcript")
    except Exception as e:
        # Silently ignore polling network failures to prevent UI crashing
        pass

    # If voice value is received, save it to session state so it populates the text area
    if voice_value:
        st.session_state.text_fallback_value = voice_value

    # Initialize fallback state
    if "text_fallback_value" not in st.session_state:
        st.session_state.text_fallback_value = ""

    # 4. Text Area Fallback
    user_typed = st.text_area(
        "Or type your answer here:",
        value=st.session_state.text_fallback_value,
        key="text_fallback",
        height=150
    )

    # Submission logic
    submitted = st.button("Submit Answer", key="submit_answer_btn")

    # If transcript has been populated via voice, we can auto-submit or let the user click submit
    if submitted or (voice_value and not user_typed):
        final_answer = user_typed.strip() if user_typed.strip() else (voice_value.strip() if voice_value else "")
        if final_answer:
            # Reset fallback state value
            st.session_state.text_fallback_value = ""
            return final_answer

    return None
