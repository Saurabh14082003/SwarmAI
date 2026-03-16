import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Define tool server locations
SERVERS = {
    "search": "mcp_servers/search_server.py",
    "email": "mcp_servers/gmail_server.py",
    "calendar": "mcp_servers/calendar_server.py"
}

async def _call_mcp_tool_async(server_name, tool_name, arguments):
    if server_name not in SERVERS:
        raise ValueError(f"Unknown server: {server_name}")
    
    server_script = os.path.join(os.getcwd(), SERVERS[server_name])
    
    server_params = StdioServerParameters(
        command="python",
        args=[server_script],
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content[0].text if result.content else ""

def call_mcp_tool(server_name, tool_name, **kwargs):
    """Sync wrapper to call an MCP tool."""
    return asyncio.run(_call_mcp_tool_async(server_name, tool_name, kwargs))

def get_available_mcp_tools():
    """Returns a list of available tool names across all servers."""
    # For now, we return the keys of SERVERS since each server hosts tools of that name
    # In a full discovery mode, we would async-list tools from each server
    return list(SERVERS.keys())