from mcp.server.fastmcp import FastMCP
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import create_retriever_tool
import os

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set")


mc = FastMCP("akash-mcp", host="0.0.0.0", port=4000)

tavily = TavilySearchResults(
    max_results=3,
    tavily_api_key=TAVILY_API_KEY
)

retriever_tool = create_retriever_tool(
    tavily,
    name="tools",
    description="Answer questions using internet data"
)


@mc.tool()
def tool1(query: str):
    result = retriever_tool.invoke(query)
    return str(result)


if __name__ == "__main__":
    mc.run(transport="sse")
