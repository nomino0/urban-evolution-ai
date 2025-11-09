# 🏗️ Urban Evolution AI - Project Architecture

## 📂 Project Structure Overview

This project is organized into **three main sections** to promote modularity, maintainability, and clear separation of concerns:

```
urban-evolution-ai/
├── 📊 ml-pipeline/          # Machine Learning & Data Science
├── 🚀 app/                  # Production Application (Frontend + Backend)
├── 🔧 shared/               # Shared utilities and configurations
└── 📄 Project Root Files    # Configuration, docs, deployment
```

---

## 🎯 Design Philosophy

### Separation of Concerns

1. **ML Pipeline** (`ml-pipeline/`)
   - Focused on data science, model development, and training
   - Used by data scientists and ML engineers
   - Heavy dependencies (PyTorch, TensorFlow, geospatial libraries)
   - Can be run independently for research and experimentation

2. **Application** (`app/`)
   - Production-ready frontend and backend
   - Lighter dependencies (only inference-related)
   - Consumes trained models from ML pipeline
   - Optimized for deployment and scaling

3. **Shared** (`shared/`)
   - Common utilities used by both ML and App
   - Configurations, constants, helper functions
   - Single source of truth for shared logic

---

## 📊 ML Pipeline (`ml-pipeline/`)

**Purpose**: Research, data processing, model training, and experimentation

```
ml-pipeline/
├── data_collection/               # Satellite & geospatial data download
│   ├── download_sentinel.py      # Google Earth Engine integration
│   ├── download_osm.py            # OpenStreetMap extraction
│   ├── download_topographic.py   # Elevation data
│   ├── define_city_boundaries.py # City boundary definitions
│   ├── create_tile_grids.py      # Tile manifest generation
│   └── aligned_download.py       # Coordinated download system
│
├── models/                        # Model implementations
│   ├── detection/
│   │   ├── yolo_detector.py      # YOLOv11 building detection
│   │   ├── sam_segmentation.py   # SAM-Geo segmentation
│   │   └── shadow_detection.py   # Shadow-based height estimation
│   └── growth_forecasting/
│       ├── lstm_spatial_growth.py # LSTM growth prediction
│       ├── xgboost_classifier.py  # Building classification
│       └── prophet_population.py  # Population forecasting
│
├── training/                      # Training scripts
│   ├── train_yolo.py
│   ├── train_lstm.py
│   ├── train_xgboost.py
│   ├── evaluate_models.py
│   └── hyperparameter_tuning.py
│
├── notebooks/                     # Jupyter notebooks for exploration
│   ├── 01_data_exploration.ipynb
│   ├── 02_yolo_training.ipynb
│   ├── 03_growth_analysis.ipynb
│   └── 04_policy_scenarios.ipynb
│
├── experiments/                   # MLflow experiments
│   └── mlruns/                   # Experiment tracking
│
├── datasets/                      # Training data
│   ├── raw/                      # Raw downloaded data
│   │   ├── sentinel/
│   │   ├── osm/
│   │   └── topographic/
│   └── processed/                # Preprocessed data
│       ├── train/
│       ├── val/
│       └── test/
│
├── trained_models/                # Exported trained models
│   ├── yolo_v11_buildings.pt
│   ├── lstm_growth.h5
│   ├── xgboost_classifier.pkl
│   └── model_metadata.json
│
├── requirements-ml.txt            # ML-specific dependencies
└── README.md                      # ML pipeline documentation
```

**Key Responsibilities**:
- ✅ Download and preprocess satellite imagery
- ✅ Extract OSM building footprints and features
- ✅ Train computer vision models (YOLO, SAM)
- ✅ Train time-series forecasting models (LSTM, Prophet)
- ✅ Experiment tracking with MLflow
- ✅ Export trained models for production use
- ✅ Data quality validation and alignment

**Run ML Pipeline**:
```bash
# Activate ML environment
cd ml-pipeline
python -m venv venv-ml
.\venv-ml\Scripts\Activate.ps1
pip install -r requirements-ml.txt

# Download data for a city
python data_collection/define_city_boundaries.py --city Tunis
python data_collection/aligned_download.py --city Tunis

# Train models
python training/train_yolo.py --config ../shared/configs/model_config.yaml
python training/train_lstm.py --epochs 100

# Export models
python training/export_models.py --output trained_models/
```

---

## 🚀 Application (`app/`)

**Purpose**: Production application serving end users

