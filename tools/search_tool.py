from tavily import TavilyClient
from langchain_core.tools import Tool
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=TAVILY_API_KEY)

def web_search(query: str) -> str:
    try:
        response = client.search(query, max_results=3)
        results = response.get("results", [])
        
        if not results:
            return "Koi result nahi mila."
        
        output = ""
        for i, r in enumerate(results, 1):
            output += f"{i}. {r['title']}\n{r['content']}\n\n"
        
        return output.strip()
    
    except Exception as e:
        return f"Search error: {str(e)}"

class SearchInput(BaseModel):
    query: str = Field(description="The search query to look up on the internet")

search_tool = Tool(
    name="web_search",
    func=web_search,
    description="Use this to search the internet for current information. Input should be a clear search query.",
    args_schema=SearchInput
)