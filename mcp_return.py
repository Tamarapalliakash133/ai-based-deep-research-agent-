import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from model import my_model


async def main():
    client = MultiServerMCPClient(
        {
            "akash-mcp": {
                "url" : "https://your-mcp-server.onrender.com/sse",
                "transport" : "sse",
            }
        }
    )
    tools = await client.get_tools()
    return tools

