# Urban Evolution AI - Complete Setup Script
# This script sets up all three environments

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Urban Evolution AI - Complete Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = "d:\Tek-UP\5eme SDIA\Projects\urban-evolution-ai"

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Python not found. Please install Python 3.10+ first." -ForegroundColor Red
    exit 1
}

# Check Node.js installation
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  Found Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  WARNING: Node.js not found. Frontend setup will be skipped." -ForegroundColor Yellow
    $nodeInstalled = $false
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Step 1: ML Pipeline Environment Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "This will install ~3GB of ML dependencies" -ForegroundColor Yellow
Write-Host ""

$setupML = Read-Host "Setup ML Pipeline environment? (yes/no)"
if ($setupML -eq "yes") {
    Write-Host "Creating ML Pipeline virtual environment..." -ForegroundColor Yellow
    cd "$projectRoot\ml-pipeline"
    
    if (Test-Path "venv-ml") {
        Write-Host "  Removing existing venv-ml..." -ForegroundColor Gray
        Remove-Item -Path "venv-ml" -Recurse -Force
    }
    
    python -m venv venv-ml
    Write-Host "  Virtual environment created" -ForegroundColor Green
    
    Write-Host "Installing ML dependencies (this will take several minutes)..." -ForegroundColor Yellow
    .\venv-ml\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements-ml.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ML Pipeline environment ready!" -ForegroundColor Green
    } else {
        Write-Host "  WARNING: Some packages may have failed to install" -ForegroundColor Yellow
    }
    
    deactivate
} else {
    Write-Host "Skipping ML Pipeline setup" -ForegroundColor Gray
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Step 2: Backend Environment Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "This will install ~500MB of backend dependencies" -ForegroundColor Yellow
Write-Host ""

$setupBackend = Read-Host "Setup Backend environment? (yes/no)"
if ($setupBackend -eq "yes") {
    Write-Host "Creating Backend virtual environment..." -ForegroundColor Yellow
    cd "$projectRoot\app\backend"
    
    if (Test-Path "venv-backend") {
        Write-Host "  Removing existing venv-backend..." -ForegroundColor Gray
        Remove-Item -Path "venv-backend" -Recurse -Force
    }
    
    python -m venv venv-backend
    Write-Host "  Virtual environment created" -ForegroundColor Green
    
    Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
    .\venv-backend\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -r requirements-backend.txt
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Backend environment ready!" -ForegroundColor Green
    } else {
        Write-Host "  WARNING: Some packages may have failed to install" -ForegroundColor Yellow
    }
    
    deactivate
} else {
    Write-Host "Skipping Backend setup" -ForegroundColor Gray
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Step 3: Frontend Environment Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "This will install ~200MB of Node dependencies" -ForegroundColor Yellow
Write-Host ""

if ($nodeInstalled -ne $false) {
    $setupFrontend = Read-Host "Setup Frontend environment? (yes/no)"
    if ($setupFrontend -eq "yes") {
        Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
        cd "$projectRoot\app\frontend"
        
        if (Test-Path "node_modules") {
            Write-Host "  Removing existing node_modules..." -ForegroundColor Gray
            Remove-Item -Path "node_modules" -Recurse -Force
        }
        
        npm install
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  Frontend environment ready!" -ForegroundColor Green
        } else {
            Write-Host "  WARNING: Some packages may have failed to install" -ForegroundColor Yellow
        }
    } else {
        Write-Host "Skipping Frontend setup" -ForegroundColor Gray
    }
} else {
    Write-Host "Node.js not installed. Skipping Frontend setup." -ForegroundColor Gray
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Step 4: Environment Configuration" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

cd $projectRoot

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    
    $envContent = @"
# Urban Evolution AI - Environment Variables

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_EARTH_ENGINE_PROJECT=your_gee_project_id
OPENAI_API_KEY=your_openai_key_for_agents

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/urban_evolution
# Or use SQLite for development:
# DATABASE_URL=sqlite:///./urban_evolution.db

# Redis (for caching and task queue)
REDIS_URL=redis://localhost:6379/0

# MLflow (for experiment tracking)
MLFLOW_TRACKING_URI=http://localhost:5000

# Application
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_MAPBOX_TOKEN=your_mapbox_token
"@
    
    Set-Content -Path ".env" -Value $envContent
    Write-Host "  .env file created" -ForegroundColor Green
    Write-Host "  Please update with your actual API keys" -ForegroundColor Yellow
} else {
    Write-Host ".env file already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Update .env file with your API keys" -ForegroundColor White
Write-Host ""
Write-Host "2. Start ML Pipeline:" -ForegroundColor White
Write-Host "   cd ml-pipeline" -ForegroundColor Gray
Write-Host "   .\venv-ml\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   python data_collection/download_sentinel.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Start Backend:" -ForegroundColor White
Write-Host "   cd app\backend" -ForegroundColor Gray
Write-Host "   .\venv-backend\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "   uvicorn api.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Start Frontend:" -ForegroundColor White
Write-Host "   cd app\frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - README.md: Project overview" -ForegroundColor Gray
Write-Host "  - QUICK_REFERENCE.md: Commands cheat sheet" -ForegroundColor Gray
Write-Host "  - Component READMEs in each directory" -ForegroundColor Gray
Write-Host ""
Write-Host "Happy coding! " -ForegroundColor Green
