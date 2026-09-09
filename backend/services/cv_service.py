import os
import cv2
import numpy as np
import math
from typing import Tuple, List, Optional
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

def normalize_illumination(img: np.ndarray) -> np.ndarray:
    """
    Apply robust Gray-World chromatic adaptation with percentile clipping.
    Normalizes color temperature (e.g. golden afternoon sunlight or cool blue shadow)
    towards neutral D65 daylight while preserving genuine biological undertones.
    """
    img_float = img.astype(np.float32)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Clip extreme specular highlights (sun glare) and deep shadows
    p_low = np.percentile(gray, 6)
    p_high = np.percentile(gray, 94)
    mask = (gray >= p_low) & (gray <= p_high)
    
    if np.count_nonzero(mask) < 200:
        return img
        
    b_mean = float(np.mean(img_float[:, :, 0][mask]))
    g_mean = float(np.mean(img_float[:, :, 1][mask]))
    r_mean = float(np.mean(img_float[:, :, 2][mask]))
    
    avg_gray = (b_mean + g_mean + r_mean) / 3.0
    
    # Bounded gain factors to prevent unnatural shifts
    scale_b = float(np.clip(avg_gray / max(b_mean, 1.0), 0.78, 1.28))
    scale_g = float(np.clip(avg_gray / max(g_mean, 1.0), 0.88, 1.12))
    scale_r = float(np.clip(avg_gray / max(r_mean, 1.0), 0.78, 1.28))
    
    balanced = np.zeros_like(img_float)
    balanced[:, :, 0] = np.clip(img_float[:, :, 0] * scale_b, 0, 255)
    balanced[:, :, 1] = np.clip(img_float[:, :, 1] * scale_g, 0, 255)
    balanced[:, :, 2] = np.clip(img_float[:, :, 2] * scale_r, 0, 255)
    
    return balanced.astype(np.uint8)