```
app/
├── backend/                       # FastAPI Backend
│   ├── api/
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── routers/              # API endpoints
│   │   │   ├── cities.py
│   │   │   ├── buildings.py
│   │   │   ├── growth.py
│   │   │   ├── scenarios.py
│   │   │   ├── chat.py
│   │   │   ├── news.py
│   │   │   └── ethics.py
│   │   ├── models/               # Database models
│   │   │   ├── database.py       # SQLAlchemy ORM
│   │   │   └── schemas.py        # Pydantic models
│   │   ├── middleware/
│   │   │   ├── auth.py           # JWT authentication
│   │   │   ├── cors.py           # CORS configuration
│   │   │   └── rate_limit.py     # Rate limiting
│   │   └── dependencies.py       # FastAPI dependencies
│   │
│   ├── services/                  # Business logic
│   │   ├── gemini_flash_service.py    # Image generation
│   │   ├── model_inference_service.py # ML model inference
│   │   ├── news_service.py            # News aggregation
│   │   ├── growth_service.py          # Growth predictions
│   │   └── scenario_service.py        # Scenario generation
│   │
│   ├── agents/                    # Multi-agent system
│   │   ├── orchestrator.py        # LangGraph orchestrator
│   │   ├── base_agent.py          # Base agent class
│   │   ├── news_analyzer.py       # News analysis agent
│   │   ├── growth_predictor.py    # Growth prediction agent
│   │   ├── policy_analyzer.py     # Policy analysis agent
│   │   ├── scenario_generator.py  # Scenario generation agent
│   │   ├── ethics_guardian.py     # Ethics checking agent
│   │   └── tools/                 # Agent tools
│   │       ├── geocoding.py
│   │       ├── news_scraper.py
│   │       └── osm_queries.py
│   │
│   ├── database/
│   │   ├── connection.py          # Database connection
│   │   ├── migrations/            # Alembic migrations
│   │   └── seed.py                # Database seeding
│   │
│   ├── tasks/                     # Celery background tasks
│   │   ├── data_update.py
│   │   ├── model_inference.py
│   │   └── report_generation.py
│   │
│   ├── requirements-backend.txt   # Backend dependencies
│   └── README.md
│
└── frontend/                      # Next.js Frontend
    ├── src/
    │   ├── app/                   # Next.js 14 App Router
    │   │   ├── page.tsx           # Home page
    │   │   ├── dashboard/
    │   │   ├── scenarios/
    │   │   └── chat/
    │   ├── components/            # React components
    │   │   ├── ui/                # shadcn/ui components
    │   │   ├── map/
    │   │   │   ├── InteractiveMap.tsx
    │   │   │   ├── BuildingLayer.tsx
    │   │   │   └── HeatmapLayer.tsx
    │   │   ├── timeline/
    │   │   │   └── TimeSlider.tsx
    │   │   ├── scenario/
    │   │   │   └── ScenarioBuilder.tsx
    │   │   ├── chat/
    │   │   │   └── AgentChat.tsx
    │   │   └── analytics/
    │   │       └── GrowthCharts.tsx
    │   ├── lib/                   # Utilities
    │   │   ├── api-client.ts      # API calls
    │   │   ├── utils.ts           # Helper functions
    │   │   └── constants.ts
    │   └── styles/
    │       └── globals.css
    │
    ├── public/                    # Static assets
    ├── package.json
    ├── tsconfig.json
    ├── next.config.js
    ├── tailwind.config.js
    └── README.md
```

**Key Responsibilities**:
- ✅ Serve REST API for frontend
- ✅ Load and run trained ML models for inference
- ✅ Manage user sessions and authentication
- ✅ Handle database operations (CRUD)
- ✅ Generate scenarios with Gemini API
- ✅ Multi-agent orchestration with LangGraph
- ✅ Real-time updates with WebSockets
- ✅ Background task processing with Celery
- ✅ Interactive web dashboard

**Run Application**:
```bash
# Backend
cd app/backend
python -m venv venv-backend
.\venv-backend\Scripts\Activate.ps1
pip install -r requirements-backend.txt
uvicorn api.main:app --reload --port 8000

# Frontend
cd app/frontend
npm install
npm run dev
```

---

## 🔧 Shared (`shared/`)

**Purpose**: Common code and configurations used by both ML and App

```
shared/
├── configs/                       # Configuration files
│   ├── model_config.yaml         # ML model hyperparameters
│   ├── agent_config.yaml         # Agent system settings
│   ├── policy_profiles.yaml      # Urban policy definitions
│   └── app_config.yaml           # Application settings
│
├── utils/                         # Shared utilities
│   ├── logger.py                 # Logging utility
│   ├── geometry.py               # Geospatial utilities
│   ├── validators.py             # Data validation
│   └── constants.py              # Shared constants
│
└── schemas/                       # Shared data schemas
    ├── city.py
    ├── building.py
    └── prediction.py
```

**Key Responsibilities**:
- ✅ Centralized configuration management
- ✅ Shared utility functions
- ✅ Common data validation schemas
- ✅ Constants and enumerations

---

## 🔄 Workflow: ML Pipeline → Application

### Step 1: Data Collection (ML Pipeline)
```bash
cd ml-pipeline
python data_collection/aligned_download.py --city Tunis
```
- Downloads Sentinel-2, OSM, topographic data
- Ensures spatial alignment
- Stores in `ml-pipeline/datasets/raw/`

### Step 2: Model Training (ML Pipeline)
```bash
python training/train_yolo.py
python training/train_lstm.py
```
- Trains models on collected data
- Tracks experiments in MLflow
- Exports trained models to `ml-pipeline/trained_models/`

