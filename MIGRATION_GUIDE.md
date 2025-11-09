# 🔄 Migration Guide: Old Structure → New Architecture

This guide helps you migrate from the original monolithic structure to the new separated architecture.

## 📋 Overview

We're reorganizing the project into three main sections:

```
OLD STRUCTURE                    NEW STRUCTURE
==================              ==================
src/                            ml-pipeline/         (ML & Data Science)
├── data/        ─────────────> ├── data_collection/
├── models/      ─────────────> ├── models/
├── agents/      ─────────────> └── training/
├── services/    ───────┐
└── api/         ───────┤
                        ├─────> app/                (Production App)
data/            ───────┤       ├── backend/
configs/         ───────┤       │   ├── api/
notebooks/       ───────┤       │   ├── services/
frontend/        ───────┤       │   └── agents/
                        │       └── frontend/
                        │
                        └─────> shared/             (Common Code)
                                ├── configs/
                                └── utils/
```

## 🚀 Automated Migration Script

We've created a PowerShell script to automate the migration:

```powershell
# Run from project root
.\scripts\migrate_to_new_structure.ps1
```

**What it does:**
1. Creates backup of current structure
2. Copies files to new locations
3. Updates import statements
4. Creates necessary __init__.py files
5. Validates the migration

## 📝 Manual Migration Steps

If you prefer to migrate manually, follow these steps:

### Step 1: Backup Current Structure

```powershell
# Create backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item -Path "." -Destination "..\urban-evolution-ai-backup-$timestamp" -Recurse -Exclude ".git","venv","node_modules","__pycache__"
```

### Step 2: Move ML/Data Science Files

```powershell
# Data collection scripts
Move-Item "src\data\download_*.py" "ml-pipeline\data_collection\"
Move-Item "src\data\aligned_download.py" "ml-pipeline\data_collection\"
Move-Item "src\data\define_city_boundaries.py" "ml-pipeline\data_collection\"
Move-Item "src\data\create_tile_grids.py" "ml-pipeline\data_collection\"

# ML Models
Move-Item "src\models\detection\*" "ml-pipeline\models\detection\"
Move-Item "src\models\growth_forecasting\*" "ml-pipeline\models\growth_forecasting\"

# Training scripts (if any exist in src/)
Move-Item "src\models\training\*" "ml-pipeline\training\" -ErrorAction SilentlyContinue

# Notebooks
Move-Item "notebooks\*" "ml-pipeline\notebooks\"

# Datasets
Move-Item "data\raw\*" "ml-pipeline\datasets\raw\"
Move-Item "data\processed\*" "ml-pipeline\datasets\processed\"

# Trained models
Move-Item "models\*" "ml-pipeline\trained_models\" -ErrorAction SilentlyContinue

# Experiments
Move-Item "experiments\*" "ml-pipeline\experiments\"
```

### Step 3: Move Application Files

```powershell
# Backend API
Move-Item "src\api\*" "app\backend\api\"

# Services (keep only production services)
Move-Item "src\services\gemini_flash_service.py" "app\backend\services\"
# Add other production services here

# Agents
Move-Item "src\agents\*" "app\backend\agents\"

# Database
New-Item -Path "app\backend\database" -ItemType Directory
Move-Item "src\api\models\database.py" "app\backend\database\models.py"

# Frontend
Move-Item "frontend\*" "app\frontend\" -ErrorAction SilentlyContinue
```

### Step 4: Move Shared Files

```powershell
# Configurations
Move-Item "configs\*" "shared\configs\"

# Utilities
Move-Item "src\utils\*" "shared\utils\"
```

### Step 5: Update Import Statements

You'll need to update import statements in your Python files:

**Old imports:**
```python
from src.models.detection.yolo_detector import YOLODetector
from src.utils.logger import setup_logger
from configs.model_config import load_config
```

**New imports (ML Pipeline):**
```python
# In ml-pipeline files
from models.detection.yolo_detector import YOLODetector
from shared.utils.logger import setup_logger
from shared.configs.model_config import load_config
```

**New imports (Backend):**
```python
# In app/backend files
from services.gemini_flash_service import GeminiFlashService
from database.models import City, Building
from shared.utils.logger import setup_logger
```

### Step 6: Update Requirements Files

**Replace old requirements.txt with:**

```powershell
# ML Pipeline
Copy-Item "requirements.txt" "ml-pipeline\requirements-ml.txt"

# Backend
Copy-Item "requirements.txt" "app\backend\requirements-backend.txt"

# Then manually edit each file to remove unnecessary dependencies
```

Edit `ml-pipeline/requirements-ml.txt`:
- Keep: PyTorch, TensorFlow, YOLO, geospatial libs, MLflow, Jupyter
- Remove: FastAPI, Uvicorn, authentication libs

Edit `app/backend/requirements-backend.txt`:
- Keep: FastAPI, SQLAlchemy, LangChain, auth libs, lightweight ML
- Remove: Heavy ML libs (full PyTorch, TensorFlow), Jupyter, MLflow

### Step 7: Update Configuration Paths

Update paths in configuration files:

**In `shared/configs/model_config.yaml`:**
```yaml
# Old
model_path: models/yolo_v11.pt

# New
model_path: ../ml-pipeline/trained_models/yolo_v11.pt
```

**In `app/backend/api/main.py`:**
```python
# Old
from src.utils.logger import setup_logger

# New
import sys
sys.path.append('../../shared')
from utils.logger import setup_logger
```

