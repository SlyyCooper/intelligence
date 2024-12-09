from typing import Optional, Dict, Any, List, Generator
from dataclasses import dataclass, field
from datetime import datetime
from .core import Swarm
from .agents.orchestrator_agent import orchestrator_agent

@dataclass
class ConversationState:
    history: List[Dict[str, Any]] = field(default_factory=list)
    active_tasks: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    last_agent: Optional[str] = None
    last_update: datetime = field(default_factory=datetime.now)

    def update(self, response):
        # Update history with the new message
        if isinstance(response, dict):
            self.history.append(response)
        elif hasattr(response, 'messages'):
            self.history.extend(response.messages)
        
        self.last_update = datetime.now()
        
        # Update task status
        if isinstance(response, dict) and response.get("task_completed"):
            self.active_tasks.pop(response.get("task_id"), None)
        
        # Update last agent
        if isinstance(response, dict) and response.get("agent"):
            self.last_agent = response["agent"]

class AgentController:
    def __init__(self):
        self.state = ConversationState()
        self.current_context = {}
        self.swarm = Swarm()
    
    def format_chunk(self, chunk: Dict[str, Any]) -> Optional[str]:
        """Format a streaming chunk for display."""
        if "content" in chunk and chunk["content"]:
            return chunk["content"]
        if "value" in chunk and chunk["value"]:
            return chunk["value"]
        return None
    
    def format_response(self, response) -> str:
        """Format the response for the user, hiding internal details."""
        if hasattr(response, 'messages') and response.messages:
            last_message = response.messages[-1]
            if "content" in last_message:
                return last_message["content"]
            
        if isinstance(response, dict):
            if "error" in response:
                return f"I encountered an issue: {response['error']}"
            if "value" in response:
                return response["value"]
        
        return "I'm processing your request..."
    
    def handle_message_stream(self, message: str) -> Generator[str, None, None]:
        """
        Stream the response to the user.
        
        Args:
            message: The user's message
            
        Yields:
            Formatted response chunks
        """
        try:
            # Create message format
            user_message = {"role": "user", "content": message}
            
            # Get conversation history
            messages = self.state.history + [user_message]
            
            # Process through orchestrator using Swarm with streaming
            response_stream = self.swarm.run(
                agent=orchestrator_agent,
                messages=messages,
                context_variables=self.current_context,
                stream=True
            )
            
            last_response = None
            for chunk in response_stream:
                # Handle response object at the end of stream
                if "response" in chunk:
                    last_response = chunk["response"]
                    continue
                
                # Handle streaming chunks
                if formatted := self.format_chunk(chunk):
                    yield formatted
            
            # Update state with final response
            if last_response:
                self.state.update(last_response)
                
                # Update context for next interaction
                self.current_context.update({
                    "conversation_history": self.state.history,
                    "last_agent": self.state.last_agent,
                    "active_tasks": self.state.active_tasks
                })
            
        except Exception as e:
            import traceback
            print("Error details:", traceback.format_exc())
            yield f"I encountered an unexpected error: {str(e)}"
    
    def handle_message(self, message: str) -> str:
        """
        Non-streaming message handler (fallback).
        
        Args:
            message: The user's message
            
        Returns:
            Formatted response for the user
        """
        try:
            # Create message format
            user_message = {"role": "user", "content": message}
            
            # Get conversation history
            messages = self.state.history + [user_message]
            
            # Process through orchestrator using Swarm
            response = self.swarm.run(
                agent=orchestrator_agent,
                messages=messages,
                context_variables=self.current_context,
                stream=False
            )
            
            # Update state
            self.state.update(response)
            
            # Update context for next interaction
            self.current_context.update({
                "conversation_history": self.state.history,
                "last_agent": self.state.last_agent,
                "active_tasks": self.state.active_tasks
            })
            
            # Return formatted response
            return self.format_response(response)
            
        except Exception as e:
            import traceback
            print("Error details:", traceback.format_exc())
            return f"I encountered an unexpected error: {str(e)}"
    
    def get_state(self) -> Dict[str, Any]:
        """Get current conversation state."""
        return {
            "history_length": len(self.state.history),
            "active_tasks": len(self.state.active_tasks),
            "last_update": self.state.last_update.isoformat(),
            "last_agent": self.state.last_agent
        } 