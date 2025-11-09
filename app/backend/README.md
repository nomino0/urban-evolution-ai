# 🚀 Urban Evolution AI - Backend

FastAPI backend for the Urban Evolution AI Platform.

## 🎯 Purpose

Production-ready API serving the frontend application with:
- RESTful endpoints for city data, predictions, scenarios
- Multi-agent AI system for intelligent analysis
- ML model inference (using trained models from ml-pipeline)
- Database management (PostgreSQL)
- Background task processing (Celery)
- Real-time updates (WebSockets)

## 📁 Structure

```
backend/
├── api/                    # FastAPI application
│   ├── main.py            # App entry point
│   ├── routers/           # API endpoints
│   ├── models/            # Database models (SQLAlchemy)
│   ├── middleware/        # Auth, CORS, rate limiting
│   └── dependencies.py    # Shared dependencies
├── services/              # Business logic
├── agents/                # Multi-agent AI system
├── database/              # DB connection & migrations
├── tasks/                 # Celery background tasks
└── models/                # Trained ML models (from ml-pipeline)
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd app/backend

# Create virtual environment
python -m venv venv-backend

# Activate (Windows)
.\venv-backend\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv-backend/bin/activate

# Install dependencies
pip install -r requirements-backend.txt
```

### 2. Configure Environment Variables

Create `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/urban_evolution
DEV_DATABASE_URL=sqlite:///./urban_evolution.db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
GOOGLE_GEMINI_API_KEY=your-gemini-key
GROQ_API_KEY=your-groq-key
LANGSMITH_API_KEY=your-langsmith-key

# Google Earth Engine
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-service-account@project.iam.gserviceaccount.com
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=path/to/key.json

# Environment
ENVIRONMENT=development
DEBUG=True
```

### 3. Setup Database

```bash
# Create database (PostgreSQL)
createdb urban_evolution

# Or use SQLite for development (no setup needed)

# Run migrations
alembic upgrade head

# Seed database (optional)
python database/seed.py
```

### 4. Copy Trained Models

```bash
# Copy trained models from ml-pipeline
cp ../../ml-pipeline/trained_models/*.pt models/
cp ../../ml-pipeline/trained_models/*.h5 models/
cp ../../ml-pipeline/trained_models/*.pkl models/
```

### 5. Start Backend

```bash
# Development mode (with auto-reload)
uvicorn api.main:app --reload --port 8000

# Production mode
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn (production)
gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 6. Start Background Workers (Optional)

```bash
# Start Celery worker
celery -A tasks.celery_app worker --loglevel=info

# Start Celery beat (for periodic tasks)
celery -A tasks.celery_app beat --loglevel=info

# Monitor with Flower
celery -A tasks.celery_app flower --port=5555
```

## 📡 API Documentation

Once the server is running:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔌 API Endpoints

### Cities

```http
GET    /api/cities                    # List all cities
GET    /api/cities/{city_id}          # Get city details
POST   /api/cities                    # Create new city
PUT    /api/cities/{city_id}          # Update city
DELETE /api/cities/{city_id}          # Delete city
```

### Buildings

```http
GET    /api/buildings                 # List buildings (with filters)
GET    /api/buildings/{building_id}   # Get building details
POST   /api/buildings/detect          # Run building detection
```

### Growth Predictions

```http
POST   /api/growth/predict            # Predict urban growth
GET    /api/growth/{prediction_id}    # Get prediction results
GET    /api/growth/city/{city_id}     # Get predictions for city
```

### Scenarios

```http
POST   /api/scenarios/generate        # Generate scenario image
GET    /api/scenarios/{scenario_id}   # Get scenario details
GET    /api/scenarios/city/{city_id}  # List scenarios for city
```

### Multi-Agent Chat

```http
POST   /api/chat                      # Send message to agents
GET    /api/chat/history              # Get chat history
WS     /api/chat/stream               # WebSocket for real-time chat
```

### News

```http
GET    /api/news/city/{city_id}       # Get urban news for city
POST   /api/news/analyze              # Analyze news sentiment
```

### Ethics

```http
POST   /api/ethics/check              # Check scenario for ethical concerns
GET    /api/ethics/guidelines         # Get ethical guidelines
```

## 🤖 Multi-Agent System

The backend uses LangGraph for multi-agent orchestration:

```python
from agents.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()

# Run agent workflow
result = await orchestrator.run(
    query="What will Tunis look like in 2030?",
    city_id="123e4567-e89b-12d3-a456-426614174000"
)
```

### Available Agents

1. **NewsAnalyzer**: Scrapes and analyzes urban development news
2. **GrowthPredictor**: Predicts urban growth using LSTM models
3. **PolicyAnalyzer**: Analyzes urban policies and regulations
4. **ScenarioGenerator**: Generates future scenarios with Gemini
5. **EthicsGuardian**: Checks for ethical concerns and biases

## 🔧 Services

### Model Inference Service

```python
from services.model_inference_service import ModelInferenceService

service = ModelInferenceService()

# Detect buildings
buildings = await service.detect_buildings(
    image_path="data/tunis_satellite.tif",
    confidence=0.5
)

# Predict growth
growth = await service.predict_growth(
    city_id="123e4567",
    target_year=2030
)
```

### Gemini Flash Service

```python
from services.gemini_flash_service import GeminiFlashService

service = GeminiFlashService()

# Generate scenario
result = await service.edit_image(
    source_image_path="outputs/tunis_2024.png",
    prompt="Transform to green city with 40% green space",
    edit_regions=[[100, 100, 500, 500]],
    reference_image_path="outputs/copenhagen_2024.png"
)
```

## 🗄️ Database

### Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Models

- **City**: City information and boundaries
- **Tile**: Satellite tile data
- **Building**: Detected buildings
- **GrowthPrediction**: Growth forecasts
- **Scenario**: Generated scenarios
- **NewsCache**: Cached news articles
- **User**: User authentication (if needed)

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_get_city
```

## 📊 Monitoring

### Prometheus Metrics

Metrics exposed at `/metrics`:

```
# Request count
http_requests_total{method="GET",endpoint="/api/cities"}

# Request duration
http_request_duration_seconds{method="GET",endpoint="/api/cities"}

# Active connections
active_connections

# Model inference time
model_inference_duration_seconds{model="yolo"}
```

### Logging

Logs are written to:
- Console: Structured JSON logs
- File: `logs/app.log` (rotated daily)
- Sentry: Production error tracking

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Test connection
python -c "from sqlalchemy import create_engine; engine = create_engine('postgresql://user:pass@localhost/urban_evolution'); engine.connect(); print('Success!')"
```

### Redis Connection Issues

```bash
# Check Redis is running
redis-cli ping

# Should return: PONG
```

### Model Loading Issues

```bash
# Verify models exist
ls models/

# Test model loading
python -c "from services.model_inference_service import ModelInferenceService; service = ModelInferenceService(); print('Models loaded!')"
```

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t urban-evolution-backend .

# Run container
docker run -p 8000:8000 --env-file .env urban-evolution-backend
```

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### AWS/GCP

See `../../deployment/README.md` for cloud deployment guides.

## 📚 Additional Documentation

- **API Reference**: See `/docs` endpoint
- **Agent System**: See `agents/README.md`
- **Services**: See `services/README.md`
- **Database Schema**: See `database/README.md`

## 🎯 Next Steps

1. **Database Setup**: Configure PostgreSQL
2. **Copy Models**: Copy trained models from ml-pipeline
3. **Start Server**: Run uvicorn
4. **Test Endpoints**: Visit `/docs` and try API
5. **Start Workers**: Run Celery for background tasks

Happy Coding! 🚀
