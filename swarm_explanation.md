# Swarm Framework Visualization

```ascii
                                    SWARM SYSTEM
+-------------------------------------------------------------------------+
|                                                                         |
|  +----------------+     +-----------------+     +------------------+     |
|  |   Main Agent   |     |  Expert Agent   |     |   Other Agents  |     |
|  |  "Generalist" --|---->  "Specialist"   |---->|   (Extensible)  |     |
|  +----------------+     +-----------------+     +------------------+     |
|          |                      |                       |               |
|          v                      v                       v               |
|  +-------------------------------------------------------------------------+
|  |                         Function Toolkit                                 |
|  |  +---------------+  +---------------+  +----------------+  +---------+   |
|  |  | Agent Handoff |  | Tool Calling  |  | Context Update |  | Custom  |   |
|  |  +---------------+  +---------------+  +----------------+  +---------+   |
|  +-------------------------------------------------------------------------+
|                                    |                                        |
|                                    v                                        |
|  +-------------------------------------------------------------------------+
|  |                         Core Functionality                               |
|  |  • Conversation Management                                              |
|  |  • Agent Orchestration                                                  |
|  |  • Stream Processing                                                    |
|  |  • Error Handling                                                       |
|  +-------------------------------------------------------------------------+
|                                                                         |
+-------------------------------------------------------------------------+
```

## Key Components:

1. **Agents**
   - Main Agent: General purpose responder
   - Expert Agent: Technical specialist
   - Can create more specialized agents

2. **Core Features**
   - Agent-to-agent handoffs
   - Function calling
   - Context management
   - Streaming responses
   - Interactive demo loop

## Current Implementation:

```ascii
User Query
    │
    v
[Main Agent]────────┐
    │               │
    │               v
    │         [Expert Agent]
    │               │
    v               v
[Response/Function Calls]
```

## Example Flow:

1. User asks: "How are you?"
   - Main Agent handles it
   - Returns simple response

2. User asks: "Explain neural networks"
   - Main Agent recognizes technical query
   - Transfers to Expert Agent
   - Expert Agent provides detailed response

## Key Functions:

```ascii
+------------------------+
|     Agent Methods      |
+------------------------+
| • transfer_to_expert() |
| • run_demo_loop()      |
| • handle_tool_calls()  |
| • get_chat_completion()|
+------------------------+
```

## Usage Example:

```python
# Basic interaction
response = client.run(
    agent=main_agent,
    messages=[{"role": "user", "content": "Hello!"}]
)

# With context variables
response = client.run(
    agent=main_agent,
    messages=[...],
    context_variables={"user_name": "John"}
)

# With streaming
for chunk in client.run(agent=main_agent, messages=[...], stream=True):
    print(chunk)
```

## Core Capabilities:

1. **Agent Management**
   - Create multiple agents
   - Define specialized behaviors
   - Handle agent transitions

2. **Context Handling**
   - Maintain conversation state
   - Pass variables between agents
   - Update context dynamically

3. **Function Integration**
   - Call Python functions
   - Handle tool responses
   - Process results

4. **Stream Processing**
   - Real-time responses
   - Chunk management
   - Delta updates

## File Structure:

```ascii
swarm/
├── main.py      (Example implementation)
├── core.py      (Core functionality)
├── types.py     (Data structures)
└── util.py      (Helper functions)
``` 