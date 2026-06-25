import chromadb
import json
from rag.retriever import get_user_context, get_job_context
from agents.profiler import ProjectProfiler

# 1. Initialize the persistent ChromaDB client
db_client = chromadb.PersistentClient(path="./chroma_db")

# 2. Retrieve the contexts
print("Retrieving context from ChromaDB...")
user_ctx = get_user_context("What are my core technical projects and engineering skills?")
job_ctx = get_job_context("What are the primary technical requirements for this position?")

# 3. Instantiate Phase 4 Profiler and generate the card
print("Initializing Profiler Agent and calling Claude API...")
profiler = ProjectProfiler(chroma_client=db_client)
player_card = profiler.build_player_card(user_ctx, job_ctx)

# 4. Print the result
print("\n========== GENERATED PLAYER CARD ==========")
if player_card:
    print(json.dumps(player_card, indent=2))
else:
    print("ERROR: Player card generation failed or returned None.")