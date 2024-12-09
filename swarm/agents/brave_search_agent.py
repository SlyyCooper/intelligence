import requests
import json
from typing import Optional, Dict
from ..swarm_types import Agent, Result

API_KEY = "BSAB4YwWaXxHmxvN7tCcJ4pH1jEIuIn"
BASE_URL = "https://api.search.brave.com/res/v1/web/search"

def perform_web_search(
    query: str,
    count: int = 10,
    country: str = "US",
    search_lang: str = "en",
    safesearch: str = "moderate",
    context_variables: dict = {}
) -> Result:
    """
    Performs a web search using Brave Search API.
    
    Args:
        query: Search query
        count: Number of results (max 20)
        country: Country code
        search_lang: Search language
        safesearch: Safety level (off/moderate/strict)
        context_variables: Context variables passed from the agent system
    
    Returns:
        Result object containing search results or error message
    """
    try:
        # Prepare headers
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": API_KEY
        }

        # Prepare parameters
        params = {
            "q": query,
            "count": min(count, 20),  # Ensure we don't exceed max
            "country": country,
            "search_lang": search_lang,
            "safesearch": safesearch,
            "text_decorations": 1,
            "spellcheck": 1
        }

        # Make the request
        response = requests.get(
            BASE_URL,
            headers=headers,
            params=params
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        
        # Format results nicely
        if "web" in data and "results" in data["web"]:
            results = data["web"]["results"]
            formatted_results = "\n\n".join([
                f"🔍 {result['title']}\n"
                f"🌐 {result['url']}\n"
                f"📝 {result['description']}"
                for result in results
            ])
            
            # Return results and signal completion
            return Result(
                value=formatted_results + "\n\nSearch completed. Returning to orchestrator for next steps.",
                context_variables={
                    "last_query": query,
                    "result_count": len(results),
                    "raw_response": data,
                    "task_completed": True,
                    "task_type": "web_search",
                    "return_to": "orchestrator"
                }
            )
        else:
            # Return no results and signal completion
            return Result(
                value="No results found. Returning to orchestrator for next steps.",
                context_variables={
                    "last_query": query,
                    "result_count": 0,
                    "raw_response": data,
                    "task_completed": True,
                    "task_type": "web_search",
                    "return_to": "orchestrator"
                }
            )

    except requests.exceptions.RequestException as e:
        # Return error and signal completion
        return Result(
            value=f"Search Error: {str(e)}\nReturning to orchestrator for next steps.",
            context_variables={
                "last_error": str(e),
                "task_completed": False,
                "task_type": "web_search",
                "return_to": "orchestrator"
            }
        )

# Create the Brave Search Agent
brave_search_agent = Agent(
    name="BraveSearchAgent",
    model="gpt-4o",
    instructions="""You are a specialized agent for performing web searches using the Brave Search API.
Your primary function is to:
1. Process search queries effectively
2. Format and present search results clearly
3. Handle search parameters appropriately
4. Manage errors gracefully
5. Signal task completion for orchestrator

Search Capabilities:
- Web search with up to 20 results
- Multiple language support
- Safe search filtering
- Spell checking
- Country-specific results

Result Format:
🔍 Title of the result
🌐 URL of the page
📝 Description/snippet

Parameters You Can Adjust:
- Number of results (1-20)
- Country code
- Search language
- Safe search level (off/moderate/strict)

Task Completion:
1. Execute the search
2. Format results clearly
3. Signal completion to orchestrator
4. Include task status in context

Always provide clear and formatted results with:
- Relevant titles
- Clean URLs
- Helpful descriptions""",
    functions=[perform_web_search],
    parallel_tool_calls=False
) 