import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# Thread-safe storage for the latest transcript
latest_transcript = None
transcript_lock = threading.Lock()

# Standalone HTML page with the SpeechRecognition client
HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>PrepAI Voice Capture</title>
  <style>
    body {
      margin: 0;
      padding: 16px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: #0F172A;
      color: #E2E8F0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      box-sizing: border-box;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      padding: 12px 24px;
      font-size: 15px;
      font-weight: 600;
      color: #0F172A;
      background-color: #38BDF8;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      outline: none;
      transition: background-color 0.2s, transform 0.1s;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .btn:hover {
      background-color: #7DD3FC;
    }
    .btn:active {
      transform: scale(0.98);
    }
    .recording {
      color: #FFFFFF;
      background-color: #EF4444;
    }
    .recording:hover {
      background-color: #F87171;
    }
    .dot {
      width: 10px;
      height: 10px;
      background-color: #FFFFFF;
      border-radius: 50%;
      margin-right: 10px;
      display: inline-block;
    }
    .recording .dot {
      animation: pulse 1.2s infinite;
    }
    @keyframes pulse {
      0% { opacity: 0.3; transform: scale(0.9); }
      50% { opacity: 1; transform: scale(1.1); }
      100% { opacity: 0.3; transform: scale(0.9); }
    }
    #transcript {
      margin-top: 14px;
      font-size: 13.5px;
      color: #94A3B8;
      font-style: italic;
      text-align: center;
      max-width: 90%;
      line-height: 1.4;
      min-height: 38px;
    }
    .error {
      color: #EF4444;
      margin-top: 14px;
      font-size: 13.5px;
      font-weight: 500;
    }
    .success {
      color: #10B981;
      margin-top: 14px;
      font-size: 13.5px;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <button id="record-btn" class="btn">🎤 Click to speak your answer</button>
  <div id="status-msg"></div>
  <div id="transcript"></div>

  <script>
    const recordBtn = document.getElementById("record-btn");
    const transcriptDiv = document.getElementById("transcript");
    const statusDiv = document.getElementById("status-msg");

    let recognition = null;
    let isRecording = false;
    let finalTranscript = "";

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      recordBtn.disabled = true;
      statusDiv.className = "error";
      statusDiv.innerText = "Use Chrome for voice. Type below instead.";
    } else {
      recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        isRecording = true;
        recordBtn.innerHTML = '<span class="dot"></span>🔴 Recording... click to stop';
        recordBtn.classList.add("recording");
        transcriptDiv.innerText = "";
        statusDiv.className = "";
        statusDiv.innerText = "";
        finalTranscript = "";
      };

      recognition.onresult = (event) => {
        let interimTranscript = "";
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }
        transcriptDiv.innerText = finalTranscript + interimTranscript;
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        statusDiv.className = "error";
        if (event.error === 'not-allowed') {
          statusDiv.innerText = "Mic access denied. Type below.";
        } else {
          statusDiv.innerText = "Error: " + event.error + ". Type below.";
        }
        stopRecording();
      };

      recognition.onend = () => {
        stopRecording();
        if (finalTranscript.trim()) {
          submitTranscript(finalTranscript.trim());
        }
      };
    }

    function startRecording() {
      if (recognition) {
        try {
          recognition.start();
        } catch (e) {
          console.error(e);
        }
      }
    }

    function stopRecording() {
      if (isRecording) {
        isRecording = false;
        recordBtn.innerHTML = '🎤 Click to speak your answer';
        recordBtn.classList.remove("recording");
        if (recognition) {
          recognition.stop();
        }
      }
    }

    function submitTranscript(text) {
      statusDiv.className = "";
      statusDiv.innerText = "Submitting...";
      
      fetch("/transcript", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ transcript: text })
      })
      .then(response => {
        if (response.ok) {
          statusDiv.className = "success";
          statusDiv.innerText = "✅ Answer submitted successfully!";
        } else {
          statusDiv.className = "error";
          statusDiv.innerText = "Submission failed.";
        }
      })
      .catch(err => {
        console.error(err);
        statusDiv.className = "error";
        statusDiv.innerText = "Connection error.";
      });
    }

    recordBtn.addEventListener("click", () => {
      if (isRecording) {
        stopRecording();
      } else {
        startRecording();
      }
    });
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    """Serves the standalone mic-capture HTML page."""
    return HTML_PAGE

@app.route("/transcript", methods=["POST"])
def post_transcript():
    """Receives and stores final transcript from the client browser."""
    global latest_transcript
    data = request.get_json()
    if data and "transcript" in data:
        with transcript_lock:
            latest_transcript = data["transcript"]
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid payload"}), 400

@app.route("/transcript", methods=["GET"])
def get_transcript():
    """Returns the latest stored transcript to Streamlit and clears it."""
    global latest_transcript
    with transcript_lock:
        temp = latest_transcript
        latest_transcript = None  # Clear once read to prevent replay loops
    return jsonify({"transcript": temp}), 200

def start_flask():
    """Starts the Flask server on localhost:5050 in a daemon thread."""
    flask_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=5050, debug=False, use_reloader=False),
        daemon=True
    )
    flask_thread.start()
