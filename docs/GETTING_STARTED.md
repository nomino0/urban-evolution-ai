# Getting Started with Urban Evolution AI

This guide will help you set up and run the Urban Evolution AI Platform on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/)
- **PostgreSQL 14+** (Production) - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Redis 7+** - [Download Redis](https://redis.io/download/) or use Docker

### Optional
- **CUDA Toolkit** (for GPU acceleration)  
- **Docker Desktop** (for containerized services)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/urban-evolution-ai.git
cd urban-evolution-ai
```

### 2. Set Up Python Environment

#### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get an execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Linux/Mac
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your API keys and configuration
# Required:
# - GEMINI_API_KEY
# - GROQ_API_KEY
# - DATABASE_URL
# - REDIS_URL
```

#### Getting API Keys

1. **Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add to `.env`: `GEMINI_API_KEY=your-key-here`

2. **Groq API Key**
   - Visit [Groq Console](https://console.groq.com/)
   - Create account and generate API key
   - Add to `.env`: `GROQ_API_KEY=your-key-here`

3. **Google Earth Engine** (for satellite data)
   - Visit [Earth Engine Signup](https://earthengine.google.com/signup/)
   - Create project and service account
   - Download credentials JSON
   - Add to `.env`: `GOOGLE_EE_PROJECT_ID=your-project-id`

4. **LangSmith** (optional, for agent tracing)
   - Visit [LangSmith](https://smith.langchain.com/)
   - Create API key
   - Add to `.env`: `LANGSMITH_API_KEY=your-key-here`

### 4. Set Up Database

#### Option A: SQLite (Development)
```bash
# Already configured in .env.example
# DATABASE_URL=sqlite:///./urban_evolution.db
```

#### Option B: PostgreSQL (Production)
```bash
# Install PostgreSQL
# Create database
psql -U postgres
CREATE DATABASE urban_evolution_ai;
CREATE USER urban_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE urban_evolution_ai TO urban_user;
\q

# Update .env
DATABASE_URL=postgresql://urban_user:your_password@localhost:5432/urban_evolution_ai
```

### 5. Initialize Database

```bash
# Create database tables (Alembic migrations)
# TODO: Run when Alembic is set up
# alembic upgrade head

# For now, tables will be created automatically
python -c "from src.api.models.database import Base; from sqlalchemy import create_engine; engine = create_engine('sqlite:///./urban_evolution.db'); Base.metadata.create_all(engine)"
```

### 6. Set Up Redis

#### Option A: Docker (Recommended)
```bash
# Pull and run Redis container
docker run -d -p 6379:6379 --name urban-redis redis:7-alpine

# Verify Redis is running
docker ps
```

#### Option B: Windows Installation
```powershell
# Download Redis for Windows from:
# https://github.com/microsoftarchive/redis/releases

# Or use WSL2:
wsl --install
wsl
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

### 7. Start the Backend

```bash
# Ensure virtual environment is activated
# Ensure Redis is running

# Start FastAPI server
uvicorn src.api.main:app --reload --port 8000

# Server will be available at:
# http://localhost:8000
# API docs: http://localhost:8000/docs
```

### 8. Start Celery Worker (Optional, for background tasks)

```bash
# Open a new terminal
# Activate virtual environment
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Start Celery worker
celery -A src.services.celery_tasks worker --loglevel=info --pool=solo
```

### 9. Set Up Frontend

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev

# Frontend will be available at:
# http://localhost:3000
```

## Verify Installation

### 1. Test Backend API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","timestamp":"2024-11-09T...","service":"urban-evolution-ai"}

# Test cities endpoint
curl http://localhost:8000/api/cities/

# View API documentation
# Open browser: http://localhost:8000/docs
```

### 2. Test Frontend

```bash
# Open browser
# Navigate to: http://localhost:3000

# You should see the Urban Evolution AI dashboard
```

### 3. Test Gemini Service

```python
# Create a test script: test_gemini.py
from src.services.gemini_flash_service import GeminiFlashService

async def test():
    service = GeminiFlashService()
    print("Gemini service initialized successfully!")
    print(service.get_cost_summary())

import asyncio
asyncio.run(test())

# Run: python test_gemini.py
```

## Common Issues and Solutions

### Issue: Module not found errors

```bash
# Ensure you're in the project root directory
# Ensure virtual environment is activated
# Try reinstalling dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Redis connection refused

```bash
# Check if Redis is running
docker ps  # If using Docker
# or
redis-cli ping  # Should return PONG

# Start Redis if not running
docker start urban-redis
```

### Issue: Database connection errors

```bash
# Check DATABASE_URL in .env
# Ensure PostgreSQL is running
# Test connection:
psql -U urban_user -d urban_evolution_ai -h localhost
```

### Issue: API key errors

```bash
# Verify all required API keys are in .env
# Check for typos in key names
# Ensure keys are valid (test in respective consoles)
```

### Issue: Port already in use

```bash
# Check what's using the port
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Kill the process or use a different port
uvicorn src.api.main:app --reload --port 8001
```

## Next Steps

Once your setup is complete:

1. **Explore the API** - Visit http://localhost:8000/docs
2. **Read the Documentation** - Check the `docs/` folder
3. **Run Example Notebooks** - Open Jupyter notebooks in `notebooks/`
4. **Download Sample Data** - Follow data collection guides
5. **Train Models** - See model training documentation

## Development Workflow

```bash
# 1. Create a feature branch
git checkout -b feature/your-feature-name

# 2. Make changes to code

# 3. Format code
black src/
isort src/

# 4. Run tests
pytest

# 5. Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature-name

# 6. Create pull request
```

## Useful Commands

```bash
# Format code
black src/ tests/
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/
pylint src/

# Run tests
pytest
pytest --cov=src  # With coverage
pytest -m unit  # Only unit tests
pytest -v  # Verbose output

# Database migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head
alembic downgrade -1

# Clear cache
rm -rf __pycache__
rm -rf .pytest_cache
rm -rf .mypy_cache

# Rebuild dependencies
pip freeze > requirements.txt
```

## Getting Help

- **Documentation**: See `docs/` folder
- **Issues**: https://github.com/yourusername/urban-evolution-ai/issues
- **Discussions**: https://github.com/yourusername/urban-evolution-ai/discussions
- **Email**: your.email@example.com

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [YOLOv11 Documentation](https://docs.ultralytics.com/)

---

**Happy Coding! 🚀**
