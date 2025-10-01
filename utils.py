"""
Utility functions for data preprocessing and model inference
"""

import os
import json
import torch
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import torchvision.transforms as transforms
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ImagePreprocessor:
    """Handle image preprocessing for body type classification"""
    
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def enhance_image(self, image: Image.Image) -> Image.Image:
        """Apply image enhancements for better classification"""
        # Auto-orient based on EXIF data
        image = ImageOps.exif_transpose(image)
        
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        # Enhance sharpness slightly
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        return image
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """Preprocess image for model inference"""
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply enhancements
        image = self.enhance_image(image)
        
        # Apply transforms
        tensor = self.transform(image)
        
        return tensor.unsqueeze(0)  # Add batch dimension

class ModelManager:
    """Manage model loading and inference"""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.body_types = ['Apple', 'Hourglass', 'Inverted Triangle', 'Rectangle', 'Triangle']
        self.model = None
        self.preprocessor = ImagePreprocessor()
    
    def load_model(self) -> torch.nn.Module:
        """Load the trained model"""
        from torchvision.models import resnet50
        import torch.nn as nn
        
        model = resnet50(pretrained=True)
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, len(self.body_types))
        
        if self.model_path and os.path.exists(self.model_path):
            try:
                model.load_state_dict(torch.load(self.model_path, map_location=self.device))
                logger.info(f"Loaded model from {self.model_path}")
            except Exception as e:
                logger.warning(f"Could not load model: {e}")
        
        model.eval()
        model.to(self.device)
        self.model = model
        return model
    
    def predict(self, image: Image.Image) -> Dict:
        """Make prediction on image"""
        if self.model is None:
            self.load_model()
        
        # Preprocess image
        image_tensor = self.preprocessor.preprocess_image(image).to(self.device)
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
            
            # Get all class probabilities
            all_probs = {}
            for i, body_type in enumerate(self.body_types):
                all_probs[body_type] = probabilities[0][i].item()
        
        return {
            'predicted_class': self.body_types[predicted_class],
            'confidence': confidence,
            'all_probabilities': all_probs
        }

class RecommendationEngine:
    """Handle clothing recommendations based on body type"""
    
    def __init__(self, recommendations_file: Optional[str] = None):
        self.recommendations = self._load_recommendations(recommendations_file)
    
    def _load_recommendations(self, file_path: Optional[str]) -> Dict:
        """Load recommendations from file or use default"""
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load recommendations from {file_path}: {e}")
        
        # Default recommendations (same as in app.py)
        return {
            'Apple': {
                'focus': 'Create vertical lines, draw attention up/down',
                'tops': [
                    'V-neck tops and blouses',
                    'Empire waist dresses',
                    'Flowy fabrics that drape nicely',
                    'Wrap tops',
                    'Scoop necks'
                ],
                'bottoms': [
                    'Straight-leg jeans',
                    'Bootcut pants',
                    'High-waisted trousers',
                    'A-line skirts',
                    'Wide-leg pants'
                ],
                'avoid': [
                    'Tight clothing around midsection',
                    'Horizontal stripes',
                    'Belts at natural waist'
                ]
            }
            # ... (continue with other body types)
        }
    
    def get_recommendations(self, body_type: str, confidence: float = 1.0) -> Dict:
        """Get recommendations for a body type"""
        recommendations = self.recommendations.get(body_type, {})
        
        # Add confidence-based modifications
        if confidence < 0.7:
            recommendations['note'] = (
                "Low confidence prediction. Consider trying recommendations "
                "for similar body types as well."
            )
        
        return recommendations

class DataValidator:
    """Validate and clean dataset"""
    
    @staticmethod
    def validate_image(image_path: str) -> bool:
        """Check if image is valid"""
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_image_info(image_path: str) -> Dict:
        """Get image information"""
        try:
            with Image.open(image_path) as img:
                return {
                    'size': img.size,
                    'mode': img.mode,
                    'format': img.format,
                    'valid': True
                }
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    @staticmethod
    def clean_dataset(data_dir: str) -> Dict:
        """Clean and validate dataset"""
        stats = {
            'total_images': 0,
            'valid_images': 0,
            'invalid_images': [],
            'body_type_counts': {}
        }
        
        body_types = ['Apple', 'Hourglass', 'Inverted Triangle', 'Rectangle', 'Triangle']
        
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    stats['total_images'] += 1
                    
                    if DataValidator.validate_image(file_path):
                        stats['valid_images'] += 1
                        
                        # Try to determine body type from path
                        for body_type in body_types:
                            if body_type.lower() in file.lower() or body_type.lower() in root.lower():
                                stats['body_type_counts'][body_type] = stats['body_type_counts'].get(body_type, 0) + 1
                                break
                    else:
                        stats['invalid_images'].append(file_path)
        
        return stats

def setup_directories():
    """Create necessary directories"""
    dirs = [
        'models',
        'static/uploads',
        'logs'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")

def main():
    """Main utility function"""
    setup_directories()
    
    # Validate dataset if exists
    if os.path.exists('temp_dataset'):
        stats = DataValidator.clean_dataset('temp_dataset')
        print("Dataset Statistics:")
        print(f"Total images: {stats['total_images']}")
        print(f"Valid images: {stats['valid_images']}")
        print(f"Body type distribution: {stats['body_type_counts']}")
        
        if stats['invalid_images']:
            print(f"Invalid images found: {len(stats['invalid_images'])}")

if __name__ == "__main__":
    main()