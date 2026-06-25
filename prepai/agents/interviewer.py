"""
Agent 2: The Interviewer (Part A - Basic Loop)

Generates targeted, context-aware interview questions based on the player card.
Questions explicitly reference the candidate's actual projects and experience.
"""

import anthropic
import json
import sys
import os
from typing import Optional, List, Dict

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ANTHROPIC_API_KEY


class InterviewerAgent:
    """
    Interview question generator that creates targeted questions based on player card analysis.

    Questions are tailored to:
    - The candidate's actual projects and experience
    - Identified skill gaps
    - Detected role level (junior/mid/senior)
    - Current position in interview sequence (1-6)
    """

    def __init__(self):
        """
        Initialize the InterviewerAgent with Anthropic Claude API client.
        """
        # Initialize the Anthropic client using API key from config
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    def generate_question(
        self,
        player_card: dict,
        question_number: int,
        previous_answers: List[str] = None
    ) -> str:
        """
        Generate a single targeted interview question based on player card and sequence.

        Args:
            player_card: Dictionary containing:
                - user_strengths: List of candidate strengths
                - user_projects: List of standout projects
                - skill_gaps: List of identified gaps
                - recommended_question_focus: List of focus areas
                - role_level: "junior" | "mid" | "senior"
                - company_culture_signals: List of culture indicators
            question_number: Integer 1-6 indicating position in interview sequence
            previous_answers: Optional list of previous Q&A pairs (reserved for Part B)

        Returns:
            String containing only the interview question text

        Question Strategy by Number:
            1: Opening question about fit and background
            2-4: Deep dive into specific projects with technical challenges
            5-6: Probe skill gaps and architectural thinking
        """
        # Validate inputs
        if not player_card:
            raise ValueError("player_card cannot be empty")
        if question_number < 1 or question_number > 6:
            raise ValueError("question_number must be between 1 and 6")

        # Extract key information from player card
        role_level = player_card.get("role_level", "mid")
        user_projects = player_card.get("user_projects", [])
        skill_gaps = player_card.get("skill_gaps", [])
        user_strengths = player_card.get("user_strengths", [])
        recommended_focus = player_card.get("recommended_question_focus", [])

        # Build the system prompt that enforces question generation rules
        system_prompt = f"""You are an expert technical interviewer conducting a {role_level}-level interview.

Your task is to generate ONE highly specific interview question based on the candidate's profile.

CRITICAL RULES:
1. Return ONLY the question text itself - no preamble, no "Here's a question:", no markdown
2. Make questions specific by referencing actual projects, technologies, or experiences from the candidate's background
3. Questions should be challenging but fair for a {role_level}-level candidate
4. Use a conversational but professional tone
5. Questions should require detailed technical explanations, not yes/no answers

DO NOT include:
- Introductory phrases like "Sure, here is your question:" or "Here's what I'd ask:"
- Markdown formatting like ``` or **bold**
- Explanations of why you're asking the question
- Multiple questions or follow-ups

Just return the raw question text."""

        # Build context-specific user prompt based on question number
        if question_number == 1:
            # Opening question: Tell me about yourself
            user_prompt = f"""Generate an opening interview question for question #{question_number}.

CANDIDATE PROFILE:
Role Level: {role_level}
Key Strengths: {', '.join(user_strengths[:3])}
Notable Projects: {', '.join(user_projects[:2])}

Generate an opening question that:
- Asks the candidate to introduce themselves
- Specifically mentions the role they're interviewing for
- Encourages them to highlight relevant experience and fit
- Is warm but professional

Return ONLY the question text."""

        elif 2 <= question_number <= 4:
            # Technical deep dive on specific projects
            # Pick a project based on question number to vary focus
            project_index = (question_number - 2) % len(user_projects) if user_projects else 0
            selected_project = user_projects[project_index] if user_projects else "your previous work"

            user_prompt = f"""Generate a technical interview question for question #{question_number}.

CANDIDATE PROFILE:
Role Level: {role_level}
Selected Project: {selected_project}
Key Strengths: {', '.join(user_strengths)}
Recommended Focus Areas: {', '.join(recommended_focus[:2])}

Generate a question that:
- Explicitly references the selected project: "{selected_project}"
- Challenges a specific technical decision or architecture choice in that project
- Requires the candidate to explain trade-offs, alternatives, or problem-solving approach
- Tests depth of understanding for a {role_level}-level engineer

Return ONLY the question text."""

        else:  # question_number 5 or 6
            # Focus on skill gaps and architectural thinking
            gap_index = (question_number - 5) % len(skill_gaps) if skill_gaps else 0
            selected_gap = skill_gaps[gap_index] if skill_gaps else "a relevant technology"

            user_prompt = f"""Generate a challenging technical question for question #{question_number}.

CANDIDATE PROFILE:
Role Level: {role_level}
Identified Skill Gap: {selected_gap}
Other Gaps: {', '.join(skill_gaps[:3])}
Recommended Focus Areas: {', '.join(recommended_focus)}

Generate a question that:
- Addresses the skill gap: "{selected_gap}"
- Tests architectural thinking and adaptability
- Asks how they would approach learning or solving a problem in this area
- Evaluates system design thinking appropriate for {role_level} level
- Can reveal depth despite lack of direct experience

Return ONLY the question text."""

        try:
            # Call Claude API to generate the interview question
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,  # Questions should be concise
                temperature=0.5,  # Balanced creativity for varied questions
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            # Extract the question text from response
            question_text = response.content[0].text.strip()

            # Additional cleanup: remove any markdown or wrapper text
            # Remove quotes if the model wrapped the question in quotes
            if question_text.startswith('"') and question_text.endswith('"'):
                question_text = question_text[1:-1]
            if question_text.startswith("'") and question_text.endswith("'"):
                question_text = question_text[1:-1]

            # Remove markdown code fences if present
            if question_text.startswith("```"):
                lines = question_text.split('\n')
                question_text = '\n'.join(lines[1:-1]) if len(lines) > 2 else question_text

            return question_text.strip()

        except Exception as e:
            print(f"Error generating question: {e}")
            # Return a fallback question if API fails
            return f"Can you tell me about your experience with the technologies required for this {role_level}-level role?"

    def evaluate_and_followup(
        self,
        original_question: str,
        user_answer: str,
        player_card: Dict
    ) -> Dict:
        """
        Evaluate a candidate's answer and generate a follow-up question if weak.

        This method analyzes the candidate's response for:
        - Vagueness or lack of specificity
        - Missing STAR format components (especially Result)
        - Insufficient technical depth
        - Incomplete answers

        Args:
            original_question: The interview question that was asked
            user_answer: The candidate's response to evaluate
            player_card: The player card context for tailored follow-ups

        Returns:
            Dictionary with evaluation results:
            {
                "evaluation": "WEAK" | "STRONG",
                "reason": "Brief explanation of the evaluation",
                "followup_question": "Follow-up question text" | null
            }

        Raises:
            ValueError: If original_question or user_answer is empty
        """
        # Validate inputs
        if not original_question or not original_question.strip():
            raise ValueError("original_question cannot be empty")
        if not user_answer or not user_answer.strip():
            raise ValueError("user_answer cannot be empty")

        # Extract role level for context
        role_level = player_card.get("role_level", "mid")

        # Build the system prompt for answer evaluation
        system_prompt = f"""You are an expert technical interviewer evaluating candidate responses.

Your task is to analyze a candidate's answer to an interview question and determine if it needs a follow-up probe.

EVALUATION CRITERIA:
1. STAR Format Completeness:
   - Situation: Does the answer establish context?
   - Task: Is the objective or challenge clear?
   - Action: Are specific actions and decisions explained?
   - Result: Are measurable outcomes or learnings provided? (CRITICAL - most important)

2. Technical Depth:
   - Are technical decisions explained with reasoning?
   - Are trade-offs and alternatives discussed?
   - Is the answer specific with concrete examples?

3. Vagueness Check:
   - Does the answer avoid generic statements?
   - Are there specific numbers, technologies, or outcomes?
   - Is there actual substance vs. hand-waving?

Mark as WEAK if:
- Missing Result section entirely (no outcomes/learnings mentioned)
- Too vague or generic without specifics
- Avoids the technical core of the question
- Lacks depth for a {role_level}-level candidate

Mark as STRONG if:
- Includes clear Result with measurable outcomes
- Demonstrates technical depth with specific examples
- Addresses the question directly with substance

You MUST respond with valid JSON only, using exactly this schema:
{{
  "evaluation": "WEAK" OR "STRONG",
  "reason": "Brief technical explanation (1-2 sentences)",
  "followup_question": "The specific follow-up question text (if WEAK) or null (if STRONG)"
}}

If evaluation is WEAK, generate a targeted follow-up that:
- Directly addresses what was missing (usually the Result)
- References specific technologies or context from their vague answer
- Pushes for concrete details, metrics, or outcomes
- Returns ONLY the follow-up question text in the followup_question field

Do not include any text before or after the JSON. Only return valid JSON."""

        # Build the user prompt with the Q&A to evaluate
        user_prompt = f"""Evaluate this candidate's answer and determine if a follow-up is needed.

ORIGINAL QUESTION:
{original_question}

CANDIDATE'S ANSWER:
{user_answer}

CANDIDATE LEVEL: {role_level}

Analyze the answer using the criteria in the system prompt and return your evaluation as JSON."""

        try:
            # Call Claude API to evaluate the answer
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=800,  # Need space for evaluation + potential follow-up
                temperature=0.3,  # Low temperature for consistent evaluation
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ]
            )

            # Extract the response text
            response_text = response.content[0].text.strip()

            # Strip markdown code fences if present
            # Claude sometimes wraps JSON in ```json ... ``` despite instructions
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # Remove ```json
            elif response_text.startswith("```"):
                response_text = response_text[3:]  # Remove ```
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # Remove trailing ```
            response_text = response_text.strip()

            # Parse the JSON response
            evaluation_result = json.loads(response_text)

            # Validate the response schema
            required_fields = ["evaluation", "reason", "followup_question"]
            for field in required_fields:
                if field not in evaluation_result:
                    print(f"Warning: Missing required field '{field}' in evaluation")
                    return self._fallback_evaluation()

            # Validate evaluation value
            if evaluation_result["evaluation"] not in ["WEAK", "STRONG"]:
                print(f"Warning: Invalid evaluation value '{evaluation_result['evaluation']}'")
                return self._fallback_evaluation()

            # Ensure followup_question is null for STRONG evaluations
            if evaluation_result["evaluation"] == "STRONG" and evaluation_result["followup_question"]:
                evaluation_result["followup_question"] = None

            return evaluation_result

        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON from evaluation response: {e}")
            print(f"Response was: {response_text[:200]}...")
            return self._fallback_evaluation()

        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return self._fallback_evaluation()

    def _fallback_evaluation(self) -> Dict:
        """
        Return a safe fallback evaluation if API call fails.

        Returns:
            Dictionary marking answer as STRONG to allow interview to continue
        """
        return {
            "evaluation": "STRONG",
            "reason": "Unable to evaluate answer due to technical error. Allowing interview to continue.",
            "followup_question": None
        }
