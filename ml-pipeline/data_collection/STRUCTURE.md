# Data Collection - Clean Project Structure

**Last Updated:** November 12, 2025

---

## ✅ Current Structure

```
ml-pipeline/data_collection/
├── define_city_boundaries.py           # ✅ Phase 1 Step 1: OSM queries & boundary calculation
├── create_tile_grids.py                # ✅ Phase 1 Step 2: 2km×2km tile grid generation
├── export_xtnt_files.py                # ✅ Phase 1 Step 3: XTNT file export for QGIS
├── README_DATA_COLLECTION.md           # ✅ Complete workflow documentation
│
├── qgis_frames/                        # ✅ 24 .xtnt files for QGIS MapTileLoader
│   ├── tunis_tiles_full.xtnt
│   ├── tunis_tiles_north_west.xtnt
│   ├── tunis_tiles_north_east.xtnt
│   ├── tunis_tiles_south_west.xtnt
│   ├── tunis_tiles_south_east.xtnt
│   ├── copenhagen_tiles_full.xtnt
│   ├── copenhagen_tiles_north_west.xtnt
│   ├── copenhagen_tiles_north_east.xtnt
│   ├── copenhagen_tiles_south_west.xtnt
│   ├── copenhagen_tiles_south_east.xtnt
│   ├── shenzhen_tiles_full.xtnt
│   ├── shenzhen_tiles_north_west.xtnt
│   ├── shenzhen_tiles_north_center.xtnt
│   ├── shenzhen_tiles_north_east.xtnt
│   ├── shenzhen_tiles_south_west.xtnt
│   ├── shenzhen_tiles_south_center.xtnt
│   ├── shenzhen_tiles_south_east.xtnt
│   ├── phoenix_tiles_full.xtnt
│   ├── phoenix_tiles_north_west.xtnt
│   ├── phoenix_tiles_north_center.xtnt
│   ├── phoenix_tiles_north_east.xtnt
│   ├── phoenix_tiles_south_west.xtnt
│   ├── phoenix_tiles_south_center.xtnt
│   └── phoenix_tiles_south_east.xtnt
│
├── scripts/                            # ✅ Utility scripts (kept for reference)
│   └── archive/                        # Old test/phase scripts
│
└── archive_phase2-5/                   # ✅ Old download/processing scripts
    ├── download_sentinel.py
    ├── download_osm_renders.py
    ├── download_topographic.py
    ├── download_osm.py
    ├── aligned_download.py
    ├── verify_alignment.py
    ├── stitch_tiles.py
    ├── CENTERED_APPROACH.md
    ├── master_data_prompt.md
    └── README.md
```

---

## 📂 Related Data Directories

```
ml-pipeline/datasets/
├── city_boundaries.json                # All 4 city boundaries
├── city_boundaries_map.png             # Visualization (all cities overlay)
├── tunis_tile_grid.png                 # Grid visualization
├── copenhagen_tile_grid.png            # Grid visualization
├── shenzhen_tile_grid.png              # Grid visualization
├── phoenix_tile_grid.png               # Grid visualization
└── manifests/
    ├── tunis_tile_manifest.json        # 405 tiles
    ├── copenhagen_tile_manifest.json   # 390 tiles
    ├── shenzhen_tile_manifest.json     # 13,158 tiles
    └── phoenix_tile_manifest.json      # 4,450 tiles
```

---

## 🎯 File Count Summary

### Active Files (Phase 1 - Python)
- **Core Scripts**: 3 files
  - `define_city_boundaries.py`
  - `create_tile_grids.py`
  - `export_xtnt_files.py`

### Generated Outputs
- **XTNT Files**: 24 files (in `qgis_frames/`)
- **Tile Manifests**: 4 JSON files
- **Visualizations**: 5 PNG files
- **Documentation**: 2 files (README + this file)

### Archived Files
- **Phase 2-5 Scripts**: 10 Python files
- **Old Documentation**: 3 Markdown files
- **Total Archived**: 13 files

---

## 🚀 Quick Commands

### Run Complete Phase 1 Pipeline
```bash
# From project root
cd ml-pipeline/data_collection
python export_xtnt_files.py
```

### Load Frame in QGIS
1. Open QGIS Desktop
2. Plugins → MapTileLoader
3. Click "Load frame"
4. Browse to: `ml-pipeline/data_collection/qgis_frames/<city>_tiles_<quadrant>.xtnt`
5. Select tile source (e.g., "ESRI Wayback 2016")
6. Set zoom level: 18
7. Click "Download"

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| **Total Cities** | 4 |
| **Total Tiles** | 18,403 |
| **XTNT Files** | 24 (4 full + 20 quadrants/chunks) |
| **Active Python Scripts** | 3 |
| **Archived Scripts** | 13 |
| **Code Reduction** | ~80% |

---

## 🔧 Maintenance

### Regenerate All Files
```bash
# Activate environment
.\ml-pipeline\venv-ml\Scripts\Activate.ps1

# Export XTNT files
cd ml-pipeline/data_collection
python export_xtnt_files.py
```

### Update City Configuration
Edit `define_city_boundaries.py`, then:
```bash
python define_city_boundaries.py
python create_tile_grids.py
python export_xtnt_files.py
```

---

## 📝 Notes

- **Archive folder** (`archive_phase2-5/`) contains old Phase 2-5 download/processing scripts that are no longer needed since we're using QGIS manual workflow
- **Scripts/archive folder** contains old test scripts and phase runners
- All paths in documentation are relative to `ml-pipeline/data_collection/`
- XTNT files can be loaded directly in QGIS MapTileLoader plugin

---

**Status**: ✅ Clean and Organized - Ready for QGIS Workflow!
