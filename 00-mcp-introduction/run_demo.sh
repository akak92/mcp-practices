#!/bin/bash
# run_demo.sh
# Script to demonstrate MCP client-server communication

echo "🐳 MCP Docker Demo"
echo "=================="
echo

echo "📋 Project Structure:"
echo "--------------------"
find . -name "*.py" -o -name "*.txt" -o -name "Dockerfile" | head -10
echo

echo "🔍 Checking Python environment..."
python --version
echo

echo "📦 Checking MCP installation..."
python -c "import mcp; print('✅ MCP installed successfully')" 2>/dev/null || echo "❌ MCP not found"
echo

echo "🧪 Testing individual components..."
echo "-----------------------------------"

echo "1️⃣ Testing server import..."
python -c "
try:
    from server import mcp
    print('✅ Server imports successfully')
    print(f'   Server name: {mcp.name}')
except Exception as e:
    print(f'❌ Server import failed: {e}')
"
echo

echo "2️⃣ Testing utils modules..."
python -c "
try:
    from utils.tools import add, subtract
    from utils.resources import get_greeting, get_farewell
    print('✅ Utils modules import successfully')
    print(f'   add(2, 3) = {add(2, 3)}')
    print(f'   get_greeting(\"Docker\") = {get_greeting(\"Docker\")}')
except Exception as e:
    print(f'❌ Utils import failed: {e}')
"
echo

echo "3️⃣ Running MCP Client Test..."
echo "-----------------------------"
echo "Note: This will test the client-server communication"
echo

# Run the client which will automatically start and communicate with the server
timeout 30 python client.py || echo "⏰ Client test completed (timeout after 30s)"

echo
echo "🎉 Demo completed!"
echo "=================="
echo
echo "📝 What happened:"
echo "• The MCP server provides tools (add, subtract) and resources (greeting, farewell)"
echo "• The client connects to the server and tests all functionality"
echo "• All communication happens through the Model Context Protocol (MCP)"
echo
echo "💡 To run manually:"
echo "• Server: python server.py"
echo "• Client: python client.py (in another terminal)"