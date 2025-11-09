# Urban Evolution AI Platform - Quick Start Script
# PowerShell script to quickly verify project setup

Write-Host "🌆 Urban Evolution AI Platform - Setup Verification" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "1. Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.(1[0-9]|[2-9][0-9])") {
    Write-Host "✅ Python version OK: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "❌ Python 3.10+ required. Found: $pythonVersion" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if virtual environment exists
Write-Host "2. Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "✅ Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not found. Creating..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Check .env file
Write-Host "3. Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file exists" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ .env file created" -ForegroundColor Green
    Write-Host "⚠️  Remember to add your API keys to .env!" -ForegroundColor Yellow
}
Write-Host ""

# Check project structure
Write-Host "4. Checking project structure..." -ForegroundColor Yellow
$requiredDirs = @(
    "src",
    "src/api",
    "src/agents",
    "src/models",
    "src/services",
    "configs",
    "data",
    "outputs",
    "docs"
)

$allDirsExist = $true
foreach ($dir in $requiredDirs) {
    if (!(Test-Path $dir)) {
        Write-Host "❌ Missing directory: $dir" -ForegroundColor Red
        $allDirsExist = $false
    }
}

if ($allDirsExist) {
    Write-Host "✅ All required directories exist" -ForegroundColor Green
}
Write-Host ""

# Check key files
Write-Host "5. Checking key files..." -ForegroundColor Yellow
$requiredFiles = @(
    "requirements.txt",
    "pyproject.toml",
    "README.md",
    "src/api/main.py",
    "src/services/gemini_flash_service.py",
    "src/utils/logger.py",
    "configs/model_config.yaml",
    "configs/agent_config.yaml"
)

$allFilesExist = $true
foreach ($file in $requiredFiles) {
    if (!(Test-Path $file)) {
        Write-Host "❌ Missing file: $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if ($allFilesExist) {
    Write-Host "✅ All required files exist" -ForegroundColor Green
}
Write-Host ""

# Summary
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "Setup Verification Complete!" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Activate virtual environment:" -ForegroundColor White
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Install dependencies:" -ForegroundColor White
Write-Host "   pip install -r requirements.txt" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Configure your API keys in .env file" -ForegroundColor White
Write-Host ""
Write-Host "4. Start the backend:" -ForegroundColor White
Write-Host "   uvicorn src.api.main:app --reload --port 8000" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Visit:" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host "   Health Check: http://localhost:8000/health" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Yellow
Write-Host "   - README.md" -ForegroundColor Gray
Write-Host "   - docs/GETTING_STARTED.md" -ForegroundColor Gray
Write-Host "   - PROJECT_SUMMARY.md" -ForegroundColor Gray
Write-Host ""
Write-Host "🚀 Happy coding!" -ForegroundColor Green
