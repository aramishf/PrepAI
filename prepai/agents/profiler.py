"""
Agent 1: The Profiler

Analyzes the user's resume and job description to create a structured "player card"
that guides the interview process. Runs once at the start of each session.
"""

import anthropic
import json
import sys
import os
from typing import List, Dict, Optional

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ANTHROPIC_API_KEY


def build_player_card(user_context: List[Dict], job_context: List[Dict]) -> Optional[Dict]:
    """
    Analyze user resume and job description to build a structured player card.

    This function runs once at the start of an interview session. It uses Claude
    to analyze the retrieved context chunks and extract key insights about the
    candidate's strengths, gaps, and recommended focus areas.

    Args:
        user_context: List of dictionaries from get_user_context() containing:
                     - text: chunk content
                     - source: "resume"
                     - chunk_index: position in document
        job_context: List of dictionaries from get_job_context() containing:
                    - text: chunk content
                    - source: "job_description"
                    - chunk_index: position in document

    Returns:
        Dictionary with structured player card data:
        {
            "user_strengths": ["strength1", "strength2", ...],  # 3-5 items
            "user_projects": ["project1", "project2", ...],
            "skill_gaps": ["gap1", "gap2", ...],
            "recommended_question_focus": ["area1", "area2", ...],
            "role_level": "junior" | "mid" | "senior",
            "company_culture_signals": ["signal1", "signal2", ...]
        }

        Returns None if API call fails or JSON parsing fails.

    Raises:
        ValueError: If user_context or job_context is empty
    """
    # Validate inputs
    if not user_context or not job_context:
        raise ValueError("Both user_context and job_context must be non-empty")

    # Format the user context (resume chunks) for the prompt
    # Concatenate all retrieved resume chunks into a single text block
    user_text = "\n\n".join([
        f"[Resume Chunk {chunk['chunk_index']}]\n{chunk['text']}"
        for chunk in user_context
    ])

    # Format the job context (job description chunks) for the prompt
    # Concatenate all retrieved job description chunks into a single text block
    job_text = "\n\n".join([
        f"[Job Description Chunk {chunk['chunk_index']}]\n{chunk['text']}"
        for chunk in job_context
    ])

    # Build the system prompt that enforces structured JSON output
    system_prompt = """You are an expert technical recruiter and interview preparation coach.

Your task is to analyze a candidate's resume and a job description, then create a structured "player card" that will guide an AI interview system.

You must analyze:
1. The candidate's top 3-5 technical or behavioral strengths
2. Standout projects that demonstrate their capabilities
3. Clear skill gaps between job requirements and candidate experience
4. Recommended focus areas for interview questions
5. The target role's seniority level (junior, mid, or senior)
6. Company culture signals and values from the job posting

Be specific, concise, and actionable. Focus on what will help tailor the interview.

You MUST respond with valid JSON only, using exactly this schema:
{
  "user_strengths": ["string", "string", ...],
  "user_projects": ["string", "string", ...],
  "skill_gaps": ["string", "string", ...],
  "recommended_question_focus": ["string", "string", ...],
  "role_level": "junior" OR "mid" OR "senior",
  "company_culture_signals": ["string", "string", ...]
}

Do not include any text before or after the JSON. Only return valid JSON."""

    # Build the user prompt with the actual resume and job description content
    user_prompt = f"""Analyze this candidate for this role and create a player card.

RESUME:
{user_text}

JOB DESCRIPTION:
{job_text}

Return your analysis as valid JSON following the exact schema specified in the system prompt."""

    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    try:
        # Call Claude API to analyze and generate the player card
        # Using Claude Sonnet 4.5 for good balance of quality and cost
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,  # Sufficient for structured analysis
            temperature=0.3,  # Low temperature for consistent, focused output
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        # Extract the text content from the response
        response_text = response.content[0].text

        # Strip markdown code fences if present
        # Claude sometimes wraps JSON in ```json ... ``` despite instructions
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]  # Remove ```json
        elif response_text.startswith("```"):
            response_text = response_text[3:]  # Remove ```
        if response_text.endswith("```"):
            response_text = response_text[:-3]  # Remove trailing ```
        response_text = response_text.strip()

        # Parse the JSON response
        player_card = json.loads(response_text)

        # Validate the response has all required fields
        required_fields = [
            "user_strengths",
            "user_projects",
            "skill_gaps",
            "recommended_question_focus",
            "role_level",
            "company_culture_signals"
        ]

        for field in required_fields:
            if field not in player_card:
                print(f"Warning: Missing required field '{field}' in player card")
                return None

        # Validate role_level is one of the expected values
        if player_card["role_level"] not in ["junior", "mid", "senior"]:
            print(f"Warning: Invalid role_level '{player_card['role_level']}'. Expected: junior, mid, or senior")
            return None

        return player_card

    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON from Claude response: {e}")
        print(f"Response was: {response_text[:200]}...")
        return None

    except Exception as e:
        print(f"Error: Failed to generate player card: {e}")
        return None


class ProjectProfiler:
    """
    Class-based wrapper for the Profiler agent.

    This class encapsulates the profiler functionality and can be instantiated
    with a ChromaDB client reference for future extensibility.
    """

    def __init__(self, chroma_client=None):
        """
        Initialize the ProjectProfiler.

        Args:
            chroma_client: Optional ChromaDB client (reserved for future use)
        """
        # Store the chroma_client for potential future use
        # Currently not used in build_player_card, but available for extensions
        self.chroma_client = chroma_client

    def build_player_card(self, user_context: List[Dict], job_context: List[Dict]) -> Optional[Dict]:
        """
        Analyze user resume and job description to build a structured player card.

        This is a wrapper method that delegates to the standalone build_player_card function.

        Args:
            user_context: List of dictionaries from get_user_context()
            job_context: List of dictionaries from get_job_context()

        Returns:
            Dictionary with structured player card data or None on error
        """
        # Delegate to the standalone function
        return build_player_card(user_context, job_context)
