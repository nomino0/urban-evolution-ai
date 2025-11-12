# 🌆 Urban Evolution AI Platform

**AI-Powered Urban Evolution Platform with Predictive Growth & City Reimagination**

*Helping decision-makers make the right moves, at the right scale, and try all the different scenarios.*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 🎯 Overview

An AI-powered decision support platform that combines satellite change detection, time-series forecasting, multi-agent AI, and generative image editing to predict urban growth and enable scenario planning. This platform empowers urban planners, policymakers, and stakeholders to visualize and evaluate different development scenarios before implementation, reducing risk and maximizing positive impact.

### 🌟 Inspiration

This project builds upon groundbreaking research in satellite-based urban change detection, particularly inspired by the work of **[Rodrigo Caye Daudt](https://rcdaudt.github.io/)** (Senior Computer Vision Research Engineer at Sony) and his pioneering work on the **Onera Satellite Change Detection (OSCD) Dataset**.

**Key Reference:**
> Daudt, R.C., Le Saux, B., Boulch, A. and Gousseau, Y., 2018. "Urban Change Detection for Multispectral Earth Observation Using Convolutional Neural Networks." *IEEE International Geoscience and Remote Sensing Symposium (IGARSS)*. 
> 
> [[Paper]](https://rcdaudt.github.io/files/2018igarss-change-detection.pdf) [[Dataset]](https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection) [[GitHub]](https://github.com/rcdaudt/fully_convolutional_change_detection)

The OSCD dataset provides 24 pairs of multispectral Sentinel-2 images (2015-2018) from locations worldwide, with pixel-level urban change annotations. This methodology forms the foundation of our building detection and change tracking system.

---

## 🆕 NEW SEPARATED ARCHITECTURE!

This project has been **reorganized into three modular sections** for better development:

```
📊 ml-pipeline/    ← Data Science & Model Training
🚀 app/           ← Production App (Backend + Frontend)  
🔧 shared/        ← Common Code & Configs
```

### 📖 Essential Documentation

| Document | Description |
|----------|-------------|
| **[Getting Started Guide](docs/GETTING_STARTED.md)** ⭐ | **START HERE** - Quick start and setup |
| **[Architecture Guide](docs/ARCHITECTURE.md)** 🏗️ | Detailed architecture and design |
| **[Quick Reference](docs/QUICK_REFERENCE.md)** 📄 | One-page command cheat sheet |
| **[Project Structure](docs/NEW_STRUCTURE_SUMMARY.md)** 📊 | Three-tier architecture overview |
| **[Migration Guide](docs/MIGRATION_GUIDE.md)** 🔄 | Migrating from old structure |

### 🚀 Quick Setup

```powershell
# ML Pipeline
cd ml-pipeline && python -m venv venv-ml
.\venv-ml\Scripts\Activate.ps1 && pip install -r requirements-ml.txt

# Backend
cd app\backend && python -m venv venv-backend
.\venv-backend\Scripts\Activate.ps1 && pip install -r requirements-backend.txt
uvicorn api.main:app --reload  # → http://localhost:8000/docs

# Frontend
cd app\frontend && npm install && npm run dev  # → http://localhost:3000
```

---

## 🎯 What This Platform Does

The system uses:

- **YOLOv11** for building detection and classification
- **LSTM** models for spatial urban growth prediction  
- **Multi-agent systems** (LangGraph) for intelligent scenario generation
- **Google Gemini 2.5 Flash** for pixel-precise image editing
- **Real-time news analysis** for announced project integration

## ✨ Key Features

### � Decision Support for Urban Planning

**Make informed decisions by exploring multiple scenarios:**
- Visualize the impact of different policy choices before implementation
- Compare growth trajectories under various development strategies
- Assess environmental, social, and economic trade-offs
- Test infrastructure investments at different scales
- Identify optimal timing for interventions

### 1. 🛰️ Satellite-Based Change Detection

Built on proven methodologies from the OSCD dataset:
- Multi-spectral Sentinel-2 imagery analysis (10m-60m resolution)
- Pixel-level urban change detection using Fully Convolutional Networks
- Building footprint extraction and classification
- Historical change tracking (2015-2024)
- Automated annotation of new constructions and urban expansion

### 2. 🏗️ Building Detection & Urban Analytics

- YOLOv11-based building detection from satellite imagery
- Height estimation via shadow analysis and geometric modeling
- Building type classification (residential/commercial/industrial/government)
- Population capacity estimation and density mapping
- Infrastructure gap analysis

### 3. 📈 Predictive Urban Growth Modeling

- LSTM-based spatial expansion forecasting
- Integration with real-time urban planning news
- Historical pattern analysis and trend identification
- Confidence intervals and probability heatmaps
- Multi-year projection capabilities (2025-2040)

### 4. 🎭 Scenario Planning & Simulation

**Try different scenarios before committing resources:**
- **Policy Simulations**: Test EU Green Cities, Singapore Smart City, Copenhagen sustainability models
- **Scale Variations**: Compare small-scale interventions vs. city-wide transformations
- **Timeline Analysis**: Evaluate short-term (5yr), medium-term (10yr), long-term (20yr) impacts
- **Stakeholder Perspectives**: View scenarios from environmental, economic, and social lenses
- **Risk Assessment**: Identify potential challenges and mitigation strategies

### 5. 🤖 Multi-Agent AI System

Intelligent agents working together to generate insights:
- **DataCollector**: Gathers satellite imagery and urban data
- **ChangeDetector**: Identifies urban transformations using CNN models
- **GrowthPredictor**: Forecasts expansion zones with confidence metrics
- **NewsAnalyzer**: Extracts planned projects from news sources
- **PolicyAnalyzer**: Applies regulatory and policy constraints
- **ScenarioGenerator**: Creates detailed development scenarios
- **ImageEditor**: Generates photorealistic visualizations via Gemini 2.5 Flash
- **EthicsGuardian**: Validates fairness, bias, and environmental impact

### 6. 🎨 Pixel-Precise Visualization

- Region-specific image editing (not full-image generation)
- Geographic accuracy preservation
- Style blending from multiple reference cities
- Photorealistic future scenario renderings
- Before/after comparison views

### 7. 📊 Interactive Decision Dashboard

- Interactive maps with detected buildings and projected changes
- Timeline slider (historical 2015 → present 2024 → future 2030-2040)
- Scenario builder with customizable parameters
- Side-by-side scenario comparison
- Multi-agent chat interface for natural language queries
- Downloadable reports and data exports

## 🏗️ Architecture

```
Satellite Imagery → Building Detection (YOLO) → Classification (XGBoost)
                                ↓
                         Growth Prediction (LSTM)
                                ↓
    News Analysis → Multi-Agent Orchestrator → Gemini 2.5 Flash
                                ↓
                    Interactive Web Dashboard
```

## 📋 Tech Stack

- **Backend**: FastAPI, Python 3.10+, PostgreSQL, Redis, Celery
- **ML/CV**: PyTorch, YOLOv11, SAM-Geo, TensorFlow, XGBoost
- **Geospatial**: Google Earth Engine, OSMnx, GeoPandas, Rasterio
- **AI Agents**: LangChain, LangGraph, Groq API (Llama 3.1 70B)
- **Image Gen**: Google Gemini 2.5 Flash (NanoBanana)
- **Frontend**: Next.js 14, TypeScript, React Leaflet, shadcn/ui
- **MLOps**: MLflow, DVC, Prometheus, Grafana

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- PostgreSQL 14+
- Redis 7+
- CUDA (optional, for GPU acceleration)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/urban-evolution-ai.git
cd urban-evolution-ai
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
# - GOOGLE_EE_PROJECT_ID
# - GEMINI_API_KEY
# - GROQ_API_KEY
# - DATABASE_URL
```

### 4. Initialize Database

```bash
# Run migrations
alembic upgrade head

# Seed initial data (optional)
python scripts/seed_database.py
```

### 5. Start Backend Services

```bash
# Start Redis (Windows with Docker)
docker run -d -p 6379:6379 redis:7-alpine

# Start FastAPI server
uvicorn src.api.main:app --reload --port 8000

# Start Celery worker (new terminal)
celery -A src.services.celery_tasks worker --loglevel=info
```

### 6. Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Visit `http://localhost:3000` for the dashboard and `http://localhost:8000/docs` for API documentation.

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api_documentation.md)
- [Multi-Agent System Design](docs/agent_design.md)
- [Growth Modeling Methodology](docs/growth_modeling.md)
- [Policy Profiles](docs/policy_profiles.md)
- [Gemini Integration Guide](docs/gemini_integration.md)
- [Ethics Framework](docs/ethics_framework.md)
- [Deployment Guide](docs/deployment.md)

## 🗂️ Project Structure

```
urban-evolution-ai/
├── configs/              # YAML configuration files
├── data/                 # Data manifests and storage
├── src/
│   ├── agents/          # Multi-agent system (LangGraph)
│   ├── data/            # Data collection and processing
│   ├── models/          # ML models (YOLO, LSTM, XGBoost)
│   ├── services/        # External API services
│   ├── api/             # FastAPI backend
│   ├── monitoring/      # Observability and ethics
│   └── utils/           # Shared utilities
├── frontend/            # Next.js dashboard
├── models/              # Trained model weights
├── notebooks/           # Jupyter notebooks
├── tests/               # Unit and integration tests
├── docs/                # Documentation
└── deployment/          # Docker, Railway, Modal configs
```

## 🎓 Example Use Cases

### 1. Predict Urban Growth for Tunis

```bash
curl -X POST http://localhost:8000/api/growth/predict \
  -H "Content-Type: application/json" \
  -d '{"city_name": "Tunis", "target_year": 2030}'
```

### 2. Generate EU Green Cities Scenario

```bash
curl -X POST http://localhost:8000/api/scenarios/generate \
  -H "Content-Type: application/json" \
  -d '{
    "source_city": "Tunis",
    "target_policy": "EU_GREEN_CITIES",
    "user_preferences": {"prioritize_green_space": true}
  }'
```

### 3. Chat with Multi-Agent System

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What would Tunis look like in 2030 with Copenhagen green policies?",
    "city_context": "Tunis"
  }'
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
pytest -m ethics
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## ⚖️ Ethics & Responsible AI

This project is committed to responsible AI development. See [ETHICS.md](ETHICS.md) for our ethical guidelines, including:

- Bias detection and mitigation
- Transparency in AI decision-making
- Human oversight requirements
- Environmental impact considerations
- Community engagement principles

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### Research Foundations

**Special thanks to [Rodrigo Caye Daudt](https://rcdaudt.github.io/)** (Sony Research, Zürich) for pioneering work in satellite-based urban change detection that inspired this platform.

**Onera Satellite Change Detection (OSCD) Dataset:**
- Daudt, R.C., Le Saux, B., Boulch, A., and Gousseau, Y. (2018)
- 24 pairs of Sentinel-2 multispectral images with pixel-level urban change annotations
- Locations worldwide: Brazil, USA, Europe, Middle-East, Asia
- Dataset: [IEEE DataPort](https://ieee-dataport.org/open-access/oscd-onera-satellite-change-detection)
- Code: [GitHub Repository](https://github.com/rcdaudt/fully_convolutional_change_detection)

### Technology & Data Providers

- **Google Earth Engine** for Sentinel-2 satellite imagery access
- **OpenStreetMap** contributors for vector data
- **European Space Agency (ESA)** for Copernicus Sentinel missions
- **Ultralytics** for YOLOv11 architecture
- **Meta AI** for Segment Anything Model (SAM)
- **Google DeepMind** for Gemini 2.5 Flash API
- **LangChain** team for agent orchestration framework
- **Groq** for high-speed LLM inference

### Academic References

If you use this platform or methodology in your research, please cite:

```bibtex
@inproceedings{daudt2018urban,
  author = {Daudt, Rodrigo Caye and Le Saux, Bertrand and Boulch, Alexandre and Gousseau, Yann},
  title = {Urban Change Detection for Multispectral Earth Observation Using Convolutional Neural Networks},
  booktitle = {IEEE International Geoscience and Remote Sensing Symposium (IGARSS)},
  year = {2018},
  pages = {2115--2118},
  address = {Valencia, Spain}
}
```

## 📧 Contact

### Project Team

**Amine Mayoufi** ([@nomino0](https://github.com/nomino0))
- Email: aminemayoufi@ieee.org
- Role: Data Scientist

**Walaa Hidaya** ([@WalaaHidaya](https://github.com/WalaaHidaya))
- Email: walaahidaya0@gmail.com
- Role: Data Scientist

---

**⭐ If you find this project useful, please consider giving it a star!**
