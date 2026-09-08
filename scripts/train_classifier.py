import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import joblib

# Load processed CSV metrics
df = pd.read_csv("data/processed/celeba_color_features.csv")

# Generate baseline feature matrix
X = df[["L", "a", "b", "ita", "chroma"]]

# Map features to initial seasonal centroids using vector distances
# (e.g., Cool/High Lightness -> Summer, Warm/High Saturation -> Spring)
def assign_pseudo_season(row):
    l = row["L"]
    b = row["b"]
    c = row["chroma"]
    
    # Warm (b > 1.5) vs Cool (b <= 1.5)
    if b > 1.5:
        # Warm family: Spring (Light) or Autumn (Deep)
        if l > 60:
            # Spring
            if c > 24:
                return "Bright Spring"
            elif l > 70:
                return "Light Spring"
            else:
                return "Warm Spring"
        else:
            # Autumn
            if c < 16:
                return "Soft Autumn"
            elif l < 46:
                return "Deep Autumn"
            else:
                return "Warm Autumn"
    else:
        # Cool family: Summer (Light) or Winter (Deep)
        if l > 58:
            # Summer
            if c < 16:
                return "Soft Summer"
            elif l > 70:
                return "Light Summer"
            else:
                return "Cool Summer"
        else:
            # Winter
            if c > 24:
                return "Bright Winter"
            elif l < 46:
                return "Deep Winter"
            else:
                return "Cool Winter"

y = df.apply(assign_pseudo_season, axis=1)

# Fit lightweight Nearest Neighbors model
model = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
model.fit(X, y)

# Export artifact for production backend
joblib.dump(model, "backend/models/season_classifier.joblib")
print("Exported production classifier to backend/models/season_classifier.joblib")