"""
XTNT File Exporter for QGIS MapTileLoader Plugin

This module exports city boundaries and tile grids as .xtnt files
for use with QGIS MapTileLoader plugin to download satellite imagery.

Author: Amine Mayoufi & Walaa Hidaya
Date: November 12, 2025
"""

import json
import logging
from pathlib import Path
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class XTNTExporter:
    """
    Export city boundaries as .xtnt files for QGIS MapTileLoader plugin.
    
    XTNT format:
    Line 1: west_longitude,north_latitude (upper-left corner)
    Line 2: east_longitude,south_latitude (lower-right corner)
    """
    
    def __init__(self, manifests_dir: str = './ml-pipeline/datasets/manifests',
                 output_dir: str = './ml-pipeline/data_collection/qgis_frames'):
        """
        Initialize XTNT exporter.
        
        Args:
            manifests_dir: Directory containing tile manifests
            output_dir: Directory to save .xtnt files
        """
        self.manifests_dir = Path(manifests_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized XTNTExporter")
        logger.info(f"  Manifests: {self.manifests_dir}")
        logger.info(f"  Output: {self.output_dir}")
    
    def export_city_full(self, city_name: str) -> str:
        """
        Export full city boundary as .xtnt file.
        
        Args:
            city_name: Name of the city
            
        Returns:
            Path to created .xtnt file
        """
        manifest_path = self.manifests_dir / f"{city_name}_tile_manifest.json"
        
        if not manifest_path.exists():
            logger.error(f"Manifest not found: {manifest_path}")
            return None
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        bbox = manifest['master_bbox']
        west = bbox['west']
        south = bbox['south']
        east = bbox['east']
        north = bbox['north']
        
        # Create .xtnt file
        output_file = self.output_dir / f"{city_name}_tiles_full.xtnt"
        with open(output_file, 'w') as f:
            f.write(f"{west},{north}\n{east},{south}")
        
        grid = manifest['grid_dimensions']
        logger.info(f"✅ {output_file.name}")
        logger.info(f"   {bbox['width_km']} x {bbox['height_km']} km, {grid['n_tiles']} tiles")
        logger.info(f"   {west:.6f},{north:.6f} to {east:.6f},{south:.6f}")
        
        return str(output_file)
    
    def export_city_quadrants(self, city_name: str, n_splits_x: int = 2, n_splits_y: int = 2) -> List[str]:
        """
        Export city split into quadrants as separate .xtnt files.
        
        Args:
            city_name: Name of the city
            n_splits_x: Number of horizontal splits (columns)
            n_splits_y: Number of vertical splits (rows)
            
        Returns:
            List of paths to created .xtnt files
        """
        manifest_path = self.manifests_dir / f"{city_name}_tile_manifest.json"
        
        if not manifest_path.exists():
            logger.error(f"Manifest not found: {manifest_path}")
            return []
        
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        bbox = manifest['master_bbox']
        grid = manifest['grid_dimensions']
        
        west = bbox['west']
        south = bbox['south']
        east = bbox['east']
        north = bbox['north']
        width_km = bbox['width_km']
        height_km = bbox['height_km']
        n_tiles = grid['n_tiles']
        
        logger.info(f"\n📦 Splitting {city_name} into {n_splits_x}x{n_splits_y} = {n_splits_x * n_splits_y} chunks")
        logger.info(f"   Each chunk: ~{width_km/n_splits_x:.1f} x {height_km/n_splits_y:.1f} km")
        logger.info(f"   Expected ~{n_tiles/(n_splits_x*n_splits_y):.0f} tiles per chunk\n")
        
        step_lon = (east - west) / n_splits_x
        step_lat = (north - south) / n_splits_y
        
        output_files = []
        
        for row in range(n_splits_y):
            for col in range(n_splits_x):
                chunk_west = west + col * step_lon
                chunk_east = west + (col + 1) * step_lon
                chunk_south = south + row * step_lat
                chunk_north = south + (row + 1) * step_lat
                
                # Generate chunk name
                if n_splits_y == 2:
                    row_name = 'north' if row == 0 else 'south'
                else:
                    row_name = f"row{row}"
                
                if n_splits_x == 2:
                    col_name = 'west' if col == 0 else 'east'
                elif n_splits_x == 3:
                    col_name = ['west', 'center', 'east'][col]
                else:
                    col_name = f"col{col}"
                
                chunk_name = f"{row_name}_{col_name}"
                
                # Create .xtnt file
                output_file = self.output_dir / f"{city_name}_tiles_{chunk_name}.xtnt"
                with open(output_file, 'w') as f:
                    f.write(f"{chunk_west},{chunk_north}\n{chunk_east},{chunk_south}")
                
                logger.info(f"✅ {output_file.name}")
                logger.info(f"   {chunk_west:.6f},{chunk_north:.6f} to {chunk_east:.6f},{chunk_south:.6f}")
                
                output_files.append(str(output_file))
        
        return output_files
    
    def export_all_cities(self, split_config: Dict[str, tuple] = None):
        """
        Export all cities with their tile manifests.
        
        Args:
            split_config: Dictionary mapping city names to (n_splits_x, n_splits_y) tuples.
                         If None, uses default split configuration.
        """
        # Default split configuration
        if split_config is None:
            split_config = {
                'tunis': (2, 2),        # 4 quadrants
                'copenhagen': (2, 2),   # 4 quadrants
                'shenzhen': (3, 2),     # 6 chunks
                'phoenix': (3, 2)       # 6 chunks
            }
        
        logger.info("=" * 70)
        logger.info("EXPORTING XTNT FILES FOR ALL CITIES")
        logger.info("=" * 70)
        
        all_files = []
        
        for manifest_file in sorted(self.manifests_dir.glob("*_tile_manifest.json")):
            city_name = manifest_file.stem.replace('_tile_manifest', '')
            
            logger.info(f"\n🌍 Processing {city_name.upper()}...")
            
            # Export full extent
            full_file = self.export_city_full(city_name)
            if full_file:
                all_files.append(full_file)
            
            # Export quadrants/chunks
            if city_name in split_config:
                n_x, n_y = split_config[city_name]
                chunk_files = self.export_city_quadrants(city_name, n_x, n_y)
                all_files.extend(chunk_files)
        
        logger.info(f"\n{'=' * 70}")
        logger.info(f"✅ EXPORT COMPLETE")
        logger.info(f"{'=' * 70}")
        logger.info(f"📁 Output directory: {self.output_dir}")
        logger.info(f"📄 Total files created: {len(all_files)}")
        
        return all_files


def main():
    """Main function to export all .xtnt files."""
    exporter = XTNTExporter()
    
    # Export all cities with custom split configurations
    split_config = {
        'tunis': (2, 2),        # 405 tiles → 4 quadrants (~101 tiles each)
        'copenhagen': (2, 2),   # 390 tiles → 4 quadrants (~98 tiles each)
        'shenzhen': (3, 2),     # 13158 tiles → 6 chunks (~2193 tiles each)
        'phoenix': (3, 2)       # 4450 tiles → 6 chunks (~742 tiles each)
    }
    
    exporter.export_all_cities(split_config)


if __name__ == '__main__':
    main()
