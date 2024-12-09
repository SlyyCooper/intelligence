import subprocess
from typing import Optional
from ..swarm_types import Agent, Result

def run_applescript(script: str, context_variables: dict = {}) -> Result:
    """
    Executes an AppleScript and returns the result.
    
    Args:
        script: The AppleScript code to execute
        context_variables: Context variables passed from the agent system
    
    Returns:
        Result object containing the script output or error message
    """
    try:
        # Execute the AppleScript using osascript
        process = subprocess.Popen(
            ['osascript', '-e', script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        output, error = process.communicate()
        
        if process.returncode != 0:
            return Result(
                value=f"AppleScript Error: {error}",
                context_variables={"last_error": error}
            )
        
        return Result(
            value=output.strip(),
            context_variables={"last_output": output.strip()}
        )
    except Exception as e:
        return Result(
            value=f"Error executing AppleScript: {str(e)}",
            context_variables={"last_error": str(e)}
        )

# Create the AppleScript Agent
applescript_agent = Agent(
    name="AppleScriptAgent",
    model="gpt-4o",
    instructions="""You are a specialized agent for executing AppleScript commands on macOS.
Your primary function is to:
1. Generate appropriate AppleScript code based on requests
2. Execute the scripts safely
3. Handle and report any errors that occur
4. Only execute safe and reasonable commands

Never execute scripts that could:
- Delete important system files
- Access sensitive information
- Cause system instability
- Perform malicious actions

Always validate and explain the scripts you're about to run.""",
    functions=[run_applescript],
    parallel_tool_calls=False  # For safety, execute one script at a time
) 