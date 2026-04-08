# MyQA Agent - PowerShell Startup Script
# Run this file to start the application

param(
    [switch]$Help = $false,
    [int]$Port = 8000,
    [string]$HostAddress = "0.0.0.0"
)

if ($Help) {
    Write-Host "MyQA Agent - PowerShell Startup Script" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\START_SERVER.ps1 [-Port 8000] [-Host 0.0.0.0] [-Help]"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\START_SERVER.ps1                    # Start on default port 8000"
    Write-Host "  .\START_SERVER.ps1 -Port 9000         # Start on port 9000"
    Write-Host "  .\START_SERVER.ps1 -Host localhost    # Bind to localhost only"
    exit 0
}

# Get project directory
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

# Check if virtual environment exists
if (-not (Test-Path $VenvPython)) {
    Write-Host "❌ Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Expected: $VenvPython"
    Write-Host ""
    Write-Host "Create it with: python -m venv .venv"
    exit 1
}

# Display information
Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║          🚀 MyQA Agent - Application Startup              ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Project Directory: $ProjectRoot" -ForegroundColor Cyan
Write-Host "🐍 Python: $VenvPython" -ForegroundColor Cyan
Write-Host "🌐 Server: http://$($HostAddress):$Port" -ForegroundColor Cyan
Write-Host "⏰ Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting Uvicorn server..." -ForegroundColor Yellow
Write-Host ""

# Change to project directory
Set-Location $ProjectRoot

# Start the server
try {
    & $VenvPython -m uvicorn app.main:app --host $HostAddress --port $Port
}
catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
    exit 1
}
