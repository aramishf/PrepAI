import anthropic
import json
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ANTHROPIC_API_KEY


class EvaluatorAgent:
    """
    Agent 3: The Evaluator

    Scores each user answer across 6 specific dimensions.
    This agent runs silently in the background after every single answer 
    to collect telemetry for the final report.
    """
    
    def __init__(self):
        """Initialize the Anthropic client for the Evaluator Agent."""
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def evaluate_answer(self, question: str, user_answer: str, player_card: dict) -> dict:
        """
        Takes the question asked, the user's answer, and the player card.
        Calls Claude to score the answer across 6 dimensions (0-10).
        
        Args:
            question (str): The interview question asked.
            user_answer (str): The candidate's answer.
            player_card (dict): The generated player card containing candidate context.
            
        Returns:
            dict: The evaluation scores and feedback following the strict JSON schema.
        """
        system_prompt = """You are an expert technical interviewer and strict evaluator.
Your task is to evaluate a candidate's answer to an interview question across 6 dimensions.
You will be provided with the candidate's 'Player Card' (their background/experience), the specific question asked, and their answer.

You must score the candidate strictly from 0 to 10 on the following criteria:
1. RELEVANCE (0-10): Did they actually answer the specific question asked?
2. SPECIFICITY (0-10): Are there concrete details, tools, and technical constraints mentioned?
3. STAR_COMPLETENESS (0-10): Did they cover Situation, Task, Action, and crucially, RESULT?
4. CONFIDENCE (0-10): Is the language direct, or hedged with filler words (maybe, kinda, I think)?
5. ACCURACY (0-10): Does this align with the experience on their player_card?
6. IMPACT (0-10): Are there quantified metrics or clear business/technical outcomes?

You must also provide an 'overall_score' (0-10), a one-sentence 'strength', and a one-sentence 'weakness'.

You MUST respond with valid JSON only, using exactly this schema:
{
  "relevance": int,
  "specificity": int,
  "star_completeness": int,
  "confidence": int,
  "accuracy": int,
  "impact": int,
  "overall_score": int,
  "strength": "string (one short sentence)",
  "weakness": "string (one short sentence)"
}

Do not include any text before or after the JSON. Only return valid JSON."""

        user_prompt = f"""Evaluate this answer based on the criteria.

PLAYER CARD:
{json.dumps(player_card, indent=2)}

QUESTION ASKED:
{question}

CANDIDATE ANSWER:
{user_answer}

Provide your strict evaluation as valid JSON only."""

        try:
            # Call Claude API to evaluate the answer
            # Using Sonnet and temperature 0.1 for strict, analytical, and deterministic grading
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=1000,
                temperature=0.1,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            # Extract the text content from the response
            if not response.content:
                print(f"Warning: Model returned empty content. Stop reason: {response.stop_reason}")
                return {
                    "relevance": 0, "specificity": 0, "star_completeness": 0,
                    "confidence": 0, "accuracy": 0, "impact": 0, "overall_score": 0,
                    "strength": "Error evaluating answer.",
                    "weakness": f"API Refusal: The model refused to evaluate this response ({response.stop_reason})."
                }
            response_text = response.content[0].text

            # Robust JSON parser that cleans markdown fences
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            elif response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            evaluation = json.loads(response_text)
            
            # Validate required keys
            required_keys = [
                "relevance", "specificity", "star_completeness", 
                "confidence", "accuracy", "impact", "overall_score", 
                "strength", "weakness"
            ]
            
            for key in required_keys:
                if key not in evaluation:
                    print(f"Warning: Missing required key '{key}' in evaluator response.")
                    
            return evaluation

        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON from Evaluator response: {e}")
            print(f"Response was: {response_text}")
            # Return a fallback evaluation dictionary in case of parsing errors
            return {
                "relevance": 0, "specificity": 0, "star_completeness": 0,
                "confidence": 0, "accuracy": 0, "impact": 0, "overall_score": 0,
                "strength": "Error evaluating answer.",
                "weakness": "Failed to parse API response."
            }
        except Exception as e:
            print(f"Error: Evaluator API call failed: {e}")
            return {
                "relevance": 0, "specificity": 0, "star_completeness": 0,
                "confidence": 0, "accuracy": 0, "impact": 0, "overall_score": 0,
                "strength": "Error evaluating answer.",
                "weakness": f"API Exception: {str(e)}"
            }