### Step 8: Create New Environment Variables

Update `.env` files:

```bash
# ml-pipeline/.env
GOOGLE_SERVICE_ACCOUNT_EMAIL=...
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=...
MLFLOW_TRACKING_URI=http://localhost:5000

# app/backend/.env
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379
GOOGLE_GEMINI_API_KEY=...
GROQ_API_KEY=...

# app/frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 9: Test Each Component

```powershell
# Test ML Pipeline
cd ml-pipeline
python -m venv venv-ml
.\venv-ml\Scripts\Activate.ps1
pip install -r requirements-ml.txt
python -c "from models.detection.yolo_detector import YOLODetector; print('ML imports OK')"

# Test Backend
cd ..\app\backend
python -m venv venv-backend
.\venv-backend\Scripts\Activate.ps1
pip install -r requirements-backend.txt
uvicorn api.main:app --reload

# Test Frontend
cd ..\frontend
npm install
npm run dev
```

## 🔍 Import Path Mapping

Here's a reference for updating imports:

| Old Path | New Path (ML) | New Path (Backend) |
|----------|---------------|-------------------|
| `src.models.detection.*` | `models.detection.*` | N/A (load trained model) |
| `src.models.growth_forecasting.*` | `models.growth_forecasting.*` | N/A (load trained model) |
| `src.data.*` | `data_collection.*` | N/A |
| `src.services.gemini_flash_service` | N/A | `services.gemini_flash_service` |
| `src.agents.*` | N/A | `agents.*` |
| `src.api.*` | N/A | `api.*` |
| `src.utils.*` | `shared.utils.*` | `shared.utils.*` |
| `configs.*` | `shared.configs.*` | `shared.configs.*` |

## 📦 Dependency Management

### ML Pipeline Dependencies

**Keep:**
- torch, torchvision, tensorflow
- ultralytics, opencv-python
- earthengine-api, geemap, geopandas
- mlflow, dvc, wandb
- jupyter, matplotlib, seaborn

**Remove:**
- fastapi, uvicorn
- sqlalchemy, alembic
- langchain, langgraph
- authentication libraries

### Backend Dependencies

**Keep:**
- fastapi, uvicorn
- sqlalchemy, alembic, psycopg2
- langchain, langgraph, google-generativeai
- celery, redis
- authentication libraries

**Remove:**
- Full PyTorch/TensorFlow (use ONNX Runtime instead)
- Jupyter, matplotlib
- mlflow, dvc
- Heavy geospatial libs (keep only essentials)

## ⚠️ Common Issues & Solutions

### Issue 1: Import Errors

**Problem:**
```python
ModuleNotFoundError: No module named 'src.models'
```

**Solution:**
Update imports and ensure `shared/` is in Python path:

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
```

### Issue 2: Configuration Not Found

**Problem:**
```
FileNotFoundError: configs/model_config.yaml
```

**Solution:**
Update config paths:

```python
# Old
config_path = "configs/model_config.yaml"

# New
config_path = Path(__file__).parent.parent.parent / "shared" / "configs" / "model_config.yaml"
```

### Issue 3: Model Files Not Found

**Problem:**
```
FileNotFoundError: models/yolo_v11.pt
```

**Solution:**
Copy trained models to backend:

```powershell
Copy-Item "ml-pipeline\trained_models\*" "app\backend\models\"
```

Update model loading:

```python
# Old
model_path = "models/yolo_v11.pt"

# New
model_path = Path(__file__).parent / "models" / "yolo_v11.pt"
```

### Issue 4: Database Connection Issues

**Problem:**
Backend can't find database models.

**Solution:**
Update import in routers:

```python
# Old
from src.api.models.database import City

# New
from database.models import City
```

## ✅ Validation Checklist

After migration, verify:

- [ ] ML Pipeline runs independently
  - [ ] Data collection scripts work
  - [ ] Model training scripts work
  - [ ] Notebooks open without errors
  
- [ ] Backend runs independently
  - [ ] FastAPI starts without errors
  - [ ] API endpoints respond correctly
  - [ ] Database connections work
  - [ ] Model inference works
  
- [ ] Frontend runs independently
  - [ ] Next.js dev server starts
  - [ ] API calls to backend work
  - [ ] Map displays correctly
  
- [ ] Shared code accessible
  - [ ] Both ML and Backend can import from shared/
  - [ ] Configurations load correctly

## 🎯 Next Steps After Migration

1. **Update Documentation**: Update any references to old file paths
2. **Update CI/CD**: Modify build/deploy scripts for new structure
3. **Train Models**: Run ML pipeline to generate models
4. **Test Integration**: Ensure backend can load and use trained models
5. **Deploy**: Deploy backend and frontend separately

## 📞 Need Help?

If you encounter issues during migration:

1. Check the backup you created in Step 1
2. Review import paths carefully
3. Ensure virtual environments are activated
4. Check that all dependencies are installed
5. Refer to individual README files in each directory

## 🎉 Migration Complete!

Once everything works:

```powershell
# Clean up old structure (optional)
Remove-Item "src" -Recurse
Remove-Item "data" -Recurse
Remove-Item "notebooks" -Recurse
Remove-Item "configs" -Recurse

# Update .gitignore
# Add entries for new structure
```

Your project is now properly separated into ML Pipeline and Application! 🚀
