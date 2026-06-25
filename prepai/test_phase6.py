import json
import chromadb
from rag.retriever import get_user_context, get_job_context
from agents.profiler import ProjectProfiler
from agents.interviewer import InterviewerAgent

# 1. Setup State
db_client = chromadb.PersistentClient(path="./chroma_db")
user_ctx = get_user_context("What are my core technical projects and engineering skills?")
job_ctx = get_job_context("What are the primary technical requirements for this position?")

profiler = ProjectProfiler(chroma_client=db_client)
player_card = profiler.build_player_card(user_ctx, job_ctx)

interviewer = InterviewerAgent()

# 2. Generate a baseline question
print("\n--- GENERATING QUESTION ---")
q2 = interviewer.generate_question(player_card, question_number=2)
print(f"Interviewer: {q2}")

# 3. Test a WEAK Answer
print("\n--- TESTING WEAK ANSWER ---")
weak_answer = "I built the microservices platform. I used Python and Docker and it made things a lot faster for the team."
print(f"Candidate: {weak_answer}")

weak_eval = interviewer.evaluate_and_followup(q2, weak_answer, player_card)
print("\nClaude Evaluation:")
print(json.dumps(weak_eval, indent=2))

# 4. Test a STRONG Answer
print("\n--- TESTING STRONG ANSWER ---")
strong_answer = "I led the migration to a Python microservices architecture using Flask and Docker. By decoupling the monolithic database and implementing proper caching, we reduced query latency from 800ms down to 120ms, which allowed us to scale to 10 million users without crashing."
print(f"Candidate: {strong_answer}")

strong_eval = interviewer.evaluate_and_followup(q2, strong_answer, player_card)
print("\nClaude Evaluation:")
print(json.dumps(strong_eval, indent=2))