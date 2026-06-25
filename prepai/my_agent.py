import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    # 1. Verify file existence first
    path = "prepai/data/resume.txt"
    if not os.path.exists(path):
        print(f"DEBUG: Critical Error! {path} not found in {os.getcwd()}")
        return

    print(f"DEBUG: Found {path}, starting agent...")
    
    options = ClaudeAgentOptions(tools=["Read"])
    
    # FINAL FIX: Force the prompt to explicitly pass the exact path to the tool
    prompt = """
    Please use the Read tool to read the file located at 'prepai/data/resume.txt'. 
    Tell me what you see in the first 5 lines to confirm you've opened it. 
    Then, analyze my experience to find the most complex technical project I listed, 
    and ask me one highly specific, difficult interview question about the trade-offs I made.
    """
    
    # 2. Capture every message
    async for message in query(prompt=prompt, options=options):
        print(f"AGENT MESSAGE: {message}")

if __name__ == "__main__":
    asyncio.run(main())