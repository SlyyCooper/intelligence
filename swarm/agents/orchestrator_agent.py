import json
from typing import Optional
from ..swarm_types import Agent, Result
from .applescript_agent import applescript_agent
from .terminal_agent import terminal_agent
from .brave_search_agent import brave_search_agent

# Create our instructor agent
instructor_agent = Agent(
    name="Instructor",
    model="gpt-4o",
    instructions="""You are the main instructor agent, responsible for general conversations and technical guidance.
You excel at:
- Explaining technical concepts
- Providing coding assistance
- Project planning and architecture
- Best practices and patterns
- General problem-solving
- Interpreting results from specialized agents

When receiving search results:
- Help analyze and summarize the information
- Extract key points
- Provide additional context if needed
- Answer follow-up questions

You work alongside specialized agents and help interpret their results."""
)

def process_agent_return(context_variables: dict) -> Optional[Agent]:
    """Helper function to determine which agent should handle the next step."""
    if context_variables.get("return_to") == "orchestrator":
        task_type = context_variables.get("task_type", "")
        task_completed = context_variables.get("task_completed", False)
        
        if not task_completed:
            return instructor_agent
        
        if task_type == "web_search" and context_variables.get("result_count", 0) > 0:
            return instructor_agent
            
        return instructor_agent
    return None

def handle_task_completion(request: str, context_variables: dict = {}) -> Result:
    """
    Handles task completion from specialized agents and decides next steps.
    """
    next_agent = process_agent_return(context_variables)
    if next_agent:
        task_type = context_variables.get("task_type", "")
        task_completed = context_variables.get("task_completed", False)
        
        if not task_completed:
            return Result(
                value="I notice that task wasn't completed successfully. Let me have the instructor help clarify what you need.",
                agent=instructor_agent,
                context_variables={
                    "original_request": request,
                    "needs_clarification": True
                }
            )
        
        if task_type == "web_search" and context_variables.get("result_count", 0) > 0:
            return Result(
                value="I've got those search results. Let me have the instructor help interpret them and provide any additional context you might need.",
                agent=instructor_agent,
                context_variables={
                    "original_request": request,
                    "needs_interpretation": True,
                    "search_results": context_variables.get("raw_response", {})
                }
            )
        
        return Result(
            value="Task completed. Let's continue with the instructor for any follow-up questions.",
            agent=instructor_agent,
            context_variables={"original_request": request}
        )
    
    return continue_with_instructor(request, context_variables)

def delegate_to_applescript(request: str, context_variables: dict = {}) -> Result:
    """
    Delegates a task to the AppleScript agent when appropriate.
    """
    return Result(
        value="I'll have the AppleScript agent handle this automation task.",
        agent=applescript_agent,
        context_variables={"original_request": request}
    )

def delegate_to_terminal(request: str, context_variables: dict = {}) -> Result:
    """
    Delegates a task to the Terminal agent when appropriate.
    """
    return Result(
        value="I'll have the Terminal agent handle this command-line task.",
        agent=terminal_agent,
        context_variables={"original_request": request}
    )

def delegate_to_search(request: str, context_variables: dict = {}) -> Result:
    """
    Delegates a task to the Brave Search agent when appropriate.
    """
    return Result(
        value="I'll have the Brave Search agent look that up for you.",
        agent=brave_search_agent,
        context_variables={"original_request": request}
    )

def continue_with_instructor(request: str, context_variables: dict = {}) -> Result:
    """
    Continues the conversation with the main instructor agent.
    """
    return Result(
        value="This is a general question. I'll have the instructor help you with this.",
        agent=instructor_agent,
        context_variables={"original_request": request}
    )

# Create the Orchestrator Agent
orchestrator_agent = Agent(
    name="OrchestratorAgent",
    model="gpt-4o",
    instructions="""You are an orchestrator agent responsible for directing conversations and tasks to the appropriate specialized agents.

Your main responsibilities are to:
1. Analyze user requests and determine the best agent to handle them
2. Route tasks to the appropriate specialized agent
3. Handle returns from specialized agents
4. Decide next steps after task completion

Task Completion Handling:
1. Receive results from specialized agents
2. Check task completion status
3. Analyze if results need interpretation
4. Route to appropriate next agent

When handling returns:
- Failed tasks → Get clarification from instructor
- Search results → Send to instructor for interpretation
- Completed tasks → Return to instructor for next steps
- Always ensure smooth transitions between agents

When to delegate to Brave Search agent:
- Web search queries
- Information lookup
- Research requests
- Finding specific websites
- Current information needs

When to delegate to Terminal agent:
- Command line operations
- File system operations
- System commands
- Directory navigation
- Process management
- Package management (brew, pip, etc.)

When to delegate to AppleScript agent:
- GUI automation
- Application control
- System dialogs
- Menu bar operations
- Application-specific scripting

When to keep with the instructor:
- General conversations
- Code explanations
- Non-system tasks
- Project planning
- Technical discussions
- Result interpretation

Always explain your routing decisions briefly.""",
    functions=[
        handle_task_completion,
        delegate_to_applescript,
        delegate_to_terminal,
        delegate_to_search,
        continue_with_instructor
    ],
    parallel_tool_calls=False
) 