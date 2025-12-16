# 🚀 Urban Evolution AI - Quick Reference Card

## 📂 New Project Structure

```
urban-evolution-ai/
├── 📊 ml-pipeline/              ← Data Science & ML Training
├── 🚀 app/                      ← Production Application
│   ├── backend/                 ← FastAPI API
│   └── frontend/                ← Next.js UI
└── 🔧 shared/                   ← Common configs & utils
```

## 🎯 One-Line Summary

**ML Pipeline**: Train models → **Backend**: Serve API → **Frontend**: Show UI

## 🚀 Quick Start Commands

### Setup (One-time)

```powershell
# ML Pipeline
cd ml-pipeline
python -m venv venv-ml
.\venv-ml\Scripts\Activate.ps1
pip install -r requirements-ml.txt

# Backend
cd ..\app\backend
python -m venv venv-backend
.\venv-backend\Scripts\Activate.ps1
pip install -r requirements-backend.txt

# Frontend
cd ..\frontend
npm install
```

### Daily Development

```powershell
# Terminal 1: Backend
cd app\backend
.\venv-backend\Scripts\Activate.ps1
uvicorn api.main:app --reload
# → http://localhost:8000/docs

# Terminal 2: Frontend
cd app\frontend
npm run dev
# → http://localhost:3000

# Terminal 3: ML (when needed)
cd ml-pipeline
.\venv-ml\Scripts\Activate.ps1
python training/train_yolo.py
```

## 📖 Documentation Cheat Sheet

| Need | Read This |
|------|-----------|
| 🎯 **Overview** | [NEW_STRUCTURE_SUMMARY.md](NEW_STRUCTURE_SUMMARY.md) |
| 📊 **Visuals** | [VISUAL_STRUCTURE.md](VISUAL_STRUCTURE.md) |
| 🏗️ **Architecture** | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 🔄 **Migration** | [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) |
| 📊 **ML Setup** | [ml-pipeline/README.md](ml-pipeline/README.md) |
| 🚀 **Backend Setup** | [app/backend/README.md](app/backend/README.md) |
| 🎨 **Frontend Setup** | [app/frontend/README.md](app/frontend/README.md) |

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `shared/configs/model_config.yaml` | ML model settings |
| `shared/configs/agent_config.yaml` | Agent system config |
| `shared/configs/policy_profiles.yaml` | Urban policies |
| `ml-pipeline/requirements-ml.txt` | ML dependencies |
| `app/backend/requirements-backend.txt` | Backend dependencies |
| `app/frontend/package.json` | Frontend dependencies |

## 🎯 Component Responsibilities

| Component | Does | Doesn't Do |
|-----------|------|------------|
| **ML Pipeline** | Train models, process data, experiments | ❌ Serve API, real-time inference |
| **Backend** | Serve API, run inference, manage DB | ❌ Train models, collect data |
| **Frontend** | Show UI, user interaction | ❌ Direct DB access, model inference |

## 🔄 Typical Workflow

```
1. ML Pipeline: Train models → Export to trained_models/
2. Copy models: ml-pipeline/trained_models/ → app/backend/models/
3. Backend: Load models → Serve API
4. Frontend: Call API → Display results
```

## 📦 Dependencies

| Component | Size | Key Libraries |
|-----------|------|--------------|
| ML Pipeline | ~3 GB | PyTorch, TensorFlow, GDAL |
| Backend | ~500 MB | FastAPI, LangChain, ONNX |
| Frontend | ~200 MB | Next.js, React, Leaflet |

## 🚀 API Endpoints

```
http://localhost:8000/docs          ← API Documentation
http://localhost:8000/health        ← Health Check
http://localhost:8000/api/cities    ← Cities API
http://localhost:8000/api/scenarios ← Scenarios API
http://localhost:8000/api/chat      ← AI Chat API
```

## 🎨 Frontend Pages

```
http://localhost:3000/              ← Home
http://localhost:3000/dashboard     ← Dashboard
http://localhost:3000/scenarios     ← Scenarios
http://localhost:3000/chat          ← AI Chat
```

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | Check virtual env activated |
| Module not found | `pip install -r requirements-*.txt` |
| Port already in use | Change port or kill process |
| Database error | Check PostgreSQL running |
| Frontend can't reach API | Check backend is running |

## 🔧 Environment Variables

```bash
# ML Pipeline (.env in ml-pipeline/)
GOOGLE_SERVICE_ACCOUNT_EMAIL=...
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=...
MLFLOW_TRACKING_URI=http://localhost:5000

# Backend (.env in app/backend/)
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379
GOOGLE_GEMINI_API_KEY=...
GROQ_API_KEY=...
SECRET_KEY=...

# Frontend (.env.local in app/frontend/)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 📊 Project Status

- ✅ Structure created
- ✅ Configurations set up
- ✅ Documentation complete
- 🔄 ML implementation needed
- 🔄 Backend endpoints needed
- 🔄 Frontend components needed

## 🎯 Next Steps

1. ✅ Read [NEW_STRUCTURE_SUMMARY.md](NEW_STRUCTURE_SUMMARY.md)
2. ✅ Choose component to work on
3. ⏭️ Set up environment
4. ⏭️ Start coding!

## 📞 Need Help?

1. Check component README
2. Review [ARCHITECTURE.md](ARCHITECTURE.md)
3. Search [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

**Print this card and keep it handy! 📄**

**Project Version**: 0.2.0 (Separated Architecture)
**Last Updated**: November 9, 2025