def fallback_skin_extraction(img: np.ndarray) -> np.ndarray:
    """Deterministic CV fallback: YCrCb physiological skin segmentation."""
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    mask = cv2.inRange(ycrcb, lower, upper)
    skin_pixels = img[mask > 0]
    if len(skin_pixels) > 50:
        return np.median(skin_pixels, axis=0)
    h, w = img.shape[:2]
    center = img[h//3:2*h//3, w//3:2*w//3]
    return np.mean(center, axis=(0, 1))

def extract_robust_skin(img: np.ndarray, fx: int, fy: int, fw: int, fh: int) -> np.ndarray:
    """
    Extract skin color by segmenting the inner facial oval and filtering out
    specular highlights (sunlight glare, sweat) and shadows.
    """
    h, w = img.shape[:2]
    # Crop central facial region (avoids hair, ears, collar, background)
    y1 = max(0, fy + int(0.20 * fh))
    y2 = min(h, fy + int(0.75 * fh))
    x1 = max(0, fx + int(0.18 * fw))
    x2 = min(w, fx + int(0.82 * fw))
    
    face_inner = img[y1:y2, x1:x2]
    if face_inner.size == 0:
        return np.array([170, 150, 130], dtype=np.float32)
        
    ycrcb = cv2.cvtColor(face_inner, cv2.COLOR_BGR2YCR_CB)
    lower = np.array([0, 133, 77], dtype=np.uint8)
    upper = np.array([255, 173, 127], dtype=np.uint8)
    mask = cv2.inRange(ycrcb, lower, upper)
    
    skin_pixels = face_inner[mask > 0]
    if len(skin_pixels) > 100:
        # Convert skin pixels to LAB to isolate lightness distribution
        lab_pixels = cv2.cvtColor(skin_pixels[np.newaxis, :, :].astype(np.uint8), cv2.COLOR_BGR2LAB)[0]
        L_vals = lab_pixels[:, 0] * 100.0 / 255.0
        
        # Filter out specular highlights (glare) and deep shadows
        p_low = np.percentile(L_vals, 15)
        p_high = np.percentile(L_vals, 85)
        
        mid_mask = (L_vals >= p_low) & (L_vals <= p_high)
        if np.count_nonzero(mid_mask) > 30:
            return np.median(skin_pixels[mid_mask], axis=0)
        return np.median(skin_pixels, axis=0)
        
    # Multi-point anatomical fallback patches
    forehead = extract_patch_mean_color(img, fx + int(0.50 * fw), fy + int(0.22 * fh), radius=int(0.06 * fw))
    cheek_left = extract_patch_mean_color(img, fx + int(0.28 * fw), fy + int(0.55 * fh), radius=int(0.06 * fw))
    cheek_right = extract_patch_mean_color(img, fx + int(0.72 * fw), fy + int(0.55 * fh), radius=int(0.06 * fw))
    return np.median([forehead, cheek_left, cheek_right], axis=0)

def extract_robust_hair(
    img: np.ndarray,
    fx: int,
    fy: int,
    fw: int,
    fh: int,
    skin_bgr: np.ndarray,
    iris_metrics: Optional[ColorMetrics] = None
) -> np.ndarray:
    """
    Extract hair pigment across multiple anatomical hair zones (left temple,
    right temple, hairline, crown). Discards skin-matching pixels and bright background walls/sky.
    """
    h, w = img.shape[:2]
    
    # 5 anatomical hair sampling zones:
    # 1. Left temple / side of head
    # 2. Right temple / side of head
    # 3. Top crown center
    # 4. Top crown left
    # 5. Top crown right
    zones = [
        img[max(0, fy + int(0.12 * fh)):min(h, fy + int(0.60 * fh)), max(0, fx - int(0.16 * fw)):max(1, fx + int(0.04 * fw))],
        img[max(0, fy + int(0.12 * fh)):min(h, fy + int(0.60 * fh)), min(w - 1, fx + int(0.96 * fw)):min(w, fx + int(1.16 * fw))],
        img[max(0, fy - int(0.18 * fh)):max(1, fy + int(0.02 * fh)), max(0, fx + int(0.35 * fw)):min(w, fx + int(0.65 * fw))],
        img[max(0, fy - int(0.18 * fh)):max(1, fy + int(0.02 * fh)), max(0, fx + int(0.10 * fw)):min(w, fx + int(0.35 * fw))],
        img[max(0, fy - int(0.18 * fh)):max(1, fy + int(0.02 * fh)), max(0, fx + int(0.65 * fw)):min(w, fx + int(0.90 * fw))],
    ]
    
    candidate_patches = [z.reshape(-1, 3) for z in zones if z.size > 0]
    if not candidate_patches:
        return np.array([28, 24, 20], dtype=np.float32)
        
    all_cand = np.vstack(candidate_patches)
    
    # Convert candidate pixels and skin to LAB
    cand_lab = cv2.cvtColor(all_cand[np.newaxis, :, :].astype(np.uint8), cv2.COLOR_BGR2LAB)[0]
    skin_lab = cv2.cvtColor(np.uint8([[skin_bgr]]), cv2.COLOR_BGR2LAB)[0][0]
    
    cand_L = cand_lab[:, 0] * 100.0 / 255.0
    chroma_dist = np.linalg.norm(cand_lab[:, 1:] - skin_lab[1:], axis=1)
    
    # Filter out pixels that match skin chrominance (to avoid sampling forehead or ears)
    # and reject bright background/sky pixels (L* > 65)
    valid_mask = (chroma_dist > 4.5) & (cand_L < 65.0) & (cand_L > 4.0)
    
    if np.count_nonzero(valid_mask) > 40:
        valid_bgr = all_cand[valid_mask]
        valid_L = cand_L[valid_mask]
        
        # Hair pigment represents the true darker cluster (bottom 40th percentile of valid candidates)
        cutoff = np.percentile(valid_L, 40)
        hair_cluster = valid_bgr[valid_L <= max(cutoff, 16.0)]
        if len(hair_cluster) > 0:
            return np.median(hair_cluster, axis=0)
            
    # If iris is deeply pigmented (L <= 22), hair is virtually always deep dark (L ~ 22-26)
    if iris_metrics and iris_metrics.L <= 24.0:
        return np.array([30, 26, 22], dtype=np.float32)
        
    return np.median(all_cand, axis=0)

class ComputerVisionService:
    def __init__(self):
        face_path = getattr(cv2.data, "haarcascades", "") + "haarcascade_frontalface_default.xml"
        eye_path = getattr(cv2.data, "haarcascades", "") + "haarcascade_eye.xml"
        self.face_cascade = cv2.CascadeClassifier(face_path) if os.path.exists(face_path) else None
        self.eye_cascade = cv2.CascadeClassifier(eye_path) if os.path.exists(eye_path) else None

    def process_face_image(self, img_bytes: bytes) -> ExtractedFeatures:
        """
        Process user image bytes and extract skin, hair, and iris color metrics deterministically.
        Applies chromatic adaptation (illumination normalization) and multi-region sampling
        to ensure consistency across direct sunlight, indoor, and ambient lighting conditions.
        """
        nparr = np.frombuffer(img_bytes, np.uint8)
        raw_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if raw_img is None:
            raise ValueError("Invalid image file or corrupted image data.")

        # 1. Apply robust chromatic adaptation (illumination normalization)
        img = normalize_illumination(raw_img)

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = ()
        if self.face_cascade is not None and not self.face_cascade.empty():
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(60, 60))

        if len(faces) == 0:
            # Fallback: segment skin via physiological YCrCb
            skin_bgr = fallback_skin_extraction(img)
            hair_patch = img[0:max(1, h // 10), w // 4:3 * w // 4]
            hair_bgr = np.median(hair_patch, axis=(0, 1)) if hair_patch.size > 0 else np.array([35, 30, 25], dtype=np.float32)
            iris_bgr = np.array([45, 40, 35], dtype=np.float32)
            iris_metrics = compute_color_metrics(iris_bgr)
        else:
            # Select dominant face
            fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])

            # 2. Eye / Iris Extraction
            face_roi_color = img[fy:fy + int(0.6 * fh), fx:fx + fw]
            face_roi_gray = gray[fy:fy + int(0.6 * fh), fx:fx + fw]
            
            eyes = ()
            if self.eye_cascade is not None and not self.eye_cascade.empty():
                eyes = self.eye_cascade.detectMultiScale(face_roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(18, 18))

            if len(eyes) >= 1:
                iris_samples = []
                for (ex, ey, ew, eh) in eyes[:2]:
                    # Sample darkest core inside the eye (the iris/pupil)
                    eye_patch = face_roi_color[ey + int(0.25*eh):ey + int(0.75*eh), ex + int(0.25*ew):ex + int(0.75*ew)]
                    if eye_patch.size > 0:
                        patch_gray = cv2.cvtColor(eye_patch, cv2.COLOR_BGR2GRAY)
                        dark_thresh = np.percentile(patch_gray, 30)
                        iris_core = eye_patch[patch_gray <= dark_thresh]
                        if len(iris_core) > 0:
                            iris_samples.append(np.median(iris_core, axis=0))
                if iris_samples:
                    iris_bgr = np.mean(iris_samples, axis=0)
                else:
                    left_eye_est = extract_patch_mean_color(img, fx + int(0.32 * fw), fy + int(0.38 * fh), radius=4)
                    right_eye_est = extract_patch_mean_color(img, fx + int(0.68 * fw), fy + int(0.38 * fh), radius=4)
                    iris_bgr = np.mean([left_eye_est, right_eye_est], axis=0)
            else:
                left_eye_est = extract_patch_mean_color(img, fx + int(0.32 * fw), fy + int(0.38 * fh), radius=4)
                right_eye_est = extract_patch_mean_color(img, fx + int(0.68 * fw), fy + int(0.38 * fh), radius=4)
                iris_bgr = np.mean([left_eye_est, right_eye_est], axis=0)

            iris_metrics = compute_color_metrics(iris_bgr)

            # 3. Robust Skin Extraction (Inner facial oval, glare & shadow filtered)
            skin_bgr = extract_robust_skin(img, fx, fy, fw, fh)

            # 4. Multi-Zone Hair Extraction (Left/right temples & crown, non-skin cluster)
            hair_bgr = extract_robust_hair(img, fx, fy, fw, fh, skin_bgr, iris_metrics)

        skin_metrics = compute_color_metrics(skin_bgr)
        hair_metrics = compute_color_metrics(hair_bgr)

        # Contrast calculation with specular glare guard
        # If iris is deeply dark (L <= 24), natural hair cannot be L > 40 unless bleached or in glare
        effective_hair_L = hair_metrics.L
        if iris_metrics.L <= 24.0 and hair_metrics.L > 38.0:
            effective_hair_L = min(hair_metrics.L, iris_metrics.L + 8.0)

        lightness_diff = abs(skin_metrics.L - effective_hair_L)
        eye_diff = abs(skin_metrics.L - iris_metrics.L)
        
        # Composite contrast ratio: 60% hair difference, 40% eye difference
        contrast_ratio = min(100.0, max(0.0, lightness_diff * 0.60 + eye_diff * 0.40))

        return ExtractedFeatures(
            skin=skin_metrics,
            hair=hair_metrics,
            iris=iris_metrics,
            contrast_ratio=round(contrast_ratio, 2)
        )

# Global CV service singleton
cv_service = ComputerVisionService()
