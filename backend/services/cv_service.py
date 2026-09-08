import os
import cv2
import numpy as np
import mediapipe as mp
import math
from typing import Tuple, Optional
from backend.schemas.models import ColorMetrics, ExtractedFeatures

def bgr_to_standard_lab(bgr_color: np.ndarray) -> Tuple[float, float, float]:
    """
    Convert a BGR pixel/average array to standard CIELAB space.
    OpenCV maps 8-bit LAB as:
      L* = L * 100 / 255
      a* = a - 128
      b* = b - 128
    """
    pixel = np.uint8([[bgr_color]])
    lab_pixel = cv2.cvtColor(pixel, cv2.COLOR_BGR2LAB)[0][0]
    L = float(lab_pixel[0]) * 100.0 / 255.0
    a = float(lab_pixel[1]) - 128.0
    b = float(lab_pixel[2]) - 128.0
    return round(L, 2), round(a, 2), round(b, 2)

def bgr_to_hex(bgr_color: np.ndarray) -> str:
    b, g, r = [int(np.clip(c, 0, 255)) for c in bgr_color]
    return f"#{r:02X}{g:02X}{b:02X}"

def compute_color_metrics(bgr_color: np.ndarray) -> ColorMetrics:
    L, a, b = bgr_to_standard_lab(bgr_color)
    b_val = b if abs(b) > 0.001 else 0.001
    ita = float(np.arctan((L - 50.0) / b_val) * (180.0 / np.pi))
    chroma = float(np.sqrt(a**2 + b**2))
    hex_code = bgr_to_hex(bgr_color)
    return ColorMetrics(
        L=L,
        a=a,
        b=b,
        ita=round(ita, 2),
        chroma=round(chroma, 2),
        hex_code=hex_code
    )

def extract_patch_mean_color(img: np.ndarray, x: int, y: int, radius: int = 5) -> np.ndarray:
    """Safely sample mean BGR color from a patch around (x, y)."""
    h, w = img.shape[:2]
    y1 = max(0, y - radius)
    y2 = min(h, y + radius + 1)
    x1 = max(0, x - radius)
    x2 = min(w, x + radius + 1)
    patch = img[y1:y2, x1:x2]
    if patch.size == 0:
        return np.array([128, 128, 128], dtype=np.float32)
    return np.mean(patch, axis=(0, 1))

def fallback_skin_extraction(img: np.ndarray) -> np.ndarray:
    """Deterministic CV fallback: YCrCb skin segmentation."""
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    # Standard physiological skin threshold in YCrCb
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    mask = cv2.inRange(ycrcb, lower, upper)
    skin_pixels = img[mask > 0]
    if len(skin_pixels) > 50:
        return np.median(skin_pixels, axis=0)
    # Center crop fallback
    h, w = img.shape[:2]
    center = img[h//3:2*h//3, w//3:2*w//3]
    return np.mean(center, axis=(0, 1))

class ComputerVisionService:
    def __init__(self):
        # Deterministic OpenCV Face & Eye Cascade Detectors
        face_path = getattr(cv2.data, "haarcascades", "") + "haarcascade_frontalface_default.xml"
        eye_path = getattr(cv2.data, "haarcascades", "") + "haarcascade_eye.xml"
        self.face_cascade = cv2.CascadeClassifier(face_path) if os.path.exists(face_path) else None
        self.eye_cascade = cv2.CascadeClassifier(eye_path) if os.path.exists(eye_path) else None

    def process_face_image(self, img_bytes: bytes) -> ExtractedFeatures:
        """
        Process user image bytes and extract skin, hair, and iris color metrics deterministically.
        """
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Invalid image file or corrupted image data.")

        h, w = img.shape[:2]
        faces = ()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if self.face_cascade is not None and not self.face_cascade.empty():
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))

        if len(faces) == 0:
            # Fallback: segment skin via physiological YCrCb and sample regions
            skin_bgr = fallback_skin_extraction(img)
            hair_patch = img[0:max(1, h // 10), w // 4:3 * w // 4]
            hair_bgr = np.median(hair_patch, axis=(0, 1)) if hair_patch.size > 0 else np.array([35, 30, 25], dtype=np.float32)
            iris_bgr = np.array([45, 40, 35], dtype=np.float32)
        else:
            # Pick largest detected face
            fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])

            # 1. Skin Extraction (Forehead & Cheeks)
            forehead = extract_patch_mean_color(img, fx + int(0.50 * fw), fy + int(0.18 * fh), radius=int(0.06 * fw))
            cheek_left = extract_patch_mean_color(img, fx + int(0.24 * fw), fy + int(0.58 * fh), radius=int(0.06 * fw))
            cheek_right = extract_patch_mean_color(img, fx + int(0.76 * fw), fy + int(0.58 * fh), radius=int(0.06 * fw))
            skin_bgr = np.mean([forehead, cheek_left, cheek_right], axis=0)

            # 2. Eye / Iris Extraction
            face_roi_gray = gray[fy:fy + int(0.6 * fh), fx:fx + fw]
            eyes = ()
            if self.eye_cascade is not None and not self.eye_cascade.empty():
                eyes = self.eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20))

            if len(eyes) >= 1:
                iris_samples = []
                for (ex, ey, ew, eh) in eyes[:2]:
                    # Center of detected eye
                    eye_patch = extract_patch_mean_color(face_roi_color, ex + ew // 2, ey + eh // 2, radius=max(2, ew // 8))
                    iris_samples.append(eye_patch)
                iris_bgr = np.mean(iris_samples, axis=0)
            else:
                # Approximate eye position
                left_eye_est = extract_patch_mean_color(img, fx + int(0.32 * fw), fy + int(0.38 * fh), radius=4)
                right_eye_est = extract_patch_mean_color(img, fx + int(0.68 * fw), fy + int(0.38 * fh), radius=4)
                iris_bgr = np.mean([left_eye_est, right_eye_est], axis=0)

            # 3. Hair Extraction (Directly above the forehead)
            hair_y = max(0, fy - int(0.12 * fh))
            hair_bgr = extract_patch_mean_color(img, fx + int(0.50 * fw), hair_y, radius=int(0.08 * fw))

        skin_metrics = compute_color_metrics(skin_bgr)
        hair_metrics = compute_color_metrics(hair_bgr)
        iris_metrics = compute_color_metrics(iris_bgr)

        # Contrast calculation based on CIELAB lightness difference
        lightness_diff = abs(skin_metrics.L - hair_metrics.L)
        eye_diff = abs(skin_metrics.L - iris_metrics.L)
        contrast_ratio = min(100.0, max(0.0, lightness_diff * 0.7 + eye_diff * 0.3))

        return ExtractedFeatures(
            skin=skin_metrics,
            hair=hair_metrics,
            iris=iris_metrics,
            contrast_ratio=round(contrast_ratio, 2)
        )

# Global CV service singleton
cv_service = ComputerVisionService()
