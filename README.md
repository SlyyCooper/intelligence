# Intelligence

A modern agent-based system that combines multiple specialized agents for different tasks:

## Features

- 🎭 **Orchestration**: Smart routing between specialized agents
- 🔍 **Web Search**: Integrated Brave Search capabilities
- 💻 **Terminal**: Safe command execution with confirmation
- 🤖 **macOS Automation**: AppleScript integration
- 📊 **State Management**: Robust conversation and task state tracking
- 🔄 **Real-time Streaming**: Modern streaming responses

## Architecture

- **Controller**: Single point of contact for all interactions
- **Orchestrator**: Smart task routing and agent management
- **Specialized Agents**: Task-specific implementations
- **State Management**: Robust conversation tracking

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/intelligence.git
cd intelligence
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the system:
```bash
python main.py
```

## Usage

The system provides an interactive CLI where you can:
- Perform web searches
- Execute terminal commands
- Automate macOS tasks
- Get help and explanations

Example:
```bash
You: Search the weather in Tampa
Assistant: Let me look that up for you...
[Search results stream in real-time]
```

## Requirements

- Python 3.11+
- Brave Search API key (for web search capabilities)
- macOS (for AppleScript functionality)

## License

MIT License - see LICENSE file for details
