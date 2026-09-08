import os
import sys

# Ensure KAGGLE_API_TOKEN is set in the environment or ~/.kaggle/kaggle.json exists
if "KAGGLE_API_TOKEN" not in os.environ and not os.path.exists(os.path.expanduser("~/.kaggle/access_token")) and not os.path.exists(os.path.expanduser("~/.kaggle/kaggle.json")):
    print("Notice: KAGGLE_API_TOKEN environment variable not set. Please set it before downloading.")

try:
    import kagglehub
    print("Using modern kagglehub downloader...")
    path = kagglehub.dataset_download("jessicali9530/celeba-dataset")
    print(f"Dataset downloaded to cache at: {path}")
    
    # Symlink or copy to data/raw/celeba
    target_dir = os.path.abspath("data/raw/celeba")
    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
    if not os.path.exists(target_dir):
        os.symlink(path, target_dir)
        print(f"Created link: {target_dir} -> {path}")
    print("SUCCESS: CelebA is ready!")
    
except ImportError:
    # Fallback to kaggle package
    from kaggle.api.kaggle_api_extended import KaggleApi
    download_dir = "data/raw/celeba"
    os.makedirs(download_dir, exist_ok=True)
    api = KaggleApi()
    api.authenticate()
    print("Downloading via KaggleApi...")
    api.dataset_download_files("jessicali9530/celeba-dataset", path=download_dir, unzip=True)
    print("SUCCESS: CelebA download complete!")