import streamlit as st
import json
import PyPDF2
import requests
from bs4 import BeautifulSoup
from graph.orchestrator import InterviewGraph
from rag.ingest import store_chunks_in_collection

DEFAULT_RESUME = """Aramish Farooq
San Jose, CA | farooqaramish@gmail.com | 925-503-9167 | https://www.linkedin.com/in/aramishfarooq/ |
https://portfolio-website-sepia-seven-12.vercel.app/
PROFESSIONAL SUMMARY
Computer engineering student at San Jose State University with hands-on experience building ML models, autonomous AI agents,
and real-time computer vision systems. Proficient in Python, C++, and a broad set of AI/ML frameworks. Backed by two
internships at Pacific Northwest National Laboratory and a portfolio of projects spanning agents, RAG systems, and embedded AI.
EDUCATION
San Jose State University
B.S. in Computer Engineering. 12/2026
Diablo Valley College
Computer Science / Math. 12/2024
EXPERIENCE
Machine Learning Researcher Intern 01/2025 – 05/2025
Pacific Northwest National Laboratory
•
Engineered 80+ input features to train Random Forest, XGBoost, and LSTM models predicting aerosol size distributions.
•
Created detailed visualizations of particle behavior (10 nm - 3 um) to guide environmental impact assessments.
Machine Learning / AI Engineer Intern 08/2024 – 12/2024
Pacific Northwest National Laboratory
•
Achieved a 15% improvement in aerosol concentration predictions using supervised ML models in Python (XGBoost, LSTM).
•
Built a Tkinter GUI deployed to researchers for real-time aerosol predictions, processing 5,000+ data points.
AI/LLM Evaluator 12/2025 – Present
Handshake
•
Evaluating advanced AI models through human-in-the-loop analysis. Reviewing model reasoning to ensure accuracy.
Private Math Tutor 08/2024 – 12/2024
Diablo Valley College
•
Elevated student performance in Calculus I/II and Algebra by 15-20% through targeted, concept-based instruction.
Computer Hardware Specialist 01/2018 – Present
Independent
•
Designed and assembled 15+ high-performance gaming systems; executed hardware diagnostics and stability benchmarking.
PROJECTS
GitHub PR Automation Agent
•
Built an autonomous software agent using LangGraph and LangChain that reviews pull requests, identifies code vulnerabilities,
and automatically writes optimized refactors.
RAG Research AI Assistant System
•
Developed an AI assistant using RAG, Chroma DB, and LLaMA 3 for automated, citation-backed analysis documentation.
Silent Voice Bridge
•
Engineered a real-time edge AI translator processing continuous video via PyTorch and OpenCV on an NVIDIA Jetson Orin
Nano to translate ASL hand gestures into English text.
SpartanSat (NASA CubeSat Project)
•
Developing computer vision models on NVIDIA Jetson to recognize and synthetically illuminate the dark side of
lunar crescents to improve autonomous navigation systems.
Custom PCB Audio Amplifier
•
Designed an analog amplifier in KiCad with optimized trace routing; hand-soldered and debugged hardware.
SKILLS
Languages: Python, C, C++, Verilog
AI / ML / Agents: LangGraph, LangChain, RAG, Chroma DB, PyTorch, YOLOv8, Scikit-learn, XGBoost, LSTM
Computer Vision: OpenCV , MediaPipe, Image Processing
Data Science: NumPy, Pandas, Matplotlib
Software & Tools: Docker, Git, GitHub, Linux, Next.js
Hardware: FPGA, Vivado, NVIDIA Jetson, KiCad, PCB Design"""

DEFAULT_JD = """Job description
What to Expect

Tesla is seeking exceptional Machine Learning Interns to help build large scale models to drive the future of autonomy across all current and future generations of Tesla AI products. You will work on a lean team without boundaries and have access to one of the world’s largest training clusters with a data engine that constantly generates new information for improving our models. Most importantly, you will see your work repeatedly shipped to and utilized by millions of Tesla’s customers.

We are seeking Interns in the following AI disciplines:
• Train large-scale foundation and generative models that are optimized for performance and latency
• Improve data engine for large scale and high-quality dataset curation
• Reinforcement Learning for instilling objectives and improving overall robustness, including RL for training
• Design compound AI systems for better planning and reasoning, with emphasis on world modeling and generative videos

What You'll Do
• Applied research in the areas of Foundation Models, including but not limited to computer vision, large language models and generative modeling
• Work on cutting-edge techniques in AI - multi-task learning, video networks, multi-modal generative models, imitation learning, reinforcement learning, semi-supervised learning, self-supervised learning
• Explore and implement novel AI tooling and techniques for efficient training and fine-tuning of large-scale models, incorporating RL for training
• Leverage millions of miles of driving data and interventions to build a robust and scalable end-to-end learning based self-driving system
• Collaborate with a team to apply research findings to real-world challenges, ensuring high-quality system integration within existing platforms
• Experiment with data generation and network driven data collection approaches to enhance the diversity and quality of training data, including generative videos
• Ship production quality, safety-critical software to the entirety of Tesla’s vehicle fleet, with applications in world modeling

What You'll Bring
• Demonstrated experience in machine learning frameworks and models such as PyTorch, TensorFlow, GPT, CNNs, and generative models
• Strong experience with Python and software engineering best practices
• Experience with one or more of imitation Learning, reinforcement learning (offline/off-policy), modern neural network architectures (e.g., GPT, diffusion, generative models), or related techniques, including RL for training
• An “under the hood” knowledge of deep learning: layer details, loss functions, optimization, etc.
• Prior experience with sparse training techniques, neural network pruning, and generative modeling, with exposure to generative videos
• Experience with training large models on distributed computing
• Ability to work on complex problems and produce significant research and/or experience deploying production ML models at scale, particularly in world modeling
• Proven track record of innovations and executions in deep learning, demonstrated with shipping products or first-author publications at leading AI conferences"""

def render_progress_pills(current_turn: int, max_turns: int, is_complete: bool):
    pills_html = []
    for i in range(1, max_turns + 1):
        if is_complete or i < current_turn:
            color = "#21c354"  # Green
        elif i == current_turn:
            color = "#1c83e1"  # Blue
        else:
            color = "#d3d3d3"  # Gray
            
        pills_html.append(
            f'<div style="width: 30px; height: 10px; background-color: {color}; border-radius: 5px; margin-right: 5px; display: inline-block;"></div>'
        )
        
    pills_div = f'<div style="display: flex; flex-direction: row; margin-bottom: 20px;">{"".join(pills_html)}</div>'
    
    if is_complete:
        st.markdown(f"### Interview Complete ({max_turns} Questions)")
    else:
        st.markdown(f"### Question {current_turn} of {max_turns}")
    st.markdown(pills_div, unsafe_allow_html=True)

def render_score_bar(label: str, value: int):
    if value <= 4:
        color = "#ff4b4b" # Red
    elif value <= 7:
        color = "#ffaa00" # Amber
    else:
        color = "#21c354" # Green
        
    st.markdown(
        f"""
        <div style="margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 14px;">
                <strong>{label}</strong>
                <span>{value}/10</span>
            </div>
            <div style="width: 100%; background-color: #f0f2f6; border-radius: 5px; height: 10px;">
                <div style="width: {value * 10}%; background-color: {color}; height: 10px; border-radius: 5px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="AI Interview Coach", layout="wide")
st.title("🤖 AI Interview Coach")

# Initialize graph and configuration exactly once per session
if "graph" not in st.session_state:
    st.session_state.graph = InterviewGraph()
    # We use a static thread_id for this single-user prototype session
    st.session_state.config = {"configurable": {"thread_id": "session_1"}}

if "started" not in st.session_state:
    st.session_state.started = False

# Screen 1: Start Interview
if not st.session_state.started:
    st.markdown("### Welcome to the AI Interview Coach")
    st.write("Upload your resume (.pdf or .txt) or use the default to start a simulated technical interview.")
    
    resume_option = st.radio("How would you like to provide your resume?", ["Use Default Resume", "Upload PDF/TXT"])
    resume_text = ""
    
    if resume_option == "Use Default Resume":
        resume_text = DEFAULT_RESUME
        st.success("✅ Using default resume.")
    else:
        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    text = []
                    for page in pdf_reader.pages:
                        text.append(page.extract_text() or "")
                    resume_text = "\n".join(text)
                    st.success(f"✅ Successfully extracted text from {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
            else:
                resume_text = uploaded_file.getvalue().decode("utf-8")
                st.success(f"✅ Successfully read {uploaded_file.name}")
            
    st.markdown("### Job Description")
    jd_option = st.radio("How would you like to provide the job description?", ["Use Default Job Description", "Upload PDF/TXT", "Paste URL", "Paste Raw Text"])
    
    job_desc_text = ""
    
    if jd_option == "Use Default Job Description":
        job_desc_text = DEFAULT_JD
        st.success("✅ Using default job description.")
    elif jd_option == "Upload PDF/TXT":
        jd_file = st.file_uploader("Upload Job Description", type=["pdf", "txt"], key="jd_upload")
        if jd_file is not None:
            if jd_file.name.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(jd_file)
                    text = []
                    for page in pdf_reader.pages:
                        text.append(page.extract_text() or "")
                    job_desc_text = "\n".join(text)
                    st.success(f"✅ Successfully extracted text from {jd_file.name}")
                except Exception as e:
                    st.error(f"Error reading PDF: {e}")
            else:
                job_desc_text = jd_file.getvalue().decode("utf-8")
                st.success(f"✅ Successfully read {jd_file.name}")
    elif jd_option == "Paste URL":
        jd_url = st.text_input("Job Description URL")
        if jd_url:
            try:
                response = requests.get(jd_url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                job_desc_text = soup.get_text(separator=' ', strip=True)
                st.success("✅ Successfully extracted text from URL")
            except Exception as e:
                st.error(f"Error fetching URL: {e}")
    else:
        job_desc_text = st.text_area("Paste Job Description", height=200)

    turns = st.slider("Number of Questions", min_value=1, max_value=5, value=2)
    
    if st.button("Start Interview", disabled=not resume_text or not job_desc_text):
        with st.spinner("Analyzing resume, job description, and generating first question..."):
            # Chunk and store the job description in job_context collection
            words = job_desc_text.split()
            chunks = []
            start_idx = 0
            while start_idx < len(words):
                end_idx = start_idx + 200
                chunks.append(' '.join(words[start_idx:end_idx]))
                start_idx += (200 - 20)
                if end_idx >= len(words):
                    break
            
            if chunks:
                try:
                    store_chunks_in_collection("job_context", chunks)
                except Exception as e:
                    st.error(f"Error storing job description: {e}")
            
            initial_state = {
                "candidate_name": "Candidate",
                "resume_text": resume_text.strip(),
                "player_card": {},
                "interview_history": [],
                "evaluation_scores": [],
                "turn_count": 0,
                "max_turns": turns
            }
            # Start the graph. It will run profiler, then interviewer, and pause before human_input
            st.session_state.graph.app.invoke(initial_state, st.session_state.config)
            st.session_state.started = True
            st.rerun()

# Screen 2: The Interview Chat Interface
else:
    # Get the current state from the LangGraph checkpointer
    state_snapshot = st.session_state.graph.app.get_state(st.session_state.config)
    state_values = state_snapshot.values
    history = state_values.get("interview_history", [])
    scores = state_values.get("evaluation_scores", [])
    max_turns = state_values.get("max_turns", 5)
    current_turn = state_values.get("turn_count", 0) + 1
    is_complete = not state_snapshot.next
    
    with st.sidebar:
        st.header("📊 Live Report Panel")
        if scores:
            dimensions = ["relevance", "specificity", "star_completeness", "confidence", "accuracy", "impact"]
            avg_overall = sum(s.get("overall_score", 0) for s in scores) / len(scores)
            st.metric("Overall Average Score", f"{avg_overall:.1f}/10")
            
            dim_avgs = {dim: sum(s.get(dim, 0) for s in scores) / len(scores) for dim in dimensions}
            lowest_dim = min(dim_avgs, key=dim_avgs.get)
            st.warning(f"📉 Lowest Dimension: **{lowest_dim.replace('_', ' ').title()}** ({dim_avgs[lowest_dim]:.1f}/10)")
            
            patterns = []
            for s in reversed(scores):
                w = s.get("weakness", "")
                if w and w not in patterns:
                    patterns.append(w)
                if len(patterns) >= 3:
                    break
            
            st.markdown("### 🔍 Top Patterns Found")
            if not patterns:
                st.write("No distinct patterns yet.")
            for i, p in enumerate(patterns, 1):
                st.markdown(f"{i}. {p}")
                
            if not state_snapshot.next:
                st.markdown("---")
                st.markdown("### 🚀 30-Day Action Plan")
                st.success(f"Primary Focus: **{lowest_dim.replace('_', ' ').title()}**")
                st.markdown("**Week 1-2: Foundation**\n- Review the STAR method structure.\n- Focus on addressing the specific question asked.")
                st.markdown("**Week 3: Technical Depth**\n- Practice weaving specific tools, constraints, and metrics into answers.")
                st.markdown("**Week 4: Polish**\n- Work on delivering answers with confidence and clarity.")
        else:
            st.info("Answer the first question to see your live report!")

    # Render progress indicator
    render_progress_pills(current_turn, max_turns, is_complete)
    st.divider()

    # Render chat history
    st.markdown("### Interview Transcript")
    for i, msg in enumerate(history):
        role = "assistant" if msg["role"] == "interviewer" else "user"
        with st.chat_message(role):
            st.write(msg["content"])
            
            # If it's a candidate answer, let's also show the Evaluator's score for it (if available)
            if role == "user":
                turn_idx = i // 2
                if turn_idx < len(scores):
                    score = scores[turn_idx]
                    with st.expander("👀 View Claude's Secret Evaluation"):
                        render_score_bar("Relevance", score.get("relevance", 0))
                        render_score_bar("Specificity", score.get("specificity", 0))
                        render_score_bar("STAR Completeness", score.get("star_completeness", 0))
                        render_score_bar("Confidence", score.get("confidence", 0))
                        render_score_bar("Accuracy", score.get("accuracy", 0))
                        render_score_bar("Impact", score.get("impact", 0))
                        render_score_bar("Overall Score", score.get("overall_score", 0))
                        
                        st.markdown("---")
                        st.markdown(f"**💪 Strength:** {score.get('strength', '')}")
                        st.markdown(f"**🎯 Weakness:** {score.get('weakness', '')}")
    
    # Check if we are paused at the human_input node
    if state_snapshot.next and "human_input" in state_snapshot.next:
        user_input = st.chat_input("Type your answer here...")
        
        if user_input:
            # 1. Update the state with the candidate's answer
            new_history = history + [{"role": "candidate", "content": user_input}]
            st.session_state.graph.app.update_state(
                st.session_state.config, 
                {"interview_history": new_history}
            )
            
            # 2. Resume the graph (it will execute human_input, then evaluator, then loop)
            with st.spinner("Evaluating your answer and thinking of the next question..."):
                st.session_state.graph.app.invoke(None, st.session_state.config)
            st.rerun()
            
    # Check if graph has reached END
    elif not state_snapshot.next:
        st.success("🎉 Interview Complete! Check the expanders above to see your scores.")
        if st.button("Restart Interview"):
            st.session_state.clear()
            st.rerun()
