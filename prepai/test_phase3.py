from rag.retriever import get_user_context, get_job_context

# Test user context
print("--- USER CONTEXT TEST ---")
results = get_user_context("What projects have you built?", top_k=2)
print(results)

# Test job context
print("\n--- JOB CONTEXT TEST ---")
results = get_job_context("What technical skills does this role need?", top_k=2)
print(results)