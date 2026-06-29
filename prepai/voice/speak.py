import streamlit as st
import streamlit.components.v1 as components

def speak_text(text: str, enabled: bool = True) -> None:
    """
    Synthesizes and speaks text using the Web Speech API (SpeechSynthesis)
    in the client browser. Stops any active speech before starting.
    
    Args:
        text (str): The text content to read aloud.
        enabled (bool): Whether speech is enabled (muted if False).
    """
    # If disabled (mute mode), do nothing
    if not enabled or not text:
        return

    # Escape backticks and single quotes to prevent JS syntax/injection issues
    escaped_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("'", "\\'")

    # HTML and JavaScript component that accesses window.speechSynthesis
    js_code = f"""
    <script>
    (function() {{
        if ('speechSynthesis' in window) {{
            // Cancel any ongoing speech first
            window.speechSynthesis.cancel();

            const speak = () => {{
                const textToSpeak = `{escaped_text}`;
                const utterance = new SpeechSynthesisUtterance(textToSpeak);
                
                // Configure rate, pitch, and volume requirements
                utterance.rate = 0.92;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;

                const voices = window.speechSynthesis.getVoices();
                
                // Search for voices in the required order of preference
                const preferredNames = ["Google US English", "Alex", "Daniel", "Samantha"];
                let matchedVoice = null;
                
                for (const name of preferredNames) {{
                    matchedVoice = voices.find(v => v.name && v.name.includes(name));
                    if (matchedVoice) break;
                }}

                if (matchedVoice) {{
                    utterance.voice = matchedVoice;
                }}

                window.speechSynthesis.speak(utterance);
            }};

            // Check if voices are loaded (can be async/empty initially in some browsers)
            const loadedVoices = window.speechSynthesis.getVoices();
            if (loadedVoices.length === 0) {{
                window.speechSynthesis.onvoiceschanged = speak;
            }} else {{
                speak();
            }}
        }} else {{
            console.warn("Speech Synthesis is not supported in this browser.");
        }}
    }})();
    </script>
    """
    # Render component with height 0 so it stays invisible in UI
    components.html(js_code, height=0)
