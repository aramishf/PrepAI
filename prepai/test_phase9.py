import json
from graph.orchestrator import InterviewGraph

def main():
    print("Initializing Interview Graph...")
    graph = InterviewGraph()
    
    # Define a mock resume text
    resume_text = """
    Aramish Farooq
    Software Engineer
    
    Experience:
    - AI Interview Coach: Built a multi-agent AI system using Python, LangGraph, and Claude. Integrated ChromaDB for RAG pipeline.
    - Microservices Migration: Migrated a monolithic application to Python microservices with Flask and Docker, improving latency.
    
    Skills: Python, Docker, AI Agents, Vector Databases, System Architecture.
    """
    
    # Initialize state
    initial_state = {
        "candidate_name": "Aramish",
        "resume_text": resume_text.strip(),
        "player_card": {},
        "interview_history": [],
        "evaluation_scores": [],
        "turn_count": 0,
        "max_turns": 2
    }
    
    print("\nStarting Interview Simulation...")
    print("=" * 60)
    
    # Stream the graph execution using "values" mode to get the full state back at each step
    final_state = initial_state
    for state_update in graph.app.stream(initial_state, stream_mode="values"):
        # state_update contains the entire state at the current point
        final_state = state_update
        # The printing of nodes is handled inside the node functions themselves (e.g. print("[Node] run_profiler"))
    
    print("\n\n" + "=" * 60)
    print("                  FINAL INTERVIEW REPORT")
    print("=" * 60)
    
    history = final_state.get("interview_history", [])
    scores = final_state.get("evaluation_scores", [])
    
    # Group into Q&A turns
    turn_index = 0
    for i in range(0, len(history), 2):
        if i + 1 >= len(history):
            break
            
        question = history[i]["content"]
        answer = history[i+1]["content"]
        eval_score = scores[turn_index] if turn_index < len(scores) else {}
        
        print(f"\nTURN {turn_index + 1}")
        print("-" * 60)
        print(f"Q: {question}")
        print(f"A: {answer}")
        print("-" * 60)
        print("EVALUATION:")
        print(f"  Overall Score:     {eval_score.get('overall_score', 'N/A')}/10")
        print(f"  Relevance:         {eval_score.get('relevance', 'N/A')}/10")
        print(f"  Specificity:       {eval_score.get('specificity', 'N/A')}/10")
        print(f"  STAR Completeness: {eval_score.get('star_completeness', 'N/A')}/10")
        print(f"  Confidence:        {eval_score.get('confidence', 'N/A')}/10")
        print(f"  Accuracy:          {eval_score.get('accuracy', 'N/A')}/10")
        print(f"  Impact:            {eval_score.get('impact', 'N/A')}/10")
        print(f"\n  Strength: {eval_score.get('strength', 'N/A')}")
        print(f"  Weakness: {eval_score.get('weakness', 'N/A')}")
        
        turn_index += 1
        
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
