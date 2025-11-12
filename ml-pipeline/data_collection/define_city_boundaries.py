"""
City Boundary Definer Module

This module establishes official city boundaries and expansion zones using OpenStreetMap data.
It's the foundation for the entire data collection pipeline.

Author: Amine Mayoufi & Walaa Hidaya
Date: November 9, 2025
"""

import logging
import json
from pathlib import Path
from typing import Dict, Optional, Tuple
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon, box
import matplotlib.pyplot as plt
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CityBoundaryDefiner:
    """
    Defines city boundaries and expansion zones for urban data collection.
    
    Uses OpenStreetMap administrative boundaries with fallback to predefined boxes.
    Creates expansion zones around cities to capture future growth areas.
    """
    
    # Predefined bounding boxes (fallback if OSM query fails)
    FALLBACK_BBOXES = {
        'tunis': {'west': 10.05, 'south': 36.65, 'east': 10.35, 'north': 36.95},
        'shenzhen': {'west': 113.75, 'south': 22.35, 'east': 114.65, 'north': 22.85},
        'copenhagen': {'west': 12.45, 'south': 55.58, 'east': 12.70, 'north': 55.78},
        'phoenix': {'west': -112.35, 'south': 33.25, 'east': -111.85, 'north': 33.75}
    }
    
    # City configurations - expansion_buffer defines MINIMUM clearance from city edges
    # Creates 16:9 box with city centered and minimum clearance on all sides
    CITY_CONFIGS = {
        'tunis': {
            'country_code': 'TN',
            'expansion_buffer_km': 15,  # Min 15km clearance → ~40-50km box
            'description': 'Mediterranean developing city',
            'osm_query': 'Grand Tunis, Tunisia',  # Specific metropolitan area
            'relation_id': None  # Will use query
        },
        'shenzhen': {
            'country_code': 'CN',
            'expansion_buffer_km': 20,  # Min 20km clearance → ~140-180km box (huge city)
            'description': 'Rapid growth megacity',
            'osm_query': 'Shenzhen, Guangdong, China',
            'relation_id': None
        },
        'copenhagen': {
            'country_code': 'DK',
            'expansion_buffer_km': 8,  # Min 8km clearance (5+3km added)
            'description': 'Sustainable European model',
            'osm_query': 'Copenhagen Municipality, Denmark',  # Use municipality
            'relation_id': None,
            'center_offset_km': {'east': -5, 'north': 0}  # Shift 5km west (away from water on east)
        },
        'phoenix': {
            'country_code': 'US',
            'expansion_buffer_km': 15,  # Min 15km clearance → ~80-100km box (sprawling)
            'description': 'Desert sprawl city',
            'osm_query': 'Phoenix, Arizona, USA',
            'relation_id': None
        }
    }
    
    def __init__(self, output_dir: str = './ml-pipeline/datasets'):
        """
        Initialize the CityBoundaryDefiner.
        
        Args:
            output_dir: Directory to save boundary configurations
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized CityBoundaryDefiner with output dir: {self.output_dir}")
    
    def get_official_boundary(self, city_name: str, country_code: str, osm_query: str = None) -> Optional[Polygon]:
        """
        Download official city boundary from OpenStreetMap.
        
        Args:
            city_name: Name of the city
            country_code: ISO country code (e.g., 'TN', 'CN')
            osm_query: Specific OSM query string (if None, uses city_name, country_code)
            
        Returns:
            Shapely Polygon of city boundary or None if not found
        """
        try:
            # Use specific query if provided, otherwise default
            query = osm_query if osm_query else f"{city_name}, {country_code}"
            logger.info(f"Querying OSM for {city_name}: '{query}'")
            
            gdf = ox.geocode_to_gdf(query)
            
            if gdf is None or len(gdf) == 0:
                logger.warning(f"No boundary found for {city_name}")
                return None
            
            geometry = gdf.iloc[0]['geometry']
            
            # Calculate area (approximate)
            area_km2 = geometry.area * (111 * 111)  # degrees² to km²
            logger.info(f"Found boundary for {city_name}: {area_km2:.2f} km²")
            
            return geometry
            
        except Exception as e:
            logger.error(f"Failed to get boundary for {city_name}: {e}")
            return None
    
    def create_expansion_zone(self, boundary: Polygon, buffer_km: float) -> Polygon:
        """
        Create expansion zone by buffering the boundary.
        
        Args:
            boundary: City boundary polygon
            buffer_km: Buffer distance in kilometers
            
        Returns:
            Expanded polygon representing potential growth zone
        """
        # Convert km to degrees (approximate)
        buffer_degrees = buffer_km / 111.0
        
        logger.info(f"Creating expansion zone with {buffer_km}km buffer")
        expansion_zone = boundary.buffer(buffer_degrees)
        
        return expansion_zone
    
    def calculate_master_bbox(self, geometry: Polygon, min_clearance_km: float, center_offset_km: Dict = None) -> Dict:
        """
        Calculate master bounding box with 16:9 aspect ratio centered on city.
        Ensures city is properly centered with minimum clearance on all sides.
        
        Strategy:
        1. Find city center and dimensions
        2. Add minimum clearance (e.g., 15km) to all sides
        3. Adjust to 16:9 aspect ratio while maintaining minimum clearance
        4. Result: City perfectly centered with equal margins
        
        Args:
            geometry: City boundary polygon
            min_clearance_km: Minimum distance from city edge to box edge (e.g., 15km)
            center_offset_km: Optional offset for center point (dict with 'east', 'north' keys in km)
            
        Returns:
            Dictionary with bbox coordinates and metadata
        """
        # Get city bounds and center
        bounds = geometry.bounds  # (minx, miny, maxx, maxy)
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2
        center_lat_rad = np.radians(center_lat)
        
        # Conversion factors
        lon_km_per_degree = 111.0 * np.cos(center_lat_rad)
        lat_km_per_degree = 111.0
        
        # Apply center offset if provided
        if center_offset_km:
            offset_lon = center_offset_km.get('east', 0) / lon_km_per_degree
            offset_lat = center_offset_km.get('north', 0) / lat_km_per_degree
            center_lon += offset_lon
            center_lat += offset_lat
            logger.info(f"   Center offset applied: {center_offset_km.get('east', 0):.1f}km east, {center_offset_km.get('north', 0):.1f}km north")
        
        # Calculate actual city dimensions in km
        city_width_km = (bounds[2] - bounds[0]) * lon_km_per_degree
        city_height_km = (bounds[3] - bounds[1]) * lat_km_per_degree
        
        logger.info(f"   City dimensions: {city_width_km:.2f}km × {city_height_km:.2f}km")
        
        # Add minimum clearance to both sides (2x for total dimension)
        min_box_width_km = city_width_km + (2 * min_clearance_km)
        min_box_height_km = city_height_km + (2 * min_clearance_km)
        
        # Target aspect ratio: 16:9
        target_aspect = 16.0 / 9.0
        
        # Adjust to 16:9 while maintaining minimum clearance
        # Expand the dimension that's too small for the aspect ratio
        if min_box_width_km / min_box_height_km > target_aspect:
            # Width is relatively larger, increase height to match aspect
            final_width_km = min_box_width_km
            final_height_km = final_width_km / target_aspect
        else:
            # Height is relatively larger, increase width to match aspect
            final_height_km = min_box_height_km
            final_width_km = final_height_km * target_aspect
        
        # Calculate actual clearance achieved (will be >= min_clearance_km)
        actual_clearance_width = (final_width_km - city_width_km) / 2
        actual_clearance_height = (final_height_km - city_height_km) / 2
        
        # Convert to degrees (centered on city center)
        half_width_deg = (final_width_km / 2.0) / lon_km_per_degree
        half_height_deg = (final_height_km / 2.0) / lat_km_per_degree
        
        bbox = {
            'west': center_lon - half_width_deg,
            'south': center_lat - half_height_deg,
            'east': center_lon + half_width_deg,
            'north': center_lat + half_height_deg,
            'center_lat': center_lat,
            'center_lon': center_lon,
            'width_km': round(final_width_km, 2),
            'height_km': round(final_height_km, 2),
            'clearance_width_km': round(actual_clearance_width, 2),
            'clearance_height_km': round(actual_clearance_height, 2)
        }
        
        logger.info(f"Master bbox: {final_width_km:.2f}km × {final_height_km:.2f}km (16:9 aspect ratio)")
        logger.info(f"   Centered on city at ({center_lat:.4f}, {center_lon:.4f})")
        logger.info(f"   Clearance: {actual_clearance_width:.2f}km (width), {actual_clearance_height:.2f}km (height)")
        logger.info(f"   Minimum clearance achieved: {min(actual_clearance_width, actual_clearance_height):.2f}km")
        
        return bbox
    
    def validate_bbox(self, bbox: Dict) -> bool:
        """
        Validate bounding box coordinates.
        
        Args:
            bbox: Bounding box dictionary
            
        Returns:
            True if valid, False otherwise
        """
        if bbox['west'] >= bbox['east']:
            logger.error("Invalid bbox: west >= east")
            return False
        
        if bbox['south'] >= bbox['north']:
            logger.error("Invalid bbox: south >= north")
            return False
        
        if not (-180 <= bbox['west'] <= 180 and -180 <= bbox['east'] <= 180):
            logger.error("Invalid longitude values")
            return False
        
        if not (-90 <= bbox['south'] <= 90 and -90 <= bbox['north'] <= 90):
            logger.error("Invalid latitude values")
            return False
        
        return True
    
    def process_all_cities(self) -> Dict:
        """
        Process all cities and create boundary definitions.
        
        Returns:
            Dictionary with all city boundary data
        """
        logger.info("=" * 60)
        logger.info("PROCESSING ALL CITY BOUNDARIES")
        logger.info("=" * 60)
        
        all_boundaries = {}
        
        for city_name, config in self.CITY_CONFIGS.items():
            logger.info(f"\n📍 Processing {city_name.upper()}...")
            
            # Try to get official boundary with specific OSM query
            boundary = self.get_official_boundary(
                city_name, 
                config['country_code'],
                config.get('osm_query')  # Use specific query if provided
            )
            
            # Fallback to predefined bbox if needed
            if boundary is None:
                logger.warning(f"Using fallback bbox for {city_name}")
                fallback = self.FALLBACK_BBOXES[city_name]
                boundary = box(
                    fallback['west'], fallback['south'],
                    fallback['east'], fallback['north']
                )
            
            # Calculate master bbox centered on the TRUE city boundary
            # The expansion_buffer_km defines how large the capture area should be
            # NO expansion zone - we use the original city boundary to find center
            master_bbox = self.calculate_master_bbox(
                boundary,  # Use original city boundary for center calculation
                config['expansion_buffer_km'],  # Pass buffer to define box size
                config.get('center_offset_km')  # Optional center offset (e.g., shift east to avoid water)
            )
            
            # Validate
            if not self.validate_bbox(master_bbox):
                logger.error(f"Invalid bbox for {city_name}, skipping")
                continue
            
            # Store results - keep original city boundary for model training
            all_boundaries[city_name] = {
                'official_boundary': boundary.__geo_interface__,  # Original city for ML masks
                'master_bbox': master_bbox,  # Large 16:9 capture area
                'config': config,
                'capture_area_km2': round(master_bbox['width_km'] * master_bbox['height_km'], 2),
                'city_area_km2': round(boundary.area * (111 * 111), 2)
            }
            
            logger.info(f"✅ {city_name}: {master_bbox['width_km']}×{master_bbox['height_km']} km")
        
        # Save to file
        output_file = self.output_dir / 'city_boundaries.json'
        with open(output_file, 'w') as f:
            json.dump(all_boundaries, f, indent=2)
        
        logger.info(f"\n💾 Saved boundaries to: {output_file}")
        
        # Create visualization
        self.visualize_boundaries(all_boundaries)
        
        return all_boundaries
    
    def visualize_boundaries(self, boundaries: Dict) -> None:
        """
        Create visualization of all city boundaries.
        
        Args:
            boundaries: Dictionary of city boundary data
        """
        logger.info("Creating boundary visualization...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()
        
        for idx, (city_name, data) in enumerate(boundaries.items()):
            ax = axes[idx]
            
            # Plot master bbox (16:9 capture area)
            bbox = data['master_bbox']
            bbox_geom = box(bbox['west'], bbox['south'], bbox['east'], bbox['north'])
            bbox_series = gpd.GeoSeries([bbox_geom])
            bbox_series.plot(ax=ax, facecolor='lightblue', edgecolor='blue', alpha=0.3, linewidth=2)
            
            # Plot official city boundary (for ML mask)
            from shapely.geometry import shape
            boundary_geom = shape(data['official_boundary']) if isinstance(data['official_boundary'], dict) else data['official_boundary']
            boundary = gpd.GeoSeries([boundary_geom])
            boundary.plot(ax=ax, facecolor='lightcoral', edgecolor='red', linewidth=2, alpha=0.5)
            
            # Add labels
            ax.set_xlim(bbox['west'], bbox['east'])
            ax.set_ylim(bbox['south'], bbox['north'])
            
            # Calculate proper aspect ratio to display 16:9 box correctly
            # Need to account for latitude: 1 degree lon != 1 degree lat in km
            center_lat = bbox['center_lat']
            lat_km_per_deg = 111.0
            lon_km_per_deg = 111.0 * np.cos(np.radians(center_lat))
            
            # Degrees span in each direction
            deg_width = bbox['east'] - bbox['west']
            deg_height = bbox['north'] - bbox['south']
            
            # We need: displayed_width / displayed_height = km_width / km_height = 16/9
            # matplotlib plots: x_pixels = deg_lon * scale, y_pixels = deg_lat * scale
            # To make it display as 16:9, we adjust the axis aspect
            # The correct aspect is: lon_km_per_deg / lat_km_per_deg
            # This makes 1 degree lon display same physical size as 1 degree lat
            ax.set_aspect(1.0 / np.cos(np.radians(center_lat)))
            
            ax.set_title(
                f"{city_name.upper()}\nCapture: {bbox['width_km']}×{bbox['height_km']} km (16:9)\nCity: {data['city_area_km2']:.0f} km²",
                fontsize=12,
                fontweight='bold'
            )
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            
            # Add legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor='lightblue', edgecolor='blue', label='Capture Area (16:9)', linewidth=2),
                Patch(facecolor='lightcoral', edgecolor='red', label='City Boundary (ML mask)', linewidth=2)
            ]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
        
        plt.suptitle('Urban Evolution AI - City Capture Areas (16:9) with City Boundaries', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save
        output_file = self.output_dir / 'city_boundaries_map.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"💾 Saved visualization to: {output_file}")
        plt.close()


if __name__ == "__main__":
    definer = CityBoundaryDefiner()
    boundaries = definer.process_all_cities()
    print("\n✅ City boundaries defined and saved!")
