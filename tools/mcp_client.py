import asyncio
import os
import sys
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
    
    # Get absolute path relative to this file's directory
    # tools/mcp_client.py -> base_dir is project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_script = os.path.join(base_dir, SERVERS[server_name])
    
    # Prepare environment with inherited variables and PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = base_dir + os.pathsep + env.get("PYTHONPATH", "")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
        env=env
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text if result.content else ""
    except Exception as e:
        print(f"ERROR calling MCP tool {tool_name} on server {server_name}: {e}")
        # Log more detail if it's an exception group
        if hasattr(e, "exceptions"):
            for sub_e in e.exceptions:
                print(f"  Sub-exception: {sub_e}")
        return f"Error: {str(e)}"

def call_mcp_tool(server_name, tool_name, **kwargs):
    """Sync wrapper to call an MCP tool."""
    try:
        return asyncio.run(_call_mcp_tool_async(server_name, tool_name, kwargs))
    except Exception as e:
        print(f"CRITICAL ERROR in call_mcp_tool: {e}")
        return f"Critical error executing tool: {e}"

def get_available_mcp_tools():
    """Returns a list of available tool names across all servers."""
    return list(SERVERS.keys())