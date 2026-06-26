import sys
import os
from typing import TypedDict, List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents.profiler import ProjectProfiler
from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent

class InterviewState(TypedDict):
    candidate_name: str
    resume_text: str
    player_card: dict
    interview_history: list
    evaluation_scores: list
    turn_count: int
    max_turns: int

class InterviewGraph:
    def __init__(self):
        self.profiler = ProjectProfiler()
        self.interviewer = InterviewerAgent()
        self.evaluator = EvaluatorAgent()
        
        workflow = StateGraph(InterviewState)
        
        workflow.add_node("run_profiler", self.run_profiler)
        workflow.add_node("run_interviewer", self.run_interviewer)
        workflow.add_node("human_input", self.human_input)
        workflow.add_node("run_evaluator", self.run_evaluator)
        
        workflow.set_entry_point("run_profiler")
        workflow.add_edge("run_profiler", "run_interviewer")
        workflow.add_edge("run_interviewer", "human_input")
        workflow.add_edge("human_input", "run_evaluator")
        
        workflow.add_conditional_edges(
            "run_evaluator",
            self.should_continue,
            {
                "continue": "run_interviewer",
                "end": END
            }
        )
        
        # Add MemorySaver checkpointer for Human-in-the-loop
        memory = MemorySaver()
        self.app = workflow.compile(
            checkpointer=memory,
            interrupt_before=["human_input"]
        )

    def run_profiler(self, state: InterviewState) -> Dict[str, Any]:
        user_context = [{"text": state["resume_text"], "source": "resume", "chunk_index": 1}]
        job_context = [{"text": "Software Engineering role focusing on scalable architectures.", "source": "job_description", "chunk_index": 1}]
        
        player_card = self.profiler.build_player_card(user_context, job_context)
        return {"player_card": player_card}

    def run_interviewer(self, state: InterviewState) -> Dict[str, Any]:
        current_turn = state.get("turn_count", 0) + 1
        
        question = self.interviewer.generate_question(
            player_card=state["player_card"],
            question_number=current_turn
        )
        
        history = state.get("interview_history", []) + [{"role": "interviewer", "content": question}]
        return {"interview_history": history}

    def human_input(self, state: InterviewState) -> Dict[str, Any]:
        """
        This node gets interrupted BEFORE it runs. 
        When the UI resumes the graph, the answer is already injected into the state by Streamlit.
        We just increment the turn count here.
        """
        turn = state.get("turn_count", 0)
        return {"turn_count": turn + 1}

    def run_evaluator(self, state: InterviewState) -> Dict[str, Any]:
        history = state.get("interview_history", [])
        question = history[-2]["content"] if len(history) >= 2 else ""
        answer = history[-1]["content"] if len(history) >= 1 else ""
        
        evaluation = self.evaluator.evaluate_answer(question, answer, state["player_card"])
        scores = state.get("evaluation_scores", []) + [evaluation]
        
        return {"evaluation_scores": scores}

    def should_continue(self, state: InterviewState) -> str:
        if state.get("turn_count", 0) >= state.get("max_turns", 5):
            return "end"
        return "continue"
