"""
Setup script for Perfect Closet application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "models",
        "static/uploads",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created: {directory}")

def create_env_file():
    """Create .env file from example"""
    if not os.path.exists('.env') and os.path.exists('.env.example'):
        print("🔧 Creating .env file...")
        with open('.env.example', 'r') as src, open('.env', 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created from .env.example")
        print("🔒 Please update the SECRET_KEY in .env file!")

def check_dataset():
    """Check if dataset exists"""
    print("📊 Checking dataset...")
    dataset_path = "temp_dataset"
    
    if os.path.exists(dataset_path):
        # Count images
        image_count = 0
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_count += 1
        
        print(f"✅ Dataset found with {image_count} images")
        
        if image_count < 10:
            print("⚠️  Dataset seems small. Consider adding more images for better training.")
    else:
        print("⚠️  Dataset not found at 'temp_dataset'")
        print("   You can still run the app with the pre-trained model.")

def check_pytorch_installation():
    """Check if PyTorch is properly installed"""
    print("🔥 Checking PyTorch installation...")
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} installed")
        
        if torch.cuda.is_available():
            print(f"🚀 CUDA available! GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("💻 Running on CPU (GPU not available)")
        return True
    except ImportError:
        print("❌ PyTorch not found!")
        return False

def run_basic_test():
    """Run a basic test to ensure everything works"""
    print("🧪 Running basic test...")
    try:
        from utils import setup_directories, DataValidator
        setup_directories()
        print("✅ Basic test passed!")
        return True
    except Exception as e:
        print(f"❌ Basic test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Perfect Closet Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("Please install requirements manually:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check PyTorch
    if not check_pytorch_installation():
        print("Please install PyTorch manually:")
        print("pip install torch torchvision")
        sys.exit(1)
    
    # Check dataset
    check_dataset()
    
    # Run basic test
    if not run_basic_test():
        print("Setup may have issues. Please check the error messages above.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update the SECRET_KEY in .env file")
    print("2. (Optional) Train your model: python train_model.py")
    print("3. Run the application: python app.py")
    print("4. Open http://localhost:5000 in your browser")
    print("\n💡 Tips:")
    print("- For better performance, use a GPU-enabled environment")
    print("- Add more training data for improved accuracy")
    print("- Read README.md for detailed instructions")

if __name__ == "__main__":
    main()