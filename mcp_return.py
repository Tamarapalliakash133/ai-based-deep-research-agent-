import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from model import my_model


async def main():
    client = MultiServerMCPClient(
        {
            "akash-mcp": {
                "url" : "http://127.0.0.1:4000/sse",
                "transport" : "sse",
            }
        }
    )
    tools = await client.get_tools()
    return tools

