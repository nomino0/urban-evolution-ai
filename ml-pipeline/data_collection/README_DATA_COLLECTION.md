# Urban Evolution AI - Data Collection Setup

## Project Overview
This project generates tile grids for 4 cities (Tunis, Copenhagen, Shenzhen, Phoenix) to collect satellite imagery for urban change detection using AI models.

**Project Team:** Amine Mayoufi & Walaa Hidaya  
**Date:** November 2025

---

## 🎯 Workflow Summary

### Phase 1: City Boundaries & Tile Grids (Automated)
1. **Define city boundaries** using OpenStreetMap data
2. **Create tile grids** (2km × 2km tiles, 512×512 pixels each)
3. **Export `.xtnt` files** for QGIS MapTileLoader plugin
4. **Generate visualizations** of boundaries and grids

### Phase 2: Satellite Imagery Download (Manual - QGIS)
Use **QGIS Desktop** with **MapTileLoader Plugin** to download satellite imagery tiles.

---

## 📊 City Configurations

| City | Area (km²) | Grid Size | Total Tiles | Clearance | Notes |
|------|------------|-----------|-------------|-----------|-------|
| **Tunis** | 53.38 × 30.03 | 27 × 15 | 405 | 15 km | Mediterranean developing city |
| **Copenhagen** | 52.09 × 29.30 | 26 × 15 | 390 | 8 km | Shifted 5km west to avoid water |
| **Shenzhen** | 306.96 × 172.66 | 153 × 86 | 13,158 | 20 km | Rapid growth megacity |
| **Phoenix** | 177.24 × 99.70 | 89 × 50 | 4,450 | 15 km | Desert sprawl city |

