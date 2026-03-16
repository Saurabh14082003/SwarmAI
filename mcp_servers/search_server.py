from tavily import TavilyClient
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("Search")

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for the given query."""
    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    results = []

    for r in response["results"]:
        results.append(
            f"{r['title']} - {r['url']}\n{r['content']}"
        )

    return "\n\n".join(results)

if __name__ == "__main__":
    mcp.run()