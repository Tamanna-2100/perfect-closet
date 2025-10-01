"""
Perfect Closet - AI-Powered Body Type Classification and Clothing Recommendations
Flask Web Application
"""

import os
import io
import base64
from PIL import Image
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import resnet50
import numpy as np
from flask import Flask, render_template, request, jsonify, redirect, url_for
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key-for-development')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')

# Body type classes
BODY_TYPES = ['Apple', 'Hourglass', 'Inverted Triangle', 'Rectangle', 'Triangle']

# Clothing recommendations database
CLOTHING_RECOMMENDATIONS = {
    'Apple': {
        'focus': 'Create vertical lines, draw attention up/down',
        'tops': [
            'V-neck tops and blouses',
            'Empire waist dresses',
            'Flowy fabrics that drape nicely',
            'Wrap tops',
            'Scoop necks',
            'Asymmetrical hemlines'
        ],
        'bottoms': [
            'Straight-leg jeans',
            'Bootcut pants',
            'High-waisted trousers',
            'A-line skirts',
            'Wide-leg pants',
            'Dark colored bottoms'
        ],
        'dresses': [
            'A-line dresses',
            'Wrap dresses',
            'Empire waist dresses',
            'Shift dresses',
            'Maxi dresses with defined waist'
        ],
        'avoid': [
            'Tight clothing around midsection',
            'Horizontal stripes',
            'Belts at natural waist',
            'Crop tops',
            'High-neck tops'
        ],
        'styling_tips': [
            'Use accessories to draw attention to face and legs',
            'Layer with open cardigans or blazers',
            'Choose fabrics that flow over curves',
            'Wear statement necklaces',
            'Choose darker colors for midsection'
        ]
    },
    'Hourglass': {
        'focus': 'Emphasize the natural waist',
        'tops': [
            'Fitted tops',
            'Wrap style blouses',
            'V-neck sweaters',
            'Button-down shirts (fitted)',
            'Peplum tops',
            'Cowl necks'
        ],
        'bottoms': [
            'High-waisted jeans',
            'Pencil skirts',
            'A-line skirts',
            'Fitted straight-leg pants',
            'Bodycon skirts',
            'High-waisted shorts'
        ],
        'dresses': [
            'Bodycon dresses',
            'Wrap dresses',
            'Fit-and-flare dresses',
            'Sheath dresses',
            'Mermaid style dresses'
        ],
        'avoid': [
            'Loose, shapeless clothing',
            'Boxy cuts',
            'Drop-waist styles',
            'Oversized tops',
            'Baggy jeans'
        ],
        'styling_tips': [
            'Always define your waist with belts',
            'Choose fitted clothing that shows your silhouette',
            'Tuck in tops to emphasize waist',
            'Wear clothes that hug your curves',
            'Use belts as statement accessories'
        ]
    },
    'Triangle': {  # Pear shape
        'focus': 'Balance upper and lower body',
        'tops': [
            'Bright colored tops',
            'Horizontal stripes on top',
            'Boat neck tops',
            'Off-shoulder styles',
            'Structured shoulder tops',
            'Statement sleeves'
        ],
        'bottoms': [
            'Dark colored bottoms',
            'Straight-cut jeans',
            'Bootcut pants',
            'Wide-leg trousers',
            'A-line skirts in dark colors',
            'High-waisted styles'
        ],
        'dresses': [
            'A-line dresses',
            'Fit-and-flare dresses',
            'Empire waist dresses',
            'Dresses with embellished tops',
            'Wrap dresses'
        ],
        'avoid': [
            'Hip-emphasizing details',
            'Tight-fitting bottoms',
            'Horizontal stripes on bottom',
            'Pockets on hips',
            'Light colored bottoms'
        ],
        'styling_tips': [
            'Add volume to your upper body',
            'Use statement jewelry near face',
            'Choose tops with interesting details',
            'Wear structured blazers',
            'Use scarves to add volume up top'
        ]
    },
    'Rectangle': {
        'focus': 'Create curves and define waist',
        'tops': [
            'Peplum tops',
            'Ruffle details',
            'Crop tops',
            'Wrap tops',
            'Tops with horizontal stripes',
            'Layered looks'
        ],
        'bottoms': [
            'Low-rise jeans',
            'Flared pants',
            'Skinny jeans with interesting details',
            'Pleated skirts',
            'Ruffled skirts',
            'Patterned bottoms'
        ],
        'dresses': [
            'Fit-and-flare dresses',
            'Wrap dresses',
            'Dresses with ruffles',
            'Tiered dresses',
            'Belted dresses'
        ],
        'avoid': [
            'Straight, boxy cuts',
            'Shapeless clothing',
            'Long, straight dresses',
            'Oversized tops without definition'
        ],
        'styling_tips': [
            'Use belts to create a waist',
            'Layer clothing for dimension',
            'Add curves with ruffles and details',
            'Choose fitted clothing',
            'Experiment with different textures'
        ]
    },
    'Inverted Triangle': {
        'focus': 'Balance broad shoulders with fuller hips',
        'tops': [
            'Soft fabric tops',
            'V-neck styles',
            'Scoop necks',
            'Wrap tops',
            'Flowy blouses',
            'Avoid shoulder emphasis'
        ],
        'bottoms': [
            'Wide-leg pants',
            'Bright colored bottoms',
            'Bootcut jeans',
            'Full skirts',
            'Flared styles',
            'Patterned bottoms'
        ],
        'dresses': [
            'A-line dresses',
            'Fit-and-flare dresses',
            'Dresses with full skirts',
            'Empire waist dresses',
            'Wrap dresses'
        ],
        'avoid': [
            'Shoulder pads',
            'Tight tops',
            'Horizontal stripes on top',
            'Boat necks',
            'Cap sleeves'
        ],
        'styling_tips': [
            'Add volume to lower body',
            'Choose soft, flowing fabrics for tops',
            'Wear statement accessories on lower body',
            'Use darker colors on top',
            'Create vertical lines'
        ]
    }
}

