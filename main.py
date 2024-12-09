from swarm import Swarm
from swarm.controller import AgentController

def run_interactive_loop():
    """Run the interactive loop with the controller."""
    controller = AgentController()
    print("Starting Swarm Agent System 🐝")
    print("\nAvailable Capabilities:")
    print("- 🔍 Web Search")
    print("- 💻 Terminal Commands")
    print("- 🤖 macOS Automation")
    print("\nI'm here to help! What would you like to do?\n")
    
    while True:
        try:
            # Get user input
            user_input = input("\033[90mYou:\033[0m ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye! 👋")
                break
            
            # Start assistant response
            print("\033[94mAssistant:\033[0m ", end="", flush=True)
            
            # Stream the response
            for chunk in controller.handle_message_stream(user_input):
                print(chunk, end="", flush=True)
            print()  # New line after response
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\033[91mError:\033[0m {str(e)}")

if __name__ == "__main__":
    run_interactive_loop() 