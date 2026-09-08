import math
import joblib
import os
import numpy as np
from typing import Dict, Tuple
from backend.schemas.models import ExtractedFeatures, SeasonResult
from backend.services.palette_data import get_season_data

# Representative CIELAB centroids for 12 seasonal categories
# Features vector: [Skin_L, Skin_a, Skin_b, Contrast_Ratio, Chroma]
SEASON_CENTROIDS: Dict[str, Tuple[float, float, float, float, float]] = {
    # Spring (Warm & Light/Bright)
    "Light Spring": (76.0, 10.0, 19.0, 32.0, 21.5),
    "Warm Spring": (68.0, 14.0, 24.0, 42.0, 27.8),
    "Bright Spring": (66.0, 12.0, 18.0, 58.0, 21.6),
    # Summer (Cool & Light/Muted)
    "Light Summer": (78.0, 8.0, 11.0, 30.0, 13.6),
    "Cool Summer": (68.0, 9.0, 8.0, 38.0, 12.0),
    "Soft Summer": (62.0, 8.5, 11.0, 28.0, 13.9),
    # Autumn (Warm & Deep/Muted)
    "Soft Autumn": (60.0, 12.0, 17.0, 29.0, 20.8),
    "Warm Autumn": (52.0, 16.0, 25.0, 44.0, 29.7),
    "Deep Autumn": (42.0, 14.0, 18.0, 52.0, 22.8),
    # Winter (Cool & Deep/Bright)
    "Deep Winter": (44.0, 9.0, 6.0, 65.0, 10.8),
    "Cool Winter": (62.0, 10.0, 4.0, 60.0, 10.7),
    "Bright Winter": (68.0, 11.0, 7.0, 68.0, 13.0),
}

class ClassifierService:
    def __init__(self, model_path: str = "backend/models/season_classifier.joblib"):
        self.model = None
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
            except Exception as e:
                print(f"Notice: Could not load trained joblib model ({e}). Using CIELAB distance engine.")

    def classify(self, features: ExtractedFeatures) -> SeasonResult:
        """
        Deterministic 12-season classification adhering to project rules:
        - Pure CIELAB space calculations.
        - Temperature, Lightness, and Chroma analysis.
        - Distance-weighted matching against seasonal centroids.
        """
        skin = features.skin
        contrast = features.contrast_ratio
        chroma = skin.chroma

        # Feature vector for current user
        user_vector = np.array([skin.L, skin.a, skin.b, contrast, chroma], dtype=np.float32)

        # Weighting: Lightness (0.3), undertone a/b (0.4), contrast (0.2), chroma (0.1)
        weights = np.array([1.0, 1.2, 1.5, 0.8, 0.6], dtype=np.float32)

        # Calculate weighted Euclidean distance in CIELAB feature space
        best_season = "Deep Winter"
        min_distance = float("inf")

        # Undertone penalty: If user is distinctly cool (b < 10) or distinctly warm (b > 16),
        # penalize opposite undertone centroids
        is_warm = skin.b > 14.0 or (skin.b > 11.0 and skin.ita < 35.0)

        for season_name, centroid in SEASON_CENTROIDS.items():
            centroid_vector = np.array(centroid, dtype=np.float32)
            diff = (user_vector - centroid_vector) * weights
            dist = float(np.linalg.norm(diff))

            # Undertone alignment check
            season_is_warm = "Spring" in season_name or "Autumn" in season_name
            if is_warm and not season_is_warm:
                dist += 15.0  # Warm user penalized for cool seasons
            elif not is_warm and season_is_warm:
                dist += 15.0  # Cool user penalized for warm seasons

            # High contrast check
            if contrast > 50.0 and ("Soft" in season_name):
                dist += 10.0  # High contrast avoids soft/muted seasons
            elif contrast < 30.0 and ("Bright" in season_name):
                dist += 10.0  # Low contrast avoids bright/clear seasons

            if dist < min_distance:
                min_distance = dist
                best_season = season_name

        return get_season_data(best_season)

# Global classifier service singleton
classifier_service = ClassifierService()
