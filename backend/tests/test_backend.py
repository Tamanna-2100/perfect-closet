import io
import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def create_synthetic_face_image() -> bytes:
    """Generate a synthetic 200x200 image resembling a face for CV testing."""
    img = np.ones((200, 200, 3), dtype=np.uint8) * 220
    # Simulate face ellipse with warm skin tone (BGR: ~ 160, 190, 230)
    cv2.ellipse(img, (100, 100), (60, 80), 0, 0, 360, (160, 190, 230), -1)
    # Hair patch at top
    cv2.rectangle(img, (40, 20), (160, 60), (30, 40, 50), -1)
    # Eyes
    cv2.circle(img, (80, 95), 8, (45, 55, 65), -1)
    cv2.circle(img, (120, 95), 8, (45, 55, 65), -1)

    _, encoded = cv2.imencode(".jpg", img)
    return encoded.tobytes()

def test_health_endpoint():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["supported_seasons"] == 12

def test_seasons_list():
    res = client.get("/api/seasons")
    assert res.status_code == 200
    seasons = res.json()
    assert len(seasons) == 12
    season_names = [s["season_name"] for s in seasons]
    assert "Deep Winter" in season_names
    assert "Light Spring" in season_names
    assert "Soft Autumn" in season_names

def test_analyze_endpoint():
    img_bytes = create_synthetic_face_image()
    files = {
        "face_image": ("test_face.jpg", io.BytesIO(img_bytes), "image/jpeg")
    }
    res = client.post("/api/analyze", files=files)
    assert res.status_code == 200
    data = res.json()
    assert "features" in data
    assert "season" in data
    assert "palette" in data["season"]
    assert len(data["season"]["palette"]) > 0
    assert "inspiration" in data
    assert "products" in data
    # Verify CIELAB fields
    assert "L" in data["features"]["skin"]
    assert "a" in data["features"]["skin"]
    assert "b" in data["features"]["skin"]
    assert "ita" in data["features"]["skin"]
