# 📊 ML Pipeline

Machine Learning and Data Science components for the Urban Evolution AI Platform.

## 🎯 Purpose

This directory contains all machine learning research, experimentation, model training, and data processing code. It's separate from the production application to:

- Allow data scientists to work independently
- Use heavy ML dependencies without bloating the app
- Enable GPU-intensive training on dedicated servers
- Facilitate model versioning and experimentation

## 📁 Structure

```
ml-pipeline/
├── data_collection/     # Download satellite & geospatial data
├── models/             # Model implementations (YOLO, LSTM, etc.)
├── training/           # Training scripts
├── notebooks/          # Jupyter notebooks for exploration
├── experiments/        # MLflow experiment tracking
├── datasets/           # Training data (raw & processed)
└── trained_models/     # Exported models for production
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd ml-pipeline

# Create virtual environment
python -m venv venv-ml

# Activate (Windows)
.\venv-ml\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv-ml/bin/activate

# Install dependencies
pip install -r requirements-ml.txt
```

### 2. Configure API Keys

Create `.env` file in the ml-pipeline directory:

```bash
# Google Earth Engine
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-service-account@project.iam.gserviceaccount.com
GOOGLE_SERVICE_ACCOUNT_KEY_PATH=path/to/service-account-key.json

# MLflow (optional)
MLFLOW_TRACKING_URI=http://localhost:5000

# Weights & Biases (optional)
WANDB_API_KEY=your-wandb-key
```

### 3. Download Data

```bash
# Define city boundaries
python data_collection/define_city_boundaries.py --city Tunis

# Create tile grid
python data_collection/create_tile_grids.py --city Tunis


### 4. Train Models

```bash
# Train YOLO for building detection
python training/train_yolo.py --config ../shared/configs/model_config.yaml

# Train LSTM for growth prediction
python training/train_lstm.py --epochs 100 --batch-size 32

# Train XGBoost classifier
python training/train_xgboost.py
```

### 5. Export Models

```bash
# Export trained models for production
python training/export_models.py --output trained_models/

# This creates:
# - trained_models/yolo_v11_buildings.pt
# - trained_models/lstm_growth.h5
# - trained_models/xgboost_classifier.pkl
# - trained_models/model_metadata.json
```

## 📓 Jupyter Notebooks

Explore data and experiment with models:

```bash
# Start Jupyter Lab
jupyter lab

# Open notebooks in ml-pipeline/notebooks/
# - 01_data_exploration.ipynb
# - 02_yolo_training.ipynb
# - 03_growth_analysis.ipynb
# - 04_policy_scenarios.ipynb
```

## 🔬 Experiment Tracking

We use MLflow to track experiments:

```bash
# Start MLflow server
mlflow server --backend-store-uri sqlite:///experiments/mlflow.db --default-artifact-root ./experiments/mlruns --host 0.0.0.0 --port 5000

# View experiments at: http://localhost:5000
```

## 📦 Data Collection

### Sentinel-2 Satellite Imagery

```python
from data_collection.download_sentinel import SentinelDownloader

downloader = SentinelDownloader()
downloader.download_city(
    city_name="Tunis",
    start_date="2020-01-01",
    end_date="2023-12-31",
    cloud_coverage=20
)
```

### OpenStreetMap Data

```python
from data_collection.download_osm import OSMDownloader

downloader = OSMDownloader()
downloader.download_city(
    city_name="Tunis",
    features=["buildings", "roads", "amenities"]
)
```

## 🤖 Model Training

### YOLOv11 Building Detection

```bash
python training/train_yolo.py \
    --data datasets/processed/yolo_dataset.yaml \
    --epochs 100 \
    --batch 16 \
    --img 640 \
    --device 0
```

### LSTM Spatial Growth

```bash
python training/train_lstm.py \
    --input datasets/processed/growth_sequences.npz \
    --epochs 100 \
    --hidden-size 128 \
    --layers 3
```

### XGBoost Building Classifier

```bash
python training/train_xgboost.py \
    --input datasets/processed/building_features.csv \
    --target building_type \
    --cv 5
```

## 📊 Model Evaluation

```bash
# Evaluate all models
python training/evaluate_models.py --models all

# Evaluate specific model
python training/evaluate_models.py --model yolo --test-set datasets/processed/test/
```

## 🔧 Configuration

Model configurations are in `../shared/configs/model_config.yaml`:

```yaml
yolo:
  model: yolov8n
  imgsz: 640
  epochs: 100
  batch: 16
  conf_threshold: 0.25
  iou_threshold: 0.45

lstm:
  input_size: 10
  hidden_size: 128
  num_layers: 3
  dropout: 0.2
  learning_rate: 0.001

xgboost:
  max_depth: 6
  learning_rate: 0.1
  n_estimators: 100
  objective: multi:softmax
```

## 🚀 Exporting to Production

After training, export models for the application:

```bash
# Export all models
python training/export_models.py \
    --output ../app/backend/models/ \
    --format onnx

# This converts models to ONNX for efficient inference
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=. --cov-report=html
```

## 📚 Documentation

- **Data Collection**: See `data_collection/README.md`
- **Model Architecture**: See `models/README.md`
- **Training Guide**: See `training/README.md`

## 🐛 Troubleshooting

### GDAL Installation Issues

```bash
# Windows: Install OSGeo4W first
# Download from: https://trac.osgeo.org/osgeo4w/

# Linux
sudo apt-get install gdal-bin libgdal-dev

# Mac
brew install gdal
```

### Google Earth Engine Authentication

```bash
# Authenticate
earthengine authenticate

# Test connection
python -c "import ee; ee.Initialize(); print('Success!')"
```

### CUDA/GPU Issues

```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Install CUDA-enabled PyTorch
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## 📞 Support

For issues related to ML pipeline:
- Check `docs/ML_TROUBLESHOOTING.md`
- Review MLflow experiments for training issues
- Check data quality with notebooks

## 🎯 Next Steps

1. **Download Data**: Start with one city (Tunis)
2. **Explore Data**: Use Jupyter notebooks
3. **Train Models**: Begin with YOLO
4. **Evaluate**: Check model metrics
5. **Export**: Convert models for production

Happy Training! 🚀
