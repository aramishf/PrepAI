import asyncio
import os
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    path = "prepai/data/resume.txt"
    if not os.path.exists(path):
        print(f"❌ Error: {path} not found.")
        return

    print(f"✅ Found resume data. Initializing Agent...\n")
    print("⏳ Agent is booting up and reading the prompt...\n")
    
    options = ClaudeAgentOptions(tools=["Read"])
    
    prompt = """
    Please use the Read tool to read the file located at 'prepai/data/resume.txt'. 
    Tell me what you see in the first 5 lines to confirm you've opened it. 
    Then, analyze my experience to find the most complex technical project I listed, 
    and ask me one highly specific, difficult interview question about the trade-offs I made.
    """
    
    # Capture and filter the message stream
    async for message in query(prompt=prompt, options=options):
        msg_type = type(message).__name__
        
        # 1. Look for Tool Actions to show off the autonomous behavior
        if msg_type == "AssistantMessage":
            for block in message.content:
                if type(block).__name__ == "ToolUseBlock":
                    print(f"🛠️  [AGENT ACTION] Autonomously executing '{block.name}' tool...")
                    print(f"📂 [AGENT ACTION] Ingesting file: {block.input.get('file_path')}")
                    print(f"🧠 [AGENT ACTION] Analyzing architectural complexity...\n")
        
        # 2. Capture the final, clean text output
        elif msg_type == "ResultMessage":
            print("=" * 70)
            print("🎯 FINAL INTERVIEW ASSESSMENT")
            print("=" * 70 + "\n")
            print(message.result)  # This contains just the clean markdown text!
            print("\n" + "=" * 70)

if __name__ == "__main__":
    asyncio.run(main())