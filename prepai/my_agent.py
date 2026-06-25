import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    # Step 1: We fulfill the stretch goal by giving it the Read tool
    options = ClaudeAgentOptions(tools=["Read"]) 
    
    # Step 2: The Agentic Prompt
    # We tell it what to read, and what to do with that information
    prompt = """
    Please use the Read tool to read the file 'resume.txt' in this directory. 
    Analyze my experience, find the most complex technical project I listed, 
    and ask me one highly specific, difficult interview question about 
    the trade-offs I made in that project.
    """
    
    print("Agent is reading your resume and thinking...\n")
    print("-" * 50)
    
    # Step 3: The Execution Loop
    async for message in query(prompt=prompt, options=options):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())