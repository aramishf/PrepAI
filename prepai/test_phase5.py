import json
import chromadb
from rag.retriever import get_user_context, get_job_context
from agents.profiler import ProjectProfiler
from agents.interviewer import InterviewerAgent

# Initialize DB and generate the underlying player card from Phase 4
db_client = chromadb.PersistentClient(path="./chroma_db")
user_ctx = get_user_context("What are my core technical projects and engineering skills?")
job_ctx = get_job_context("What are the primary technical requirements for this position?")

profiler = ProjectProfiler(chroma_client=db_client)
player_card = profiler.build_player_card(user_ctx, job_ctx)

# Initialize Phase 5 Interviewer Agent
print("Initializing Interviewer Agent...")
interviewer = InterviewerAgent()

print("\n--- SIMULATING QUESTION SCRIPT ---")
# Test Question 1 (Intro)
q1 = interviewer.generate_question(player_card, question_number=1)
print(f"\n[Question 1]: {q1}")

# Test Question 2 (Deep Dive on Project)
q2 = interviewer.generate_question(player_card, question_number=2)
print(f"\n[Question 2]: {q2}")

# Test Question 5 (Targeting Skill Gaps)
q5 = interviewer.generate_question(player_card, question_number=5)
print(f"\n[Question 5]: {q5}")