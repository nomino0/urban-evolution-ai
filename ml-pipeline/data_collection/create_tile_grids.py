"""
Tile Grid Creation Module

Divides cities into 2km × 2km tiles for manageable data collection.
Creates manifests for tracking tile processing status.

Author: Amine Mayoufi & Walaa Hidaya
Date: November 9, 2025
"""

import logging
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import box, Polygon

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TileGrid:
    """
    Creates and manages tile grids for city data collection.
    
    Divides city bounding boxes into fixed-size tiles (default 2km × 2km).
    Generates unique tile IDs and tracks processing status.
    """
    
    def __init__(
        self,
        city_name: str,
        bbox: Dict,
        tile_size_km: float = 2.0,
        output_dir: str = './ml-pipeline/datasets'
    ):
        """
        Initialize tile grid for a city.
        
        Args:
            city_name: Name of the city
            bbox: Bounding box dictionary with west, south, east, north
            tile_size_km: Size of each tile in kilometers
            output_dir: Directory for saving manifests
        """
        self.city_name = city_name
        self.bbox = bbox
        self.tile_size_km = tile_size_km
        self.output_dir = Path(output_dir)
        self.manifests_dir = self.output_dir / 'manifests'
        self.manifests_dir.mkdir(parents=True, exist_ok=True)
        
        self.tiles = []
        
        logger.info(f"Initialized TileGrid for {city_name}")
        logger.info(f"Bbox: {bbox['width_km']:.2f}km × {bbox['height_km']:.2f}km")
        logger.info(f"Tile size: {tile_size_km}km")
        
        self._create_tile_grid()
    
    def _create_tile_grid(self) -> None:
        """
        Create tile grid with SQUARE tiles (same km width and height).
        Each tile is tile_size_km × tile_size_km (e.g., 2×2 km) in physical space.
        Rendered as 1080×1080 pixels from zoom 18 OSM tiles.
        """
        logger.info(f"Creating SQUARE tile grid for {self.city_name}...")
        
        # Calculate number of tiles needed for square tiles
        center_lat = self.bbox['center_lat']
        center_lat_rad = np.radians(center_lat)
        
        # Account for latitude distortion
        lon_km_per_degree = 111.0 * np.cos(center_lat_rad)
        lat_km_per_degree = 111.0
        
        # For SQUARE tiles in km, we need same physical distance
        # tile_size_km × tile_size_km in real world
        tile_lon_degrees = self.tile_size_km / lon_km_per_degree
        tile_lat_degrees = self.tile_size_km / lat_km_per_degree
        
        # Calculate bbox dimensions
        bbox_width_km = self.bbox['width_km']
        bbox_height_km = self.bbox['height_km']
        
        # Number of square tiles that fit
        n_tiles_lon = int(np.round(bbox_width_km / self.tile_size_km))
        n_tiles_lat = int(np.round(bbox_height_km / self.tile_size_km))
        
        # Adjust bbox slightly to fit exact square tiles
        # This ensures tiles are perfectly square in km
        adjusted_width_km = n_tiles_lon * self.tile_size_km
        adjusted_height_km = n_tiles_lat * self.tile_size_km
        
        logger.info(f"Grid dimensions: {n_tiles_lon} × {n_tiles_lat} tiles")
        logger.info(f"Total tiles: {n_tiles_lon * n_tiles_lat}")
        logger.info(f"Tile size: {self.tile_size_km:.3f}km × {self.tile_size_km:.3f}km (SQUARE)")
        logger.info(f"Adjusted bbox: {adjusted_width_km:.2f}km × {adjusted_height_km:.2f}km")
        
        # Calculate exact tile dimensions in degrees (for square km tiles)
        exact_tile_lon_degrees = tile_lon_degrees
        exact_tile_lat_degrees = tile_lat_degrees
        
        # Center the grid on the bbox center
        grid_width_deg = n_tiles_lon * exact_tile_lon_degrees
        grid_height_deg = n_tiles_lat * exact_tile_lat_degrees
        
        grid_west = self.bbox['center_lon'] - (grid_width_deg / 2)
        grid_south = self.bbox['center_lat'] - (grid_height_deg / 2)
        
        # Create tiles with exact square boundaries
        tile_id = 0
        for row in range(n_tiles_lat):
            for col in range(n_tiles_lon):
                # Calculate tile boundaries (exact square tiles)
                tile_west = grid_west + (col * exact_tile_lon_degrees)
                tile_east = grid_west + ((col + 1) * exact_tile_lon_degrees)
                tile_south = grid_south + (row * exact_tile_lat_degrees)
                tile_north = grid_south + ((row + 1) * exact_tile_lat_degrees)
                
                # Create tile dictionary
                tile = {
                    'tile_id': f"{self.city_name}_tile_{row:03d}_{col:03d}",
                    'numeric_id': tile_id,
                    'row': row,
                    'col': col,
                    'bbox': {
                        'west': tile_west,
                        'south': tile_south,
                        'east': tile_east,
                        'north': tile_north,
                        'center_lat': (tile_south + tile_north) / 2,
                        'center_lon': (tile_west + tile_east) / 2
                    },
                    'pixel_size': {
                        'target_width': 512,
                        'target_height': 512
                    },
                    'physical_size_km': {
                        'width': self.tile_size_km,
                        'height': self.tile_size_km
                    },
                    'status': {
                        'sentinel_2015': 'pending',
                        'sentinel_2020': 'pending',
                        'sentinel_2024': 'pending',
                        'osm_buildings': 'pending',
                        'topographic': 'pending',
                        'osm_renders': 'pending'
                    },
                    'data_sources': {
                        'sentinel_2015': None,
                        'sentinel_2020': None,
                        'sentinel_2024': None,
                        'osm_buildings': None,
                        'topographic': None,
                        'osm_renders': None
                    },
                    'metadata': {
                        'created': None,
                        'last_updated': None,
                        'alignment_verified': False,
                        'quality_score': None
                    }
                }
                
                self.tiles.append(tile)
                tile_id += 1
        
        logger.info(f"✅ Created {len(self.tiles)} tiles with exact boundaries")
    
    def get_tile_by_id(self, tile_id: str) -> Dict:
        """
        Get tile by its string ID.
        
        Args:
            tile_id: Tile identifier string
            
        Returns:
            Tile dictionary or None if not found
        """
        for tile in self.tiles:
            if tile['tile_id'] == tile_id:
                return tile
        return None
    
    def get_tiles_by_status(self, data_source: str, status: str) -> List[Dict]:
        """
        Get tiles filtered by processing status.
        
        Args:
            data_source: Data source name (e.g., 'sentinel_2015')
            status: Status value ('pending', 'processing', 'complete', 'failed')
            
        Returns:
            List of matching tiles
        """
        return [
            tile for tile in self.tiles
            if tile['status'][data_source] == status
        ]
    
    def update_tile_status(
        self,
        tile_id: str,
        data_source: str,
        status: str,
        file_path: str = None
    ) -> bool:
        """
        Update tile processing status.
        
        Args:
            tile_id: Tile identifier
            data_source: Data source name
            status: New status value
            file_path: Path to downloaded file (optional)
            
        Returns:
            True if successful, False otherwise
        """
        tile = self.get_tile_by_id(tile_id)
        if tile is None:
            logger.error(f"Tile not found: {tile_id}")
            return False
        
        tile['status'][data_source] = status
        
        if file_path:
            tile['data_sources'][data_source] = file_path
        
        # Update timestamp
        from datetime import datetime
        tile['metadata']['last_updated'] = datetime.now().isoformat()
        
        return True
    
    def calculate_pixel_coordinates(self, tile: Dict, zoom_level: int = 14) -> Dict:
        """
        Calculate pixel coordinates for Gemini image generation.
        
        Args:
            tile: Tile dictionary
            zoom_level: OSM zoom level
            
        Returns:
            Dictionary with pixel coordinates
        """
        bbox = tile['bbox']
        
        # Web Mercator projection calculations
        def lat_to_y(lat, zoom):
            lat_rad = np.radians(lat)
            y = (1 - np.log(np.tan(lat_rad) + 1 / np.cos(lat_rad)) / np.pi) / 2
            return y * (2 ** zoom) * 256
        
        def lon_to_x(lon, zoom):
            x = (lon + 180) / 360
            return x * (2 ** zoom) * 256
        
        pixel_coords = {
            'x_min': int(lon_to_x(bbox['west'], zoom_level)),
            'x_max': int(lon_to_x(bbox['east'], zoom_level)),
            'y_min': int(lat_to_y(bbox['north'], zoom_level)),
            'y_max': int(lat_to_y(bbox['south'], zoom_level)),
            'zoom_level': zoom_level
        }
        
        pixel_coords['width'] = pixel_coords['x_max'] - pixel_coords['x_min']
        pixel_coords['height'] = pixel_coords['y_max'] - pixel_coords['y_min']
        
        return pixel_coords
    
    def save_manifest(self) -> Path:
        """
        Save tile manifest to JSON file.
        
        Returns:
            Path to saved manifest file
        """
        manifest = {
            'city_name': self.city_name,
            'master_bbox': self.bbox,
            'tile_size_km': self.tile_size_km,
            'grid_dimensions': {
                'n_tiles': len(self.tiles),
                'n_rows': max(t['row'] for t in self.tiles) + 1,
                'n_cols': max(t['col'] for t in self.tiles) + 1
            },
            'tiles': self.tiles
        }
        
        output_file = self.manifests_dir / f"{self.city_name}_tile_manifest.json"
        
        with open(output_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"💾 Saved manifest to: {output_file}")
        
        return output_file
    
    def visualize_grid(self, highlight_tiles: List[str] = None) -> None:
        """
        Visualize the tile grid.
        
        Args:
            highlight_tiles: List of tile IDs to highlight
        """
        logger.info(f"Creating grid visualization for {self.city_name}...")
        
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Plot each tile
        for tile in self.tiles:
            bbox = tile['bbox']
            
            # Determine color
            if highlight_tiles and tile['tile_id'] in highlight_tiles:
                color = 'yellow'
                alpha = 0.5
                linewidth = 2
            else:
                color = 'lightblue'
                alpha = 0.3
                linewidth = 0.5
            
            # Create rectangle
            rect = patches.Rectangle(
                (bbox['west'], bbox['south']),
                bbox['east'] - bbox['west'],
                bbox['north'] - bbox['south'],
                linewidth=linewidth,
                edgecolor='blue',
                facecolor=color,
                alpha=alpha
            )
            ax.add_patch(rect)
            
            # Add tile ID (only for highlighted or small grids)
            if highlight_tiles and tile['tile_id'] in highlight_tiles:
                ax.text(
                    bbox['center_lon'],
                    bbox['center_lat'],
                    f"R{tile['row']}C{tile['col']}",
                    ha='center',
                    va='center',
                    fontsize=8
                )
        
        # Set limits and labels
        ax.set_xlim(self.bbox['west'], self.bbox['east'])
        ax.set_ylim(self.bbox['south'], self.bbox['north'])
        # Plot the 16:9 bounding box outline
        bbox_rect = patches.Rectangle(
            (self.bbox['west'], self.bbox['south']),
            self.bbox['east'] - self.bbox['west'],
            self.bbox['north'] - self.bbox['south'],
            linewidth=3,
            edgecolor='red',
            facecolor='none',
            label='16:9 Capture Area'
        )
        ax.add_patch(bbox_rect)
        
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)
        ax.set_title(
            f"{self.city_name.upper()} Tile Grid\n"
            f"{len(self.tiles)} tiles ({self.tile_size_km}km each) | "
            f"{self.bbox['width_km']:.1f}×{self.bbox['height_km']:.1f}km (16:9)",
            fontsize=14,
            fontweight='bold'
        )
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
        
        # Apply aspect ratio correction for latitude/longitude distortion
        center_lat = self.bbox['center_lat']
        ax.set_aspect(1.0 / np.cos(np.radians(center_lat)))
        
        # Save
        output_file = self.output_dir / f"{self.city_name}_tile_grid.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"💾 Saved grid visualization to: {output_file}")
        plt.close()
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the tile grid.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'total_tiles': len(self.tiles),
            'grid_dimensions': f"{max(t['row'] for t in self.tiles) + 1} × {max(t['col'] for t in self.tiles) + 1}",
            'coverage_area_km2': len(self.tiles) * (self.tile_size_km ** 2),
            'data_sources': {}
        }
        
        # Count status for each data source
        data_sources = ['sentinel_2015', 'sentinel_2020', 'sentinel_2024',
                       'osm_buildings', 'topographic', 'osm_renders']
        
        for source in data_sources:
            stats['data_sources'][source] = {
                'pending': len(self.get_tiles_by_status(source, 'pending')),
                'processing': len(self.get_tiles_by_status(source, 'processing')),
                'complete': len(self.get_tiles_by_status(source, 'complete')),
                'failed': len(self.get_tiles_by_status(source, 'failed'))
            }
        
        return stats


def create_all_tile_grids(boundaries_file: str = './ml-pipeline/datasets/city_boundaries.json') -> Dict[str, TileGrid]:
    """
    Create tile grids for all cities from boundaries file.
    
    Args:
        boundaries_file: Path to city boundaries JSON
        
    Returns:
        Dictionary mapping city names to TileGrid objects
    """
    logger.info("=" * 60)
    logger.info("CREATING TILE GRIDS FOR ALL CITIES")
    logger.info("=" * 60)
    
    # Load boundaries
    with open(boundaries_file, 'r') as f:
        boundaries = json.load(f)
    
    tile_grids = {}
    
    for city_name, data in boundaries.items():
        logger.info(f"\n📐 Creating grid for {city_name.upper()}...")
        
        grid = TileGrid(
            city_name=city_name,
            bbox=data['master_bbox'],
            tile_size_km=2.0
        )
        
        # Save manifest
        grid.save_manifest()
        
        # Create visualization
        grid.visualize_grid()
        
        # Print statistics
        stats = grid.get_statistics()
        logger.info(f"✅ {city_name}: {stats['total_tiles']} tiles, {stats['coverage_area_km2']:.2f} km²")
        
        tile_grids[city_name] = grid
    
    logger.info("\n✅ All tile grids created successfully!")
    
    return tile_grids


if __name__ == "__main__":
    grids = create_all_tile_grids()
    print(f"\n✅ Created tile grids for {len(grids)} cities")
