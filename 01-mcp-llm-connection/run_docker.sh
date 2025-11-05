#!/bin/bash
# run_docker.sh
# Script to build and run the MCP-LLM Docker container

echo "🐳 MCP-LLM Docker Setup"
echo "========================"
echo

echo "📋 Building Docker image..."
docker build -t mcp-llm-client .

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
    echo
    
    echo "🚀 Running MCP-LLM client..."
    echo "💡 Make sure your BFF is running on host at localhost:9900"
    echo
    
    # Use host networking to access localhost:9900 from container
    docker run --rm --network="host" mcp-llm-client
else
    echo "❌ Docker build failed!"
    echo "Make sure Docker is installed and running."
fi

echo
echo "💡 Manual commands:"
echo "• Build: docker build -t mcp-llm-client ."
echo "• Run: docker run --rm --network=\"host\" mcp-llm-client"
echo "• Interactive: docker run --rm -it --network=\"host\" mcp-llm-client bash"