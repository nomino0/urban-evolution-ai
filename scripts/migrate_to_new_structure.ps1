# Urban Evolution AI - Automated Structure Migration Script
# This script migrates from the old monolithic structure to the new separated architecture

Write-Host "🔄 Urban Evolution AI - Structure Migration" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "PROJECT_INIT.md")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "⚠️  WARNING: This script will reorganize your project structure." -ForegroundColor Yellow
Write-Host "A backup will be created before making changes." -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Do you want to continue? (yes/no)"

if ($confirm -ne "yes") {
    Write-Host "Migration cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Step 1: Creating backup..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "..\urban-evolution-ai-backup-$timestamp"

try {
    $excludeDirs = @(".git", "venv", "venv-ml", "venv-backend", "node_modules", "__pycache__", ".next", "dist", "build")
    
    Write-Host "Creating backup at: $backupPath" -ForegroundColor Gray
    
    # Create backup directory
    New-Item -Path $backupPath -ItemType Directory -Force | Out-Null
    
    # Copy all files except excluded directories
    Get-ChildItem -Path "." -Exclude $excludeDirs | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $backupPath -Recurse -Force
    }
    
    Write-Host "✅ Backup created successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to create backup: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 2: Checking if files need migration..." -ForegroundColor Yellow

# Check if old structure exists
$needsMigration = $false

if (Test-Path "src\data") {
    $needsMigration = $true
    Write-Host "Found: src\data (needs migration)" -ForegroundColor Gray
}

if (Test-Path "src\models") {
    $needsMigration = $true
    Write-Host "Found: src\models (needs migration)" -ForegroundColor Gray
}

if (-not $needsMigration) {
    Write-Host "✅ Project already using new structure or no files to migrate" -ForegroundColor Green
    Write-Host ""
    Write-Host "New structure is ready to use!" -ForegroundColor Cyan
    exit 0
}

Write-Host ""
Write-Host "Step 3: Migrating files to new structure..." -ForegroundColor Yellow

# Helper function to safely move items
function Move-ItemSafe {
    param(
        [string]$Source,
        [string]$Destination
    )
    
    if (Test-Path $Source) {
        try {
            # Create destination directory if it doesn't exist
            $destDir = Split-Path -Parent $Destination
            if (-not (Test-Path $destDir)) {
                New-Item -Path $destDir -ItemType Directory -Force | Out-Null
            }
            
            # Copy item
            Copy-Item -Path $Source -Destination $Destination -Recurse -Force
            Write-Host "  ✓ Migrated: $Source → $Destination" -ForegroundColor Gray
            return $true
        } catch {
            Write-Host "  ⚠️  Failed to migrate: $Source ($_)" -ForegroundColor Yellow
            return $false
        }
    }
    return $false
}

# Migrate ML Pipeline files
Write-Host ""
Write-Host "Migrating ML Pipeline files..." -ForegroundColor Cyan

if (Test-Path "src\data") {
    Get-ChildItem "src\data\*.py" | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "ml-pipeline\data_collection\$($_.Name)"
    }
}

if (Test-Path "src\models\detection") {
    Get-ChildItem "src\models\detection\*.py" | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "ml-pipeline\models\detection\$($_.Name)"
    }
}

if (Test-Path "src\models\growth_forecasting") {
    Get-ChildItem "src\models\growth_forecasting\*.py" | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "ml-pipeline\models\growth_forecasting\$($_.Name)"
    }
}

if (Test-Path "notebooks") {
    Get-ChildItem "notebooks\*" | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "ml-pipeline\notebooks\$($_.Name)"
    }
}

if (Test-Path "data\raw") {
    Get-ChildItem "data\raw\*" -ErrorAction SilentlyContinue | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "ml-pipeline\datasets\raw\$($_.Name)"
    }
}

if (Test-Path "data\processed") {
    Get-ChildItem "data\processed\*" -ErrorAction SilentlyContinue | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "ml-pipeline\datasets\processed\$($_.Name)"
    }
}

if (Test-Path "experiments") {
    Get-ChildItem "experiments\*" | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "ml-pipeline\experiments\$($_.Name)"
    }
}

# Migrate Application files
Write-Host ""
Write-Host "Migrating Application files..." -ForegroundColor Cyan

if (Test-Path "src\api") {
    Get-ChildItem "src\api\*" -Recurse | ForEach-Object {
        if ($_.PSIsContainer) {
            # Create directory structure
            $relativePath = $_.FullName.Replace((Get-Location).Path + "\src\api\", "")
            New-Item -Path "app\backend\api\$relativePath" -ItemType Directory -Force -ErrorAction SilentlyContinue | Out-Null
        } else {
            # Copy file
            $relativePath = $_.FullName.Replace((Get-Location).Path + "\src\api\", "")
            Move-ItemSafe -Source $_.FullName -Destination "app\backend\api\$relativePath"
        }
    }
}

if (Test-Path "src\services") {
    Get-ChildItem "src\services\*.py" | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "app\backend\services\$($_.Name)"
    }
}

if (Test-Path "src\agents") {
    Get-ChildItem "src\agents\*" -Recurse | ForEach-Object {
        if (-not $_.PSIsContainer) {
            $relativePath = $_.FullName.Replace((Get-Location).Path + "\src\agents\", "")
            Move-ItemSafe -Source $_.FullName -Destination "app\backend\agents\$relativePath"
        }
    }
}

# Migrate Shared files
Write-Host ""
Write-Host "Migrating Shared files..." -ForegroundColor Cyan

if (Test-Path "configs") {
    Get-ChildItem "configs\*" | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "shared\configs\$($_.Name)"
    }
}

if (Test-Path "src\utils") {
    Get-ChildItem "src\utils\*.py" | ForEach-Object {
        Move-ItemSafe -Source $_.FullName -Destination "shared\utils\$($_.Name)"
    }
}

# Create __init__.py files
Write-Host ""
Write-Host "Step 4: Creating __init__.py files..." -ForegroundColor Yellow

$initDirs = @(
    "ml-pipeline",
    "ml-pipeline\data_collection",
    "ml-pipeline\models",
    "ml-pipeline\models\detection",
    "ml-pipeline\models\growth_forecasting",
    "ml-pipeline\training",
    "app\backend",
    "app\backend\api",
    "app\backend\api\routers",
    "app\backend\api\models",
    "app\backend\api\middleware",
    "app\backend\services",
    "app\backend\agents",
    "app\backend\agents\tools",
    "app\backend\database",
    "app\backend\tasks",
    "shared",
    "shared\configs",
    "shared\utils"
)

foreach ($dir in $initDirs) {
    if (Test-Path $dir) {
        $initFile = Join-Path $dir "__init__.py"
        if (-not (Test-Path $initFile)) {
            "" | Out-File -FilePath $initFile -Encoding UTF8
            Write-Host "  ✓ Created: $initFile" -ForegroundColor Gray
        }
    }
}

# Create .gitkeep files for empty directories
Write-Host ""
Write-Host "Step 5: Creating .gitkeep files..." -ForegroundColor Yellow

$gitkeepDirs = @(
    "ml-pipeline\datasets\raw",
    "ml-pipeline\datasets\processed",
    "ml-pipeline\trained_models",
    "ml-pipeline\experiments\mlruns",
    "app\backend\models"
)

foreach ($dir in $gitkeepDirs) {
    if (Test-Path $dir) {
        $gitkeepFile = Join-Path $dir ".gitkeep"
        if (-not (Test-Path $gitkeepFile)) {
            "" | Out-File -FilePath $gitkeepFile -Encoding UTF8
            Write-Host "  ✓ Created: $gitkeepFile" -ForegroundColor Gray
        }
    }
}

Write-Host ""
Write-Host "Step 6: Validation..." -ForegroundColor Yellow

$allGood = $true

# Check if key directories exist
$requiredDirs = @(
    "ml-pipeline",
    "ml-pipeline\data_collection",
    "ml-pipeline\models",
    "app\backend",
    "app\backend\api",
    "app\frontend",
    "shared"
)

foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ Found: $dir" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Missing: $dir" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "✅ Migration completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Review MIGRATION_GUIDE.md for manual adjustments" -ForegroundColor White
    Write-Host "2. Update import statements in Python files" -ForegroundColor White
    Write-Host "3. Create separate virtual environments:" -ForegroundColor White
    Write-Host "   - ml-pipeline: .\ml-pipeline\venv-ml" -ForegroundColor Gray
    Write-Host "   - backend: .\app\backend\venv-backend" -ForegroundColor Gray
    Write-Host "4. Install dependencies in each environment" -ForegroundColor White
    Write-Host "5. Test each component independently" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Documentation:" -ForegroundColor Yellow
    Write-Host "   - ARCHITECTURE.md: New structure overview" -ForegroundColor Gray
    Write-Host "   - MIGRATION_GUIDE.md: Detailed migration steps" -ForegroundColor Gray
    Write-Host "   - ml-pipeline/README.md: ML pipeline guide" -ForegroundColor Gray
    Write-Host "   - app/backend/README.md: Backend guide" -ForegroundColor Gray
    Write-Host "   - app/frontend/README.md: Frontend guide" -ForegroundColor Gray
    Write-Host ""
    Write-Host "💾 Backup location: $backupPath" -ForegroundColor Cyan
} else {
    Write-Host "⚠️  Migration completed with warnings" -ForegroundColor Yellow
    Write-Host "Please review the output above and check MIGRATION_GUIDE.md" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Your project is now using the new architecture!" -ForegroundColor Green
