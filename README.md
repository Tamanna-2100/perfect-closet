# Perfect Closet - AI-Powered Body Type Classification

A clean, efficient web application that uses machine learning to classify women's body types and provide personalized clothing recommendations.

## 🌟 Features

- 🤖 **AI-Powered Body Type Classification**: Uses ResNet50 deep learning to classify 5 main body types
- 👗 **Personalized Clothing Recommendations**: Get specific advice for tops, bottoms, dresses, and styling tips
- 🌐 **User-Friendly Web Interface**: Beautiful, responsive web app with drag-and-drop image upload
- 📊 **Confidence Scoring**: Shows prediction confidence and alternative body type scores
- 🎯 **High Accuracy**: Uses transfer learning for robust classification
- 🔒 **Privacy-First**: Images processed locally, no data storage

## 🚀 Body Types Supported

1. **Hourglass** - Balanced proportions with defined waist
2. **Triangle (Pear)** - Hips wider than bust with defined waist  
3. **Apple** - Fuller midsection with less defined waist
4. **Rectangle** - Similar bust and hip measurements with less defined waist
5. **Inverted Triangle** - Bust wider than hips with broad shoulders

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **AI/ML**: PyTorch, ResNet50
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Image Processing**: PIL, torchvision
- **Dataset**: Style4BodyShape dataset

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- 4GB+ RAM recommended
- GPU optional (for faster inference)

## ⚡ Quick Start

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

## 🏋️ Training Your Own Model

If you want to train the model on your own dataset:

### 1. Prepare Your Dataset
Organize your images in this structure:
```
dataset/
├── Apple/
│   ├── image1.jpg
│   └── image2.jpg
├── Hourglass/
├── Triangle/
├── Rectangle/
└── Inverted Triangle/
```

### 2. Update Training Script
Edit `train_model.py` and update the `data_dir` path:
```python
data_dir = "path/to/your/dataset"
```

### 3. Train the Model
```bash
python train_model.py
```

The trained model will be saved to `models/body_type_classifier.pth`

## 📁 Project Structure

```
my_perfect_closet/
├── app.py                 # Main Flask application
├── train_model.py         # Model training script
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   └── about.html
├── static/              # Static files
│   └── uploads/         # Uploaded images (temporary)
├── models/              # Trained models (created after training)
└── temp_dataset/        # Your dataset (Style4BodyShape)
```

## 💡 Usage Tips

### For Best Results:
- ✅ Wear form-fitting clothing that shows your silhouette
- ✅ Ensure your full body is visible in the photo
- ✅ Use good lighting for clear image quality
- ✅ Stand straight with arms at your sides
- ✅ Take photo from a reasonable distance

### Avoid:
- ❌ Baggy or loose clothing
- ❌ Heavy coats or jackets
- ❌ Poor lighting conditions
- ❌ Selfies or close-up shots
- ❌ Photos where body parts are cut off

## 🎨 Clothing Recommendations

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

## ⚙️ Configuration

### Environment Variables
Create a `.env` file for configuration:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216  # 16MB
MODEL_PATH=models/body_type_classifier.pth
```

### Model Configuration
Update `app.py` to customize:
- Model architecture
- Confidence thresholds
- Image preprocessing
- Recommendation rules

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔧 Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all requirements are installed
2. **CUDA Issues**: Set `torch.device('cpu')` if no GPU
3. **Memory Issues**: Reduce batch size in training
4. **Permission Errors**: Check file permissions for upload directory

### Performance Optimization:

1. **GPU Acceleration**: Install CUDA-compatible PyTorch
2. **Model Optimization**: Use TorchScript for deployment
3. **Image Caching**: Implement Redis for repeated predictions
4. **Load Balancing**: Use multiple Gunicorn workers

## 📚 Dataset Information

This project uses the Style4BodyShape dataset:
- 270 women in various outfits
- 5 body type categories
- Form-fitting clothing for accurate classification
- Professional annotation and quality control

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Style4BodyShape dataset creators
- PyTorch and torchvision teams
- Flask framework developers
- Bootstrap for responsive design
- Font Awesome for icons

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Review the documentation

---

**Perfect Closet** - Empowering women with AI-driven fashion insights! 👗✨