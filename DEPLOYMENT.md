# Deployment Guide - Perfect Closet

## 🚀 Deploy to Render (Free Tier)

### Step 1: Prepare Your Repository

1. **Push to GitHub** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Perfect Closet app"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/perfect-closet.git
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Sign up for Render**: Go to https://render.com and sign up with GitHub
2. **Create New Web Service**: 
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `perfect-closet` repository

3. **Configure Deployment**:
   ```
   Name: perfect-closet
   Environment: Python 3
   Build Command: ./build.sh
   Start Command: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
   ```

4. **Environment Variables** (in Render dashboard):
   ```
   SECRET_KEY=your-super-secret-key-here
   FLASK_ENV=production
   ```

5. **Deploy**: Click "Create Web Service"

### Step 3: Access Your App
- Your app will be available at: `https://your-app-name.onrender.com`
- Initial build takes 5-10 minutes
- Free tier sleeps after 15 minutes of inactivity

---

## 🐍 Deploy to PythonAnywhere

### Step 1: Sign Up
1. Go to https://www.pythonanywhere.com
2. Create a free "Beginner" account

### Step 2: Upload Your Code
1. **Upload files** via "Files" tab
2. **Or clone from GitHub**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/perfect-closet.git
   ```

### Step 3: Create Web App
1. Go to "Web" tab → "Add a new web app"
2. Choose "Flask" framework
3. Select Python 3.10
4. Set source code path to `/home/yourusername/perfect-closet`

### Step 4: Configure WSGI
Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import sys
import os

# Add your project directory to sys.path
path = '/home/yourusername/perfect-closet'
if path not in sys.path:
    sys.path.append(path)

from app import app as application

if __name__ == "__main__":
    application.run()
```

### Step 5: Install Dependencies
In a Bash console:
```bash
cd perfect-closet
pip3.10 install --user -r requirements.txt
```

### Step 6: Reload Web App
- Click "Reload" in the Web tab
- Access at: `https://yourusername.pythonanywhere.com`

---

## 🚂 Deploy to Railway

### Step 1: Sign Up
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Deploy
1. **New Project** → "Deploy from GitHub repo"
2. **Select repository**: Choose your perfect-closet repo
3. **Configure**:
   - Railway auto-detects Python
   - Uses your `requirements.txt` automatically

### Step 3: Environment Variables
```
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
PORT=5000
```

### Step 4: Custom Start Command (if needed)
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

---

## 🔧 Additional Deployment Options

### 1. **Vercel** (Serverless)
- Good for: Lightweight apps
- Limitations: Cold starts, limited for ML models
- Setup: Install Vercel CLI, add `vercel.json`

### 2. **Netlify** (Static + Functions)
- Good for: Frontend-heavy apps
- Limitations: Backend as functions only
- Setup: Deploy via Git integration

### 3. **Google Cloud Platform** (Free Tier)
- Good for: Scalable apps
- Free: 1 f1-micro instance
- Setup: App Engine or Compute Engine

### 4. **AWS** (Free Tier)
- Good for: Professional deployment
- Free: EC2 t2.micro, Lambda
- Setup: Elastic Beanstalk or EC2

---

## 🎯 Recommended Deployment Flow

### For Beginners: **Render**
✅ Easiest setup
✅ Automatic HTTPS
✅ Good for ML models
✅ GitHub integration

### For Python Developers: **PythonAnywhere**
✅ Python-focused
✅ Good free tier
✅ Easy package management
✅ SSH access

### For Scalability: **Railway**
✅ Modern platform
✅ Easy scaling
✅ Good developer experience
✅ Database integration

---

## 🚨 Important Notes

### Model Size Optimization
Your ResNet50 model might be large for free tiers:

1. **Optimize model**:
   ```python
   # In train_model.py, save only state dict
   torch.save(model.state_dict(), 'model_optimized.pth')
   ```

2. **Use model quantization**:
   ```python
   # Reduce model size
   model_quantized = torch.quantization.quantize_dynamic(
       model, {torch.nn.Linear}, dtype=torch.qint8
   )
   ```

3. **Consider model alternatives**:
   - Use MobileNet instead of ResNet50
   - Implement model caching
   - Use external model hosting

### Performance Tips

1. **Reduce memory usage**:
   ```python
   # In app.py
   torch.set_num_threads(1)  # Reduce CPU usage
   ```

2. **Optimize image processing**:
   ```python
   # Reduce image size before processing
   max_size = (512, 512)
   image.thumbnail(max_size, Image.Resampling.LANCZOS)
   ```

3. **Add caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def cached_prediction(image_hash):
       # Cache predictions
   ```

---

## 🔍 Troubleshooting

### Common Issues:

1. **Build timeout**: Increase timeout in deployment settings
2. **Memory issues**: Reduce model size or use CPU-only
3. **Slug size too large**: Use `.gitignore` to exclude unnecessary files
4. **Import errors**: Ensure all dependencies in `requirements.txt`

### Monitoring:

1. **Check logs** in platform dashboard
2. **Monitor memory usage**
3. **Set up error tracking** (Sentry)
4. **Add health checks**

---

## 🎉 Next Steps

After deployment:

1. **Custom domain** (if platform supports)
2. **SSL certificate** (usually automatic)
3. **Analytics** (Google Analytics)
4. **Error monitoring** (Sentry, LogRocket)
5. **Performance monitoring** (New Relic)
6. **Database** (PostgreSQL, MongoDB)
7. **CDN** (Cloudflare)

Choose the platform that best fits your needs and technical comfort level!