### Step 3: Model Export (ML Pipeline → Shared)
```bash
python training/export_models.py --output ../app/backend/models/
```
- Exports optimized models for inference
- Includes model metadata (version, metrics)
- Backend loads these models at startup

### Step 4: Application Inference (App)
```python
# In app/backend/services/model_inference_service.py
from shared.configs import model_config

class ModelInferenceService:
    def __init__(self):
        self.yolo_model = load_model("models/yolo_v11_buildings.pt")
        self.lstm_model = load_model("models/lstm_growth.h5")
    
    async def predict_growth(self, city_id: str, target_year: int):
        # Use trained models for inference
        ...
```

### Step 5: Frontend Display (App)
```typescript
// In app/frontend/src/components/map/HeatmapLayer.tsx
const growthData = await apiClient.predictGrowth(cityId, 2030);
// Display heatmap on map
```

---

## 📦 Dependencies Management

### ML Pipeline Dependencies (`ml-pipeline/requirements-ml.txt`)
Heavy ML/data science libraries:
- PyTorch, TensorFlow
- Ultralytics (YOLO), Segment Anything
- Google Earth Engine API
- GeoPandas, Rasterio
- MLflow, DVC
- Jupyter, Matplotlib, Seaborn

### Backend Dependencies (`app/backend/requirements-backend.txt`)
Lighter inference and API libraries:
- FastAPI, Uvicorn
- SQLAlchemy, Alembic
- LangChain, LangGraph
- google-generativeai
- Celery, Redis
- Inference-only ML libraries (ONNX Runtime, TensorFlow Lite)

### Frontend Dependencies (`app/frontend/package.json`)
- Next.js 14, React, TypeScript
- React Leaflet (maps)
- Recharts (visualization)
- Tailwind CSS, shadcn/ui
- SWR (data fetching)

---

## 🚀 Deployment Strategy

### Development
```bash
# Run ML pipeline locally
cd ml-pipeline && python training/train_yolo.py

# Run backend locally
cd app/backend && uvicorn api.main:app --reload

# Run frontend locally
cd app/frontend && npm run dev
```

### Production

**ML Pipeline** (Run periodically or on-demand):
- Runs on GPU servers (Modal, AWS EC2 with GPU)
- Triggered manually or by CI/CD for retraining
- Outputs models to cloud storage (S3, GCS)

**Backend API**:
- Deploy to Railway, Render, or AWS
- Uses lightweight inference models
- Connects to PostgreSQL database
- Redis for caching and task queue

**Frontend**:
- Deploy to Vercel or Netlify
- Static site generation (SSG) for performance
- Connects to backend API

---

## 🧪 Testing Strategy

### ML Pipeline Tests
```bash
cd ml-pipeline
pytest tests/test_data_collection.py
pytest tests/test_model_training.py
```

### Backend Tests
```bash
cd app/backend
pytest tests/test_api.py
pytest tests/test_services.py
pytest tests/test_agents.py
```

### Frontend Tests
```bash
cd app/frontend
npm run test
npm run test:e2e
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     ML PIPELINE                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [Satellite Data] → [Data Collection] → [Preprocessing]      │
│         ↓                                                     │
│  [Training Data] → [Model Training] → [Trained Models]       │
│         ↓                                                     │
│  [MLflow] ← [Experiments] ← [Hyperparameter Tuning]         │
│                                                               │
└──────────────────────┬──────────────────────────────────────┘
                       │ Export Models
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  [Backend API] ← [Load Models] ← [Trained Models]           │
│       ↓                                                       │
│  [Inference Service] → [Growth Predictions]                  │
│       ↓                                                       │
│  [Multi-Agent System] → [Scenario Generation]                │
│       ↓                                                       │
│  [REST API] ← [Frontend] ← [User]                           │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Benefits of This Architecture

### 1. **Modularity**
- ML and App teams can work independently
- Clear interfaces between components
- Easy to add new models or features

### 2. **Scalability**
- ML pipeline can run on powerful GPU servers
- App backend can scale horizontally
- Frontend can use CDN for global distribution

### 3. **Maintainability**
- Separate dependencies reduce conflicts
- Clear separation of concerns
- Easier to debug and test

### 4. **Cost Efficiency**
- ML pipeline runs only when needed (periodic retraining)
- App uses lightweight inference (cheaper servers)
- Frontend is static (minimal hosting costs)

### 5. **Development Velocity**
- Data scientists focus on models
- Backend engineers focus on API and business logic
- Frontend developers focus on UX
- No stepping on each other's toes!

---

## 📚 Next Steps

1. **Complete ML Pipeline**:
   - Implement data collection scripts
   - Train initial models
   - Export models for app

2. **Complete Backend**:
   - Implement API endpoints
   - Integrate trained models
   - Set up multi-agent system

3. **Complete Frontend**:
   - Build Next.js components
   - Connect to backend API
   - Design interactive dashboard

4. **Deploy**:
   - Set up CI/CD pipelines
   - Deploy to production
   - Monitor and optimize

---

**Happy Building! 🚀**
