"""Google Gemini 2.5 Flash Service for Pixel-Precise Image Editing"""

import asyncio
import base64
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from PIL import Image

try:
    import google.generativeai as genai
except ImportError:
    genai = None

import logging
logger = logging.getLogger(__name__)


class GeminiFlashService:
    """
    Google Gemini 2.5 Flash (NanoBanana) integration
    Supports pixel-precise regional image editing
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini Flash service
        
        Args:
            api_key: Gemini API key (if None, reads from environment)
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not provided")
        
        if genai is None:
            raise ImportError("google-generativeai package not installed")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.model = genai.GenerativeModel(self.model_name)
        
        # Cost tracking
        self.total_cost = 0.0
        self.request_count = 0
        self.cost_per_request = 0.039  # USD (Gemini 2.5 Flash pricing)
        
        logger.info(f"Initialized Gemini Flash service with model: {self.model_name}")
    
    async def edit_image(
        self,
        source_image_path: str,
        prompt: str,
        edit_regions: List[Dict],
        reference_image_path: Optional[str] = None,
        output_dir: str = "outputs/scenarios",
    ) -> Dict:
        """
        Edit specific regions of satellite image using Gemini 2.5 Flash
        
        Args:
            source_image_path: Path to source city tile
            prompt: Detailed editing instructions with pixel coordinates
            edit_regions: List of {x1, y1, x2, y2, action, spec}
            reference_image_path: Optional reference city image
            output_dir: Directory to save generated images
        
        Returns:
            {
                'image_path': path to generated image,
                'cost': API cost in USD,
                'generation_time': seconds,
                'status': 'success'|'failed',
                'error': error message if failed
            }
        """
        logger.info(f"Starting image editing for: {source_image_path}")
        logger.info(f"Edit regions: {len(edit_regions)}")
        
        start_time = time.time()
        
        try:
            # Load source image
            source_image = Image.open(source_image_path)
            logger.info(f"Loaded source image: {source_image.size}")
            
            # Prepare inputs
            inputs = [prompt, source_image]
            
            # Add reference image if provided
            if reference_image_path and os.path.exists(reference_image_path):
                reference_image = Image.open(reference_image_path)
                logger.info(f"Loaded reference image: {reference_image.size}")
                
                # Enhanced prompt with reference
                enhanced_prompt = f"{prompt}\n\nReference image: Extract architectural style, color palette, and urban design features from this reference city to apply to the source image."
                inputs = [enhanced_prompt, source_image, reference_image]
            
            # Configure generation
            generation_config = genai.GenerationConfig(
                temperature=0.4,  # Lower for consistency
                candidate_count=1,
                max_output_tokens=2048,
            )
            
            # Call Gemini API (async wrapper for sync method)
            logger.info("Calling Gemini API...")
            response = await asyncio.to_thread(
                self.model.generate_content,
                inputs,
                generation_config=generation_config,
            )
            
            # Extract generated image
            if not response.candidates or not response.candidates[0].content.parts:
                raise ValueError("No image generated in response")
            
            # Get image data from response
            generated_image_data = self._extract_image_data(response)
            
            # Save generated image
            output_path = self._save_generated_image(generated_image_data, output_dir)
            logger.info(f"Saved generated image to: {output_path}")
            
            # Update cost tracking
            cost = self.cost_per_request
            self.total_cost += cost
            self.request_count += 1
            
            generation_time = time.time() - start_time
            
            logger.info(f"Image generation completed in {generation_time:.2f}s, cost: ${cost}")
            
            return {
                'image_path': output_path,
                'cost': cost,
                'generation_time': generation_time,
                'status': 'success',
                'model': self.model_name,
            }
        
        except Exception as e:
            logger.exception(f"Gemini API error: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'generation_time': time.time() - start_time,
            }
    
    def _extract_image_data(self, response) -> bytes:
        """Extract image bytes from Gemini response"""
        try:
            # Try to get inline data
            part = response.candidates[0].content.parts[0]
            if hasattr(part, 'inline_data') and part.inline_data:
                return part.inline_data.data
            
            # Try to get as blob
            if hasattr(part, 'blob') and part.blob:
                return part.blob.data
            
            raise ValueError("No image data found in response")
        
        except Exception as e:
            logger.error(f"Failed to extract image data: {e}")
            raise
    
    def _save_generated_image(self, image_data: bytes, output_dir: str) -> str:
        """
        Save generated image and return path
        
        Args:
            image_data: Image bytes (could be base64 or raw)
            output_dir: Output directory
        
        Returns:
            Path to saved image
        """
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}.png"
        file_path = output_path / filename
        
        # Try to decode if base64
        try:
            decoded_data = base64.b64decode(image_data)
            image_data = decoded_data
        except Exception:
            # Not base64, use as is
            pass
        
        # Save image
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        return str(file_path)
    
    async def edit_image_with_retry(
        self,
        source_image_path: str,
        prompt: str,
        edit_regions: List[Dict],
        reference_image_path: Optional[str] = None,
        max_retries: int = 3,
    ) -> Dict:
        """
        Edit image with exponential backoff retry logic
        
        Args:
            source_image_path: Path to source image
            prompt: Editing prompt
            edit_regions: Edit region specifications
            reference_image_path: Optional reference image
            max_retries: Maximum retry attempts
        
        Returns:
            Result dictionary
        """
        for attempt in range(max_retries):
            result = await self.edit_image(
                source_image_path,
                prompt,
                edit_regions,
                reference_image_path,
            )
            
            if result['status'] == 'success':
                return result
            
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)
        
        return result
    
    def get_cost_summary(self) -> Dict:
        """Get cost tracking summary"""
        return {
            'total_cost_usd': round(self.total_cost, 2),
            'request_count': self.request_count,
            'average_cost_per_request': round(self.total_cost / max(self.request_count, 1), 4),
        }
    
    def reset_cost_tracking(self):
        """Reset cost tracking counters"""
        self.total_cost = 0.0
        self.request_count = 0
        logger.info("Cost tracking reset")


# Example usage
if __name__ == "__main__":
    async def test_gemini_service():
        """Test Gemini service"""
        service = GeminiFlashService()
        
        # Test prompt
        prompt = """
        Transform this urban satellite image with the following edits:
        
        EDIT REGION 1 [pixels x:1200-1400, y:800-1100]:
        - Add 4-story residential building
        - Modern sustainable architecture with green roof
        - Light gray facade with large windows
        
        EDIT REGION 2 [pixels x:900-1100, y:1050-1200]:
        - Create pocket park with 15 trees
        - Add pedestrian paths and benches
        
        Style: Satellite aerial view, maintain photorealistic quality
        """
        
        # Test (would need actual image file)
        # result = await service.edit_image(
        #     "test_image.jpg",
        #     prompt,
        #     edit_regions=[
        #         {'x1': 1200, 'y1': 800, 'x2': 1400, 'y2': 1100},
        #         {'x1': 900, 'y1': 1050, 'x2': 1100, 'y2': 1200},
        #     ]
        # )
        
        print("Gemini service initialized successfully")
        print(service.get_cost_summary())
    
    asyncio.run(test_gemini_service())
