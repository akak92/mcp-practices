from mcp.server.fastmcp import FastMCP
from utils.tools import add

# Create an MCP server
mcp = FastMCP("MCP LLM Connection Server", "An MCP server with LLM connection example.")


# Register tools from utils.tools
@mcp.tool()
def add_tool(a: int, b: int) -> int:
    """Add two numbers"""
    return add(a, b)


# Main execution block - this is required to run the server
if __name__ == "__main__":
    mcp.run()