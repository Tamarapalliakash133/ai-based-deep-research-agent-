from mcp.server.fastmcp import FastMCP
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_core.tools import create_retriever_tool

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    print("sorry for the interupt in the api key")

mc = FastMCP("akash-mcp",host="0.0.0.0", port=4000)

tavily = TavilySearchResults(max_results = 3)
@mc.tool()
def tool1():
    tool1 = create_retriever_tool(
        tavily,
        name = "tools",
        description = "Answer the questions from the internet data"
    )
    return tool1

if __name__ == "__main__":
    mc.run(transport = "sse")