class BodyTypeClassifier:
    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._load_model(model_path)
        self.transform = self._get_transforms()
        
    def _load_model(self, model_path):
        """Load the trained ResNet50 model"""
        model = resnet50(pretrained=True)
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, len(BODY_TYPES))
        
        if model_path and os.path.exists(model_path):
            try:
                model.load_state_dict(torch.load(model_path, map_location=self.device))
                logger.info(f"Loaded model from {model_path}")
            except Exception as e:
                logger.warning(f"Could not load model from {model_path}: {e}")
                logger.info("Using pretrained ResNet50 with random final layer")
        else:
            logger.info("Using pretrained ResNet50 with random final layer")
            
        model.eval()
        model.to(self.device)
        return model
    
    def _get_transforms(self):
        """Get image preprocessing transforms"""
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    def predict(self, image):
        """Predict body type from image"""
        try:
            # Preprocess image
            if isinstance(image, str):
                # If image is base64 string
                image_data = base64.b64decode(image.split(',')[1])
                image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Apply transforms
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_class].item()
                
                # Get all class probabilities
                all_probs = {}
                for i, body_type in enumerate(BODY_TYPES):
                    all_probs[body_type] = probabilities[0][i].item()
            
            return {
                'predicted_class': BODY_TYPES[predicted_class],
                'confidence': confidence,
                'all_probabilities': all_probs
            }
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return {
                'predicted_class': 'Rectangle',  # Default
                'confidence': 0.2,
                'all_probabilities': {bt: 0.2 for bt in BODY_TYPES}
            }

# Initialize the classifier
classifier = BodyTypeClassifier()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    """Handle image classification"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Read and process image
        image = Image.open(file.stream)
        
        # Get prediction
        result = classifier.predict(image)
        
        # Get clothing recommendations
        body_type = result['predicted_class']
        recommendations = CLOTHING_RECOMMENDATIONS.get(body_type, {})
        
        return jsonify({
            'success': True,
            'body_type': body_type,
            'confidence': round(result['confidence'] * 100, 1),
            'all_probabilities': {k: round(v * 100, 1) for k, v in result['all_probabilities'].items()},
            'recommendations': recommendations
        })
        
    except Exception as e:
        logger.error(f"Error in classification: {e}")
        return jsonify({'error': 'Failed to process image'}), 500

@app.route('/recommendations/<body_type>')
def recommendations(body_type):
    """Get recommendations for a specific body type"""
    if body_type not in BODY_TYPES:
        return jsonify({'error': 'Invalid body type'}), 400
    
    return jsonify({
        'body_type': body_type,
        'recommendations': CLOTHING_RECOMMENDATIONS.get(body_type, {})
    })

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html', body_types=BODY_TYPES)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Get port from environment variable (for deployment) or use 5000 for local
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port)