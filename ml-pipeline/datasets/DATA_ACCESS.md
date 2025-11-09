# 📊 Training Data Access

This document provides information on accessing the training datasets used for the Urban Evolution AI project.

---

## 🚫 Data Not in Repository

**Training data is NOT included in this repository** due to size constraints and GitHub limitations.

The following data directories are ignored by `.gitignore`:
- `data/raw/` - Raw satellite imagery and geospatial data
- `data/processed/` - Preprocessed training datasets
- Large geospatial files (`.tif`, `.geotiff`, `.hdf`, `.h5`, etc.)
- Model checkpoint files (`.pt`, `.pth`, `.h5`, `.pkl`, etc.)

---

## ☁️ Cloud Storage Access

### Training Datasets

**📦 Cloud Drive Link:**  
🔗 [**INSERT YOUR CLOUD DRIVE LINK HERE**]  
*(Google Drive, OneDrive, Dropbox, etc.)*

**Estimated Size:** ~XX GB  
**Last Updated:** November 9, 2025

---

## 📂 Expected Data Structure

After downloading, extract the data into the project directory:

```
urban-evolution-ai/
├── data/
│   ├── raw/                          # Raw data (ignored by git)
│   │   ├── sentinel/                 # Satellite imagery
│   │   │   ├── city_name/
│   │   │   │   ├── 2020/
│   │   │   │   ├── 2021/
│   │   │   │   └── ...
│   │   ├── osm/                      # OpenStreetMap vector data
│   │   │   └── city_name.geojson
│   │   └── topographic/              # Elevation data
│   │       └── city_name_dem.tif
│   │
│   ├── processed/                    # Processed datasets (ignored by git)
│   │   ├── training/
│   │   │   ├── images/
│   │   │   ├── labels/
│   │   │   └── metadata.json
│   │   ├── validation/
│   │   └── test/
│   │
│   └── README.md                     # Data collection notes
```

---

## 🔄 Data Collection Scripts

If you need to collect your own data:

### 1. Satellite Imagery (Sentinel-2)
```bash
cd ml-pipeline
.\venv-ml\Scripts\Activate.ps1
python data_collection/download_sentinel.py --city "Your City" --years 2020-2024
```

### 2. OpenStreetMap Data
```bash
python data_collection/download_osm.py --city "Your City"
```

### 3. Topographic Data
```bash
python data_collection/download_topographic.py --city "Your City"
```

**Note:** These scripts require:
- Google Earth Engine account and API key
- Sufficient disk space (~50-100 GB per city)
- Stable internet connection

---

## 📋 Dataset Contents

### Raw Data Includes:
- **Sentinel-2 Satellite Imagery** (10m resolution)
  - Multi-spectral bands (RGB, NIR, SWIR)
  - Time series: 2015-2024
  - Coverage: Multiple cities
  
- **OpenStreetMap Vector Data**
  - Building footprints
  - Road networks
  - Land use polygons
  - Points of interest

- **Topographic Data**
  - Digital Elevation Models (DEM)
  - Slope and aspect derivatives
  - Drainage networks

### Processed Data Includes:
- **Training Images** (512x512 patches)
  - Normalized and augmented
  - Format: PNG/TIFF
  
- **Annotation Labels**
  - YOLO format for building detection
  - Segmentation masks for urban areas
  - Time-series metadata

- **Feature Datasets**
  - Extracted features for time-series models
  - Growth statistics and trends
  - Urban metrics (density, green space, etc.)

---

## 🔐 Data Privacy & Ethics

**Important:** This data contains information about real urban areas. Please:

- ✅ Use only for research and educational purposes
- ✅ Respect privacy when analyzing residential areas
- ✅ Follow data provider terms of service
- ✅ Cite data sources in publications
- ❌ Do not distribute without permission
- ❌ Do not use for commercial purposes without proper licensing

See `ETHICS.md` for more information on responsible AI practices.

---

## 📊 Data Statistics

| Dataset | Size | Files | Cities | Years |
|---------|------|-------|--------|-------|
| Sentinel-2 Imagery | XX GB | XX,XXX | XX | 2015-2024 |
| OSM Vector Data | XX GB | XXX | XX | Current |
| Topographic Data | XX GB | XXX | XX | Latest |
| Processed Training | XX GB | XX,XXX | XX | - |
| **Total** | **~XX GB** | **XX,XXX** | **XX** | - |

*Statistics will be updated once data collection is complete*

---

## 🚀 Quick Start

### Option 1: Download Pre-collected Data (Recommended)

1. **Download from cloud drive** (link above)
2. **Extract to project directory:**
   ```powershell
   # Extract to: D:\Tek-UP\5eme SDIA\Projects\urban-evolution-ai\data\
   ```
3. **Verify structure:**
   ```powershell
   cd ml-pipeline
   python scripts/verify_data.py
   ```

### Option 2: Collect Your Own Data

1. **Configure API keys** in `.env`:
   ```
   GOOGLE_EARTH_ENGINE_PROJECT=your-project-id
   ```
2. **Run data collection scripts** (see above)
3. **Process raw data:**
   ```powershell
   python preprocessing/prepare_training_data.py
   ```

---

## 🆘 Troubleshooting

### Issue: "Missing data directory"
**Solution:** Create the directory structure:
```powershell
mkdir data\raw\sentinel, data\raw\osm, data\raw\topographic
mkdir data\processed\training, data\processed\validation, data\processed\test
```

### Issue: "Cannot access cloud drive link"
**Solution:** Contact the project maintainer for access permissions.

### Issue: "Data validation fails"
**Solution:** Re-download the data or run collection scripts to regenerate.

---

## 📞 Support

For data access issues or questions:
- Open an issue on GitHub
- Contact: [your-email@example.com]
- Check `docs/` folder for additional documentation

---

## 🔄 Data Updates

**Current Version:** v1.0 (Initial collection)  
**Last Updated:** November 9, 2025  
**Next Update:** TBD (after model training validation)

Check this file regularly for updates to the cloud storage link and data structure.

---

**🔗 Cloud Drive Link:** [INSERT YOUR LINK HERE]  
**📧 For Access:** Contact project maintainer
