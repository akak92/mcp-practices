from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

# HTTP client for local LLM
import httpx
import json
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
    args=["server.py"],  # Your MCP server script
    env=None,  # Optional environment variables
)

async def call_llm(prompt, functions):
    """
    Call your BFF proxy at localhost:9900/chat that connects to Ollama
    """
    url = "http://localhost:9900/chat"
    
    # Use the exact format from your curl example
    payload = {
        "model": "qwen3:1.7b",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }
    
    # If we have tools available, add context about them in the prompt
    if functions:
        tool_descriptions = []
        for func in functions:
            name = func["function"]["name"]
            desc = func["function"]["description"]
            params = func["function"]["parameters"]["properties"]
            tool_descriptions.append(f"- {name}: {desc} (parameters: {list(params.keys())})")
        
        # Enhance the prompt with tool information
        enhanced_prompt = f"""{prompt}

Available tools:
{chr(10).join(tool_descriptions)}

If you need to use any tool to answer this question, please indicate which tool and what parameters to use."""
        
        payload["messages"][0]["content"] = enhanced_prompt
    
    logger.info("🤖 CALLING BFF PROXY at %s", url)
    logger.info("📝 Prompt: %s", prompt)
    logger.info("🔧 Available tools: %d", len(functions) if functions else 0)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info("✅ BFF Response: %s", result)
            
            # Extract function calls from the LLM response
            functions_to_call = []
            
            # Handle different response formats from your BFF
            content = ""
            if "choices" in result and result["choices"]:
                message = result["choices"][0].get("message", {})
                content = message.get("content", "")
            elif "content" in result:
                # Direct content format from your BFF
                content = result["content"]
            elif "message" in result and "content" in result["message"]:
                content = result["message"]["content"]
            
            logger.info("💬 LLM Response: %s", content)
            
            # Parse the text response to identify tool usage
            if functions and content:
                content_lower = content.lower()
                
                # Look for tool mentions in the response
                for func in functions:
                    tool_name = func["function"]["name"]
                    
                    # Check if LLM mentioned using the tool or if we should use it
                    if any(phrase in content_lower for phrase in [
                        tool_name.lower(), 
                        "add_tool", 
                        "herramienta", 
                        "tool",
                        "suma",
                        "add"
                    ]):
                        if "add" in tool_name.lower():
                            # Extract numbers from the response or original prompt
                            import re
                            # Look for numbers in both the original prompt and LLM response
                            all_text = prompt + " " + content
                            numbers = re.findall(r'\b(\d+)\b', all_text)
                            if len(numbers) >= 2:
                                # Convert to integers and take first two
                                a, b = int(numbers[0]), int(numbers[1])
                                logger.info("🎯 Detected %s usage with numbers: %d + %d", tool_name, a, b)
                                functions_to_call.append({
                                    "name": tool_name,
                                    "args": {"a": a, "b": b}
                                })
                                break
            
            return functions_to_call
            
    except httpx.RequestError as e:
        logger.error("❌ Request error: %s", e)
        logger.error("💡 Make sure your BFF proxy is running on localhost:9900")
        return []
    except httpx.HTTPStatusError as e:
        logger.error("❌ HTTP error: %d - %s", e.response.status_code, e.response.text)
        return []
    except Exception as e:
        logger.error("❌ Unexpected error: %s", e)
        return []

def convert_to_llm_tool(tool):
    tool_schema = {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "type": "function",
            "parameters": {
                "type": "object",
                "properties": tool.inputSchema["properties"]
            }
        }
    }

    return tool_schema

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()
            logger.info("✅ Connected to MCP server")

            # List available resources
            resources = await session.list_resources()
            logger.info("📁 LISTING RESOURCES")
            for resource in resources.resources:
                logger.info("Resource: %s", resource.uri)

            # List available tools
            tools = await session.list_tools()
            logger.info("🔧 LISTING TOOLS")

            functions = []

            for tool in tools.tools:
                logger.info("Tool: %s - %s", tool.name, tool.description)
                logger.info("Tool Schema: %s", tool.inputSchema.get("properties", {}))
                functions.append(convert_to_llm_tool(tool))
            
            # Test prompt - you can change this
            prompt = "Can you help me add 15 and 25?"
            logger.info("🎯 User Query: %s", prompt)

            # Ask LLM what tools to call, if any
            functions_to_call = await call_llm(prompt, functions)

            # Call suggested functions
            if functions_to_call:
                logger.info("🔧 Executing %d tool call(s):", len(functions_to_call))
                for f in functions_to_call:
                    logger.info("  Calling %s with args: %s", f['name'], f['args'])
                    result = await session.call_tool(f["name"], arguments=f["args"])
                    logger.info("  Result: %s", result.content)
            else:
                logger.info("💭 No tool calls needed for this query")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())