**Total tiles across all cities: 18,403 tiles**

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- QGIS Desktop 3.40+ ([Download](https://qgis.org/))
- Virtual environment (recommended)

### Python Environment Setup

```bash
# Create virtual environment
python -m venv venv-ml

# Activate virtual environment
# Windows:
.\venv-ml\Scripts\activate
# Linux/Mac:
source venv-ml/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Required Python Packages
```
osmnx
geopandas
shapely
matplotlib
numpy
Pillow
```

---

## 📁 Project Structure

```
urban-evolution-ai/
├── ml-pipeline/
│   ├── data_collection/
│   │   ├── define_city_boundaries.py    # Step 1: Define city boundaries
│   │   ├── create_tile_grids.py         # Step 2: Create tile grids
│   │   ├── export_xtnt_files.py         # Step 3: Export .xtnt for QGIS
│   │   └── scripts/
│   │       └── run_phase1.py            # Run all Phase 1 steps
│   └── datasets/
│       ├── city_boundaries.json         # City boundary definitions
│       ├── city_boundaries_map.png      # Visualization of all cities
│       ├── manifests/                   # Tile grid manifests (JSON)
│       │   ├── tunis_tile_manifest.json
│       │   ├── copenhagen_tile_manifest.json
│       │   ├── shenzhen_tile_manifest.json
│       │   └── phoenix_tile_manifest.json
│       ├── tunis_tile_grid.png          # Grid visualizations
│       ├── copenhagen_tile_grid.png
│       ├── shenzhen_tile_grid.png
│       └── phoenix_tile_grid.png
├── qgis_frames/                         # .xtnt files for QGIS
│   ├── tunis_tiles_full.xtnt
│   ├── tunis_tiles_northwest.xtnt
│   ├── tunis_tiles_northeast.xtnt
│   ├── tunis_tiles_southwest.xtnt
│   ├── tunis_tiles_southeast.xtnt
│   └── ... (similar for other cities)
└── README_DATA_COLLECTION.md            # This file
```

---

## 🔧 Phase 1: Generate Boundaries & Grids

### Run Complete Phase 1

```bash
# Activate virtual environment
.\ml-pipeline\venv-ml\Scripts\Activate.ps1

# Run Phase 1 pipeline (boundaries + grids + xtnt export)
python ml-pipeline/data_collection/scripts/run_phase1.py
```

This will:
1. ✅ Query OpenStreetMap for city boundaries
2. ✅ Calculate 16:9 master bounding boxes
3. ✅ Generate 2km × 2km tile grids
4. ✅ Create tile manifests (JSON)
5. ✅ Generate visualization maps (PNG)
6. ✅ Export `.xtnt` files for QGIS

### Run Individual Steps

```bash
# Step 1: Define city boundaries
python ml-pipeline/data_collection/define_city_boundaries.py

# Step 2: Create tile grids
python ml-pipeline/data_collection/create_tile_grids.py

# Step 3: Export .xtnt files
python ml-pipeline/data_collection/export_xtnt_files.py
```

---

## 🗺️ Phase 2: Download Satellite Imagery (QGIS)

### QGIS MapTileLoader Plugin Setup

1. **Install QGIS Desktop**
   - Download from: https://qgis.org/
   - Version 3.40+ recommended

2. **Install MapTileLoader Plugin**
   - Open QGIS
   - Plugins → Manage and Install Plugins
   - Search: "MapTileLoader"
   - Install

3. **Add Custom Tile Sources**
   
   Edit plugin file: `C:\Users\<your-user>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\map_tile_loader\map_tile_loader_dialog.py`
   
   Add these tile sources to `dict_sources`:

   ```python
   "OpenStreetMap Standard": {
       "url": "https://tile.openstreetmap.org/{2}/{0}/{1}.png", 
       "zmax": 19
   },
   
   "ESRI Wayback 2016": {
       "url": "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/18966/{2}/{1}/{0}", 
       "zmax": 20
   },
   
   "ESRI Wayback 2014-07-02": {
       "url": "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/3026/{2}/{1}/{0}", 
       "zmax": 20
   },
   
   "ESRI Wayback 2020-10-14": {
       "url": "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/119/{2}/{1}/{0}", 
       "zmax": 20
   }
   ```

### Download Workflow

#### For Each City Quadrant:

1. **Open QGIS Desktop**

2. **Load Frame**
   - Plugins → MapTileLoader
   - Click "Load frame" button
   - Browse to: `qgis_frames/<city>_tiles_<quadrant>.xtnt`
   - Example: `tunis_tiles_northwest.xtnt`

3. **Configure Download**
   - **Source**: Select tile source (e.g., "ESRI Wayback 2016")
   - **Zoom level**: 18 (recommended for 2km tiles at ~1m/pixel)
   - **Save to**: Choose output directory

4. **Download Tiles**
   - Click "Download" button
   - Wait for completion
   - Georeferenced TIFF will be saved automatically

5. **Repeat for All Quadrants**
   - Load next `.xtnt` file
   - Download with same settings
   - Organize files by city and year

---

## 📦 Tile Coverage Breakdown

### Tunis (4 Quadrants)
- **Full extent**: 405 tiles
- **Per quadrant**: ~101 tiles
- Files:
  - `tunis_tiles_northwest.xtnt`
  - `tunis_tiles_northeast.xtnt`
  - `tunis_tiles_southwest.xtnt`
  - `tunis_tiles_southeast.xtnt`

### Copenhagen (4 Quadrants)
- **Full extent**: 390 tiles
- **Per quadrant**: ~98 tiles
- **Special**: Shifted 5km west to avoid Øresund water
- Files: Same naming as Tunis

### Shenzhen (6 Chunks)
- **Full extent**: 13,158 tiles
- **Per chunk**: ~2,193 tiles
- Split: 3 columns × 2 rows
- Files:
  - `shenzhen_tiles_north_west.xtnt`
  - `shenzhen_tiles_north_center.xtnt`
  - `shenzhen_tiles_north_east.xtnt`
  - `shenzhen_tiles_south_west.xtnt`
  - `shenzhen_tiles_south_center.xtnt`
  - `shenzhen_tiles_south_east.xtnt`

### Phoenix (6 Chunks)
- **Full extent**: 4,450 tiles
- **Per chunk**: ~742 tiles
- Split: 3 columns × 2 rows
- Files: Same naming as Shenzhen

---

## 🎨 Visualization Files

### Generated Maps

1. **`city_boundaries_map.png`**
   - All 4 cities with boundaries and master bboxes
   - Shows 16:9 aspect ratio capture areas

2. **`<city>_tile_grid.png`**
   - Individual city tile grid visualization
   - Shows 2km × 2km tiles overlaid on OSM map
   - Examples:
     - `tunis_tile_grid.png` (27×15 grid)
     - `copenhagen_tile_grid.png` (26×15 grid)
     - `shenzhen_tile_grid.png` (153×86 grid)
     - `phoenix_tile_grid.png` (89×50 grid)

---

## 📝 Data Collection Years

### Target Years for Satellite Imagery:
- **2016** (baseline - post Sentinel-2A launch)
- **2020** (mid-period)
- **2024** (current/recent)

### Recommended ESRI Wayback Dates:
- **2016**: Use `ESRI Wayback 2016` (release 18966)
- **2014**: Alternative - `ESRI Wayback 2014-07-02` (release 3026)
- **2020**: Use `ESRI Wayback 2020-10-14` (release 119)

---

## 🔍 Technical Details

### Tile Specifications
- **Size**: 2km × 2km physical area
- **Resolution**: 512 × 512 pixels
- **Pixel size**: ~3.9 meters/pixel at zoom 18
- **Format**: GeoTIFF (after QGIS download)
- **CRS**: EPSG:3857 (Web Mercator)

### Coordinate System
- **Input**: EPSG:4326 (WGS84 lat/lon)
- **Output**: EPSG:3857 (Web Mercator)
- **Tile coordinates**: Calculated using Mercator projection

### Grid Calculation
- **Aspect ratio**: 16:9 (master bounding box)
- **Clearance**: Minimum distance from city edge to box edge
  - Tunis: 15 km
  - Copenhagen: 8 km (reduced, shifted west)
  - Shenzhen: 20 km
  - Phoenix: 15 km

---

## ⚠️ Important Notes

### Copenhagen Special Configuration
- **Center offset**: Shifted 5km west (away from Øresund strait)
- **Reason**: Original bbox had too much water on eastern side
- **Result**: More land coverage, better urban area capture

### Download Tips
1. **Start with small quadrants** (Tunis/Copenhagen) to test workflow
2. **Use zoom level 18** for optimal balance of detail and file size
3. **Download during off-peak hours** to avoid tile server rate limiting
4. **Organize by city/year** to keep data manageable
5. **Large cities (Shenzhen)**: Download one chunk at a time, may take several hours

### File Sizes (Approximate)
- **Per tile**: ~500 KB (TIFF with compression)
- **Tunis quadrant (~100 tiles)**: ~50 MB
- **Copenhagen quadrant (~100 tiles)**: ~50 MB
- **Shenzhen chunk (~2200 tiles)**: ~1.1 GB
- **Phoenix chunk (~750 tiles)**: ~375 MB

### Rate Limiting
- **OSM tiles**: Rate limited, use slowly
- **ESRI Wayback**: More permissive
- **Google/Yandex**: Check terms of service
- **Recommended**: 8-10 concurrent downloads max

---

## 🛠️ Troubleshooting

### Issue: `.xtnt` file not loading in QGIS
**Solution**: Check file format is exactly:
```
longitude_west,latitude_north
longitude_east,latitude_south
```

### Issue: Downloaded tiles are blank/missing
**Solution**: 
- Check zoom level doesn't exceed `zmax` for tile source
- Verify tile source URL is correct
- Try different tile source (ESRI instead of Google)

### Issue: Python script fails with OSM query
**Solution**:
- Check internet connection
- OSM may be rate limiting - wait and retry
- Fallback bboxes are defined in code

### Issue: Grid visualization shows wrong projection
**Solution**:
- Ensure QGIS project CRS is set to EPSG:3857
- Reload `.xtnt` frame
- Check MapTileLoader plugin settings

---

## 📚 References

### Tools & Libraries
- **QGIS**: https://qgis.org/
- **MapTileLoader Plugin**: https://plugins.qgis.org/plugins/MapTileLoader/
- **OSMnx**: https://osmnx.readthedocs.io/
- **GeoPandas**: https://geopandas.org/

### Tile Sources
- **OpenStreetMap**: https://www.openstreetmap.org/
- **ESRI Wayback**: https://livingatlas.arcgis.com/wayback/
- **Sentinel-2**: https://sentinels.copernicus.eu/web/sentinel/missions/sentinel-2

### Documentation
- **Tile coordinates**: https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
- **Web Mercator projection**: https://epsg.io/3857
- **QGIS Python**: https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/

---

## 📧 Contact & Support

**Project Team:**
- Amine Mayoufi
- Walaa Hidaya

**Institution:** TEK-UP, 5ème SDIA  
**Project:** Urban Evolution AI - Detecting Urban Change with Deep Learning

---

## 📜 License

This project is for academic research purposes.

---

**Last Updated:** November 12, 2025
