import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from model import my_model


async def main():
    client = MultiServerMCPClient(
        {
            "akash-mcp": {
                "url" : os.getenv(MCP_URL),
                "transport" : "sse",
            }
        }
    )
    tools = await client.get_tools()
    return tools

