import json
from agents.evaluator import EvaluatorAgent

def main():
    print("Initializing Evaluator Agent...")
    evaluator = EvaluatorAgent()

    # 1. Create a mock player card
    player_card = {
        "user_strengths": ["Python backend development", "Vector Databases", "System Architecture"],
        "user_projects": ["AI Interview Coach with multi-agent architecture and RAG", "Microservices Migration"],
        "skill_gaps": ["Front-end frameworks", "Cloud deployment at massive scale"],
        "recommended_question_focus": ["RAG optimization", "Agent coordination", "Database scaling"],
        "role_level": "mid",
        "company_culture_signals": ["Data-driven", "Ownership", "Technical rigor"]
    }

    # 2. Specific technical question
    question = (
        "In your AI Interview Coach project, you chose ChromaDB as your vector database for the RAG pipeline. "
        "Walk me through a specific scenario where you had to optimize retrieval performance when the context store grew, "
        "and explain why you didn't choose alternatives like Pinecone or Weaviate, especially considering "
        "the multi-agent architecture where multiple agents might be querying the vector store simultaneously."
    )

    print("\n" + "="*50)
    print("QUESTION ASKED:")
    print(question)
    print("="*50 + "\n")

    # 3. Test Answer A: Weak
    weak_answer = (
        "So basically I built the microservices platform, and we used React for the frontend which was cool. "
        "I think vector databases are pretty fast anyway. We used Docker and stuff and it made things a lot faster "
        "for the team, I guess. I didn't really look into Pinecone much because Chroma was just there."
    )

    print("--- TESTING WEAK ANSWER ---")
    print(f"Candidate Answer:\n{weak_answer}\n")
    print("Evaluating with Claude...")
    
    weak_evaluation = evaluator.evaluate_answer(question, weak_answer, player_card)
    print("Evaluation Results:")
    print(json.dumps(weak_evaluation, indent=2))

    print("\n" + "="*50 + "\n")

    # 4. Test Answer B: Strong
    strong_answer = (
        "When our RAG context store exceeded 100,000 document chunks, we noticed retrieval latency spiking to over 800ms "
        "during concurrent agent queries. I diagnosed this by profiling the ChromaDB queries and realized our embedding "
        "dimensionality was unnecessarily high for our use case. I implemented a dimensionality reduction pipeline "
        "and switched from a flat index to an HNSW index, tuning the efConstruction parameter. This action brought "
        "our latency down to 110ms even under load from 5 concurrent agents. I chose ChromaDB over Pinecone because "
        "we needed an embedded, local-first solution to comply with data privacy constraints, and Weaviate was too heavy "
        "for our deployment footprint. The result was a highly responsive multi-agent system that processed interviews "
        "with sub-second latency."
    )

    print("--- TESTING STRONG ANSWER ---")
    print(f"Candidate Answer:\n{strong_answer}\n")
    print("Evaluating with Claude...")
    
    strong_evaluation = evaluator.evaluate_answer(question, strong_answer, player_card)
    print("Evaluation Results:")
    print(json.dumps(strong_evaluation, indent=2))

if __name__ == "__main__":
    main()
