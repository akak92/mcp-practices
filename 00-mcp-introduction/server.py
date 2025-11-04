# server.py
from mcp.server.fastmcp import FastMCP
from utils.tools import add, subtract
from utils.resources import get_greeting, get_farewell

# Create an MCP server
mcp : FastMCP = FastMCP("First MCP Server", "A simple MCP server example.")

# Register tools from utils.tools
@mcp.tool()
def add_tool(a: int, b: int) -> int:
    """Add two numbers"""
    return add(a, b)

@mcp.tool()
def subtract_tool(a: int, b: int) -> int:
    """Subtract two numbers"""
    return subtract(a, b)

# Register resources from utils.resources
@mcp.resource("greeting://{name}")
def greeting_resource(name: str) -> str:
    """Get a personalized greeting"""
    return get_greeting(name)

@mcp.resource("farewell://{name}")
def farewell_resource(name: str) -> str:
    """Get a personalized farewell"""
    return get_farewell(name)


# Main execution block - this is required to run the server
if __name__ == "__main__":
    mcp.run()