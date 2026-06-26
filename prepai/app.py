import streamlit as st
import json
from graph.orchestrator import InterviewGraph

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
    st.write("Paste your resume below to start a simulated technical interview.")
    
    default_resume = """Aramish Farooq
Software Engineer
Experience:
- AI Interview Coach: Built a multi-agent AI system using Python, LangGraph, and Claude. Integrated ChromaDB for RAG pipeline.
- Microservices Migration: Migrated a monolithic application to Python microservices with Flask and Docker, improving latency.
Skills: Python, Docker, AI Agents, Vector Databases, System Architecture."""
    
    resume_text = st.text_area("Your Resume", value=default_resume, height=200)
    turns = st.slider("Number of Questions", min_value=1, max_value=5, value=2)
    
    if st.button("Start Interview"):
        with st.spinner("Analyzing resume and generating first question..."):
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
                        st.json(score)
    
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
