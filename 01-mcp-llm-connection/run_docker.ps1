# run_docker.ps1
# PowerShell script to build and run the MCP-LLM Docker container

Write-Host "🐳 MCP-LLM Docker Setup" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan
Write-Host

Write-Host "📋 Building Docker image..." -ForegroundColor Yellow
docker build -t mcp-llm-client .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
    Write-Host
    
    Write-Host "🚀 Running MCP-LLM client..." -ForegroundColor Yellow
    Write-Host "💡 Make sure your BFF is running on host at localhost:9900" -ForegroundColor Cyan
    Write-Host
    
    # Use host networking to access localhost:9900 from container
    docker run --rm --network="host" mcp-llm-client
} else {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    Write-Host "Make sure Docker is installed and running." -ForegroundColor Red
}

Write-Host
Write-Host "💡 Manual commands:" -ForegroundColor Cyan
Write-Host "• Build: docker build -t mcp-llm-client ." -ForegroundColor White
Write-Host "• Run: docker run --rm --network=`"host`" mcp-llm-client" -ForegroundColor White
Write-Host "• Interactive: docker run --rm -it --network=`"host`" mcp-llm-client bash" -ForegroundColor White