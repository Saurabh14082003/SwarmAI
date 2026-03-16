from tools.mcp_client import call_mcp_tool, get_available_mcp_tools

# TOOLS mapping for prompt injection (matches server name to its capabilities)
TOOLS = {name: name for name in get_available_mcp_tools()}

# Map agent tool name to (server_name, mcp_tool_name)
SERVER_TOOL_MAP = {
    "search": ("search", "web_search"),
    "email": ("email", "send_email"),
    "calendar": ("calendar", "create_event")
}

def run_tool(tool_name, query=None, **kwargs):
    """
    Routes a tool call to the appropriate MCP server via the mcp_client.
    """
    if tool_name not in SERVER_TOOL_MAP:
        raise ValueError(f"Unknown tool: {tool_name}")

    server_name, actual_tool_name = SERVER_TOOL_MAP[tool_name]
    
    # If a single query string is provided (e.g. for search)
    if query is not None and not kwargs:
        if tool_name == "search":
            return call_mcp_tool(server_name, actual_tool_name, query=query)
        # Fallback for simple calls to other tools
        return call_mcp_tool(server_name, actual_tool_name, query=query)
    
    # Handle structured keyword arguments
    return call_mcp_tool(server_name, actual_tool_name, **kwargs)