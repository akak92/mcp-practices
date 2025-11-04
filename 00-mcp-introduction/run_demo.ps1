# run_demo.ps1
# PowerShell script to build and run the MCP Docker demo

Write-Host "🐳 MCP Docker Demo - PowerShell" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan
Write-Host

Write-Host "📋 Building Docker image..." -ForegroundColor Yellow
docker build -t mcp-demo .

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Docker image built successfully!" -ForegroundColor Green
    Write-Host
    
    Write-Host "🚀 Running MCP demo..." -ForegroundColor Yellow
    docker run --rm mcp-demo
} else {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    Write-Host "Make sure Docker is installed and running." -ForegroundColor Red
}

Write-Host
Write-Host "💡 To run individual commands:" -ForegroundColor Cyan
Write-Host "• Build: docker build -t mcp-demo ." -ForegroundColor White
Write-Host "• Run: docker run --rm mcp-demo" -ForegroundColor White
Write-Host "• Interactive: docker run --rm -it mcp-demo bash" -ForegroundColor White