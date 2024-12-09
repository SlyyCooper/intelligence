import subprocess
import os
import json
from typing import Optional, Dict, List
from ..swarm_types import Agent, Result

# Set the initial working directory
os.chdir('/Users/tan')

# Common command alternatives/suggestions
COMMAND_SUGGESTIONS = {
    'ls': ['ls -la', 'ls -lh', 'tree'],
    'rm': ['rm -i', 'trash', 'mv to_delete'],
    'cp': ['cp -r', 'rsync -av'],
    'find': ['fd', 'locate', 'mdfind'],
    'grep': ['rg', 'ag', 'ack'],
    'cat': ['bat', 'less', 'head -n 20'],
    'top': ['htop', 'glances', 'activity monitor'],
    'df': ['df -h', 'du -sh *', 'ncdu'],
    'ps': ['ps aux', 'pgrep', 'procs'],
    'cd': ['pushd', 'z', 'autojump']
}

def get_command_suggestions(command: str) -> List[str]:
    """Get alternative suggestions for a command."""
    base_cmd = command.split()[0]
    return COMMAND_SUGGESTIONS.get(base_cmd, [])

def return_to_instructor(context_variables: dict = {}) -> Result:
    """Returns control to the instructor agent."""
    return Result(
        value=json.dumps({"assistant": "Instructor"}),
        context_variables=context_variables
    )

def run_terminal_command(command: str, confirmation: str = "", context_variables: dict = {}) -> Result:
    """
    Executes a terminal command and returns the result.
    
    Args:
        command: The terminal command to execute
        confirmation: User's confirmation response (Y/N)
        context_variables: Context variables passed from the agent system
    
    Returns:
        Result object containing the command output or error message
    """
    # If no confirmation provided, ask for it
    if not confirmation:
        return Result(
            value=f"Command: {command}\n[Y/N]:",
            context_variables={
                "pending_command": command,
                "needs_confirmation": True
            }
        )
    
    # Handle rejection with suggestions
    if confirmation.upper() != 'Y':
        suggestions = get_command_suggestions(command)
        if suggestions:
            suggestion_text = "\nAlternative suggestions:\n" + "\n".join(f"- {s}" for s in suggestions)
            return Result(
                value=f"Command cancelled.{suggestion_text}\n\nPlease let me know which alternative you prefer, or tell me what you'd like to do instead.",
                context_variables={
                    "command_cancelled": True,
                    "had_suggestions": True,
                    "suggestions": suggestions
                }
            )
        else:
            return Result(
                value="Command cancelled. Please let me know what you'd like to do instead.",
                context_variables={"command_cancelled": True}
            )
    
    try:
        # Execute the command
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd='/Users/tan'  # Set working directory
        )
        output, error = process.communicate()
        
        if process.returncode != 0:
            # Return to instructor with error info
            return return_to_instructor({
                "last_error": error,
                "exit_code": process.returncode,
                "command_failed": True,
                "command": command
            })
        
        # Return to instructor with success info
        return return_to_instructor({
            "last_output": output.strip(),
            "exit_code": process.returncode,
            "cwd": os.getcwd(),
            "command_succeeded": True,
            "command": command
        })

    except Exception as e:
        # Return to instructor with exception info
        return return_to_instructor({
            "last_error": str(e),
            "command_failed": True,
            "command": command
        })

# Create the Terminal Agent
terminal_agent = Agent(
    name="TerminalAgent",
    model="gpt-4o",
    instructions="""You are a specialized agent for executing terminal commands on macOS.
Your primary function is to:
1. Execute terminal commands safely and efficiently
2. Handle command output and errors appropriately
3. Maintain working directory state
4. Ensure safe command execution
5. Return to instructor after task completion

Command Execution Process:
1. Show command to be executed
2. Wait for Y/N response
3. If Y: Execute command and return to instructor
4. If N: Show alternatives and ask for preference

Command Rejection Handling:
- When user says N, provide relevant alternatives
- Let user choose from suggestions or specify their own command
- Be flexible with user's new request
- Adapt to user's preferences

Safety Guidelines:
- Never execute potentially harmful commands (rm -rf, etc.)
- Always wait for Y confirmation
- Handle sensitive operations with care
- Avoid commands that could expose sensitive information

Working Directory:
- Starting directory: /Users/tan
- Track current directory changes
- Use absolute paths when necessary
- Handle directory navigation safely

Task Flow:
1. Receive command request
2. Get user confirmation
3. Execute or suggest alternatives
4. Show results/output
5. Automatically return to instructor

Response Format:
- Show command
- Ask [Y/N]
- If N: Show alternatives
- If Y: Execute and return to instructor""",
    functions=[run_terminal_command],
    parallel_tool_calls=False  # For safety, execute one command at a time
) 