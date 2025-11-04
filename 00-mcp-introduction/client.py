# client.py
"""
MCP Client to test our server.py
This client connects to our MCP server and tests its tools and resources.
"""

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Python executable
    args=["server.py"],  # Our server script
    env=None,  # Optional environment variables
)

async def run():
    logger.info("🚀 Starting MCP Client...")
    logger.info("=" * 50)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                logger.info("✅ Connected to MCP server")
                
                # Initialize the connection
                await session.initialize()
                logger.info("✅ Session initialized")

                # List available resources
                logger.info("📁 LISTING RESOURCES:")
                logger.info("-" * 30)
                resources = await session.list_resources()
                if resources.resources:
                    for resource in resources.resources:
                        logger.info(f"  • {resource.uri} - {resource.description}")
                else:
                    logger.info("  No static resources found")

                # List available resource templates
                logger.info("📋 LISTING RESOURCE TEMPLATES:")
                logger.info("-" * 30)
                templates = await session.list_resource_templates()
                if templates.resourceTemplates:
                    for template in templates.resourceTemplates:
                        logger.info(f"  • {template.uriTemplate} - {template.description}")
                else:
                    logger.info("  No resource templates found")

                # List available tools
                logger.info("🔧 LISTING TOOLS:")
                logger.info("-" * 30)
                tools = await session.list_tools()
                if tools.tools:
                    for tool in tools.tools:
                        logger.info(f"  • {tool.name} - {tool.description}")
                else:
                    logger.info("  No tools found")

                # Test reading resources (using dynamic templates)
                logger.info("📖 TESTING RESOURCES:")
                logger.info("-" * 30)
                try:
                    # Test dynamic resources from utils/resources.py
                    result = await session.read_resource("greeting://Pedro")
                    logger.info(f"  greeting://Pedro → {result.contents[0].text}")
                    
                    result = await session.read_resource("farewell://Pedro")
                    logger.info(f"  farewell://Pedro → {result.contents[0].text}")
                    
                    # Test with different names
                    result = await session.read_resource("greeting://Docker")
                    logger.info(f"  greeting://Docker → {result.contents[0].text}")
                    
                    result = await session.read_resource("farewell://MCP")
                    logger.info(f"  farewell://MCP → {result.contents[0].text}")
                except Exception as e:
                    logger.error(f"  ❌ Error reading resource: {e}")

                # Test calling tools
                logger.info("⚙️ TESTING TOOLS:")
                logger.info("-" * 30)
                try:
                    # Test add tool
                    result = await session.call_tool("add_tool", arguments={"a": 5, "b": 3})
                    logger.info(f"  add_tool(5, 3) → {result.content[0].text}")
                    
                    # Test subtract tool
                    result = await session.call_tool("subtract_tool", arguments={"a": 10, "b": 4})
                    logger.info(f"  subtract_tool(10, 4) → {result.content[0].text}")
                except Exception as e:
                    logger.error(f"  ❌ Error calling tool: {e}")

                logger.info("🎉 All tests completed!")

    except Exception as e:
        logger.error(f"❌ Error connecting to server: {e}")
        logger.error("Make sure the server.py file is in the same directory")


if __name__ == "__main__":
    logger.info("MCP Client Test")
    logger.info("===============")
    asyncio.run(run())