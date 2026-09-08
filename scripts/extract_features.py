import os
import glob
import cv2
import numpy as np
import pandas as pd

def compute_color_metrics(img_path):
    img = cv2.imread(img_path)
    if img is None:
        return None
    
    # Convert BGR to CIELAB space
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    
    L, A, B = cv2.split(lab_img)
    mean_l = np.mean(L)
    mean_a = np.mean(A)
    mean_b = np.mean(B)
    
    # Calculate Individual Typology Angle (ITA)
    # ITA = arctan((L - 50) / b) * (180 / pi)
    b_val = mean_b if mean_b != 0 else 0.001
    ita = np.arctan((mean_l - 50) / b_val) * (180 / np.pi)
    
    # Saturation / Chroma
    chroma = np.sqrt(mean_a**2 + mean_b**2)
    
    return {
        "filename": os.path.basename(img_path),
        "L": mean_l,
        "a": mean_a,
        "b": mean_b,
        "ita": ita,
        "chroma": chroma
    }

def main():
    image_paths = glob.glob("data/raw/celeba/**/*.jpg", recursive=True)[:5000] # Batch of 5000 images
    data = []
    
    for path in image_paths:
        metrics = compute_color_metrics(path)
        if metrics:
            data.append(metrics)
            
    df = pd.DataFrame(data)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/celeba_color_features.csv", index=False)
    print("Saved feature dataset to data/processed/celeba_color_features.csv")

if __name__ == "__main__":
    main()