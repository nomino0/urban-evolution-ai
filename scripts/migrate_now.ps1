# Urban Evolution AI - Complete Migration Script
Write-Host "Migration and Cleanup Starting..." -ForegroundColor Cyan

# Create backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "..\urban-evolution-ai-backup-$timestamp"
Write-Host "Creating backup at: $backupPath" -ForegroundColor Yellow
New-Item -Path $backupPath -ItemType Directory -Force | Out-Null
$excludeDirs = @(".git", "venv", "venv-ml", "venv-backend", "node_modules", "__pycache__")
Get-ChildItem -Path "." -Exclude $excludeDirs | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $backupPath -Recurse -Force -ErrorAction SilentlyContinue
}
Write-Host "Backup created" -ForegroundColor Green

# Helper function
function Move-FilesToNew {
    param([string]$Source, [string]$Dest)
    if (Test-Path $Source) {
        if (-not (Test-Path $Dest)) { New-Item -Path $Dest -ItemType Directory -Force | Out-Null }
        Copy-Item -Path $Source -Destination $Dest -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  Moved: $Source to $Dest" -ForegroundColor Gray
    }
}

# Move ML files
Write-Host "Moving ML Pipeline files..." -ForegroundColor Cyan
if (Test-Path "src\data") { Move-FilesToNew "src\data\*" "ml-pipeline\data_collection\" }
if (Test-Path "src\models\detection") { Move-FilesToNew "src\models\detection\*" "ml-pipeline\models\detection\" }
if (Test-Path "src\models\growth_forecasting") { Move-FilesToNew "src\models\growth_forecasting\*" "ml-pipeline\models\growth_forecasting\" }
if (Test-Path "models\yolo") { Move-FilesToNew "models\yolo\*" "ml-pipeline\trained_models\yolo\" }
if (Test-Path "models\sam") { Move-FilesToNew "models\sam\*" "ml-pipeline\trained_models\sam\" }
if (Test-Path "models\growth") { Move-FilesToNew "models\growth\*" "ml-pipeline\trained_models\growth\" }

# Move backend files
Write-Host "Moving Backend files..." -ForegroundColor Cyan
if (Test-Path "src\api") { Move-FilesToNew "src\api\*" "app\backend\api\" }
if (Test-Path "src\services") { Move-FilesToNew "src\services\*" "app\backend\services\" }
if (Test-Path "src\agents") { Move-FilesToNew "src\agents\*" "app\backend\agents\" }

# Move shared files
Write-Host "Moving Shared files..." -ForegroundColor Cyan
if (Test-Path "configs") { Move-FilesToNew "configs\*" "shared\configs\" }
if (Test-Path "src\utils") { Move-FilesToNew "src\utils\*" "shared\utils\" }

# Create __init__.py files
Write-Host "Creating __init__.py files..." -ForegroundColor Cyan
$initDirs = @("ml-pipeline", "ml-pipeline\data_collection", "ml-pipeline\models", "ml-pipeline\models\detection", "ml-pipeline\models\growth_forecasting", "ml-pipeline\training", "app\backend", "app\backend\api", "app\backend\services", "app\backend\agents", "shared", "shared\configs", "shared\utils")
foreach ($dir in $initDirs) {
    if (Test-Path $dir) {
        $initFile = Join-Path $dir "__init__.py"
        if (-not (Test-Path $initFile)) { "" | Out-File -FilePath $initFile -Encoding UTF8 }
    }
}

# Clean up old directories
Write-Host "Cleaning up old directories..." -ForegroundColor Yellow
$dirsToRemove = @("src", "configs", "data", "models", "notebooks", "experiments", "frontend", "monitoring", "outputs")
foreach ($dir in $dirsToRemove) {
    if (Test-Path $dir) {
        try {
            Remove-Item -Path $dir -Recurse -Force -ErrorAction Stop
            Write-Host "  Removed: $dir" -ForegroundColor Green
        } catch {
            Write-Host "  Could not remove: $dir" -ForegroundColor Yellow
        }
    }
}

# Remove old requirements.txt
if (Test-Path "requirements.txt") {
    try { Remove-Item -Path "requirements.txt" -Force ; Write-Host "  Removed: requirements.txt" -ForegroundColor Green }
    catch { Write-Host "  Could not remove requirements.txt" -ForegroundColor Yellow }
}

Write-Host ""
Write-Host "Migration Complete!" -ForegroundColor Green
Write-Host "Backup saved at: $backupPath" -ForegroundColor Cyan
Write-Host "Old directories removed" -ForegroundColor Green
