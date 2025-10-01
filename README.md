# Perfect Closet - AI-Powered Body Type Classification

A clean, efficient web application that uses machine learning to classify women's body types and provide personalized clothing recommendations.

##  Features

-  **AI-Powered Body Type Classification**: Uses ResNet50 deep learning to classify 5 main body types
-  **Personalized Clothing Recommendations**: Get specific advice for tops, bottoms, dresses, and styling tips
-  **User-Friendly Web Interface**: Beautiful, responsive web app with drag-and-drop image upload
-  **Confidence Scoring**: Shows prediction confidence and alternative body type scores
-  **High Accuracy**: Uses transfer learning for robust classification
-  **Privacy-First**: Images processed locally, no data storage

##  Body Types Supported

1. **Hourglass** - Balanced proportions with defined waist
2. **Triangle (Pear)** - Hips wider than bust with defined waist  
3. **Apple** - Fuller midsection with less defined waist
4. **Rectangle** - Similar bust and hip measurements with less defined waist
5. **Inverted Triangle** - Bust wider than hips with broad shoulders

##  Technology Stack

- **Backend**: Python Flask
- **AI/ML**: PyTorch, ResNet50
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Image Processing**: PIL, torchvision
- **Dataset**: Style4BodyShape dataset

##  Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- 4GB+ RAM recommended
- GPU optional (for faster inference)

##  Quick Start

### 1. Clone or Download
```bash
git clone <repository-url>
cd my_perfect_closet
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Open Your Browser
Navigate to `http://localhost:5000`


##  Project Structure

```
my_perfect_closet/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   └── about.html
└── temp_dataset/        # The dataset (Style4BodyShape)
```

##  Usage Tips

### For Best Results:
-  Wear form-fitting clothing that shows your silhouette
-  Ensure your full body is visible in the photo
-  Use good lighting for clear image quality
-  Stand straight with arms at your sides
-  Take photo from a reasonable distance

### Avoid:
-  Baggy or loose clothing
-  Heavy coats or jackets
-  Poor lighting conditions
-  Selfies or close-up shots
-  Photos where body parts are cut off

##  Clothing Recommendations

The system provides comprehensive styling advice for each body type:

### Hourglass
- **Focus**: Emphasize the natural waist
- **Tops**: Fitted, wrap styles, V-necks
- **Bottoms**: High-waisted, A-line cuts

### Pear (Triangle)
- **Focus**: Balance upper and lower body
- **Tops**: Bright colors, patterns, structured shoulders
- **Bottoms**: Dark colors, straight cuts

### Apple  
- **Focus**: Create vertical lines, draw attention up/down
- **Tops**: V-necks, empire waist, flowy fabrics
- **Bottoms**: Straight-leg, bootcut styles

### Rectangle
- **Focus**: Create curves and define waist
- **Tops**: Peplum, ruffles, crop tops
- **Bottoms**: Low-rise, flared styles

### Inverted Triangle
- **Focus**: Balance broad shoulders with fuller hips
- **Tops**: Soft fabrics, avoid shoulder emphasis
- **Bottoms**: Wide-leg, bright colors, full skirts
