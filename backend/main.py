import os
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from backend.schemas.models import (
    AnalysisResponse,
    SeasonResult,
    InspirationPin,
    ProductSuggestion,
)
from backend.services.cv_service import cv_service
from backend.services.classifier_service import classifier_service
from backend.services.palette_data import SEASONS_DATA, get_season_data
from backend.services.serp_service import serp_service

load_dotenv()

app = FastAPI(
    title="Perfect Closet API",
    description="Deterministic Seasonal Color Analysis and Fashion Inspiration Engine",
    version="1.0.0"
)

# CORS Configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "Perfect Closet Core Engine",
        "supported_seasons": len(SEASONS_DATA)
    }

@app.get("/api/seasons", response_model=List[SeasonResult])
def list_seasons():
    """Retrieve color palettes and style profiles for all 12 seasons."""
    return list(SEASONS_DATA.values())

@app.get("/api/seasons/{season_name}", response_model=SeasonResult)
def get_season(season_name: str):
    """Retrieve a specific seasonal palette by name."""
    if season_name not in SEASONS_DATA:
        raise HTTPException(status_code=404, detail=f"Season '{season_name}' not found.")
    return SEASONS_DATA[season_name]

@app.get("/api/inspiration", response_model=List[InspirationPin])
def get_inspiration(
    season: str = Query("Winter", description="Season family name (Spring, Summer, Autumn, Winter)")
):
    """Retrieve outfit inspiration pins for a given season."""
    return serp_service.get_inspiration(season, season)

@app.get("/api/products", response_model=List[ProductSuggestion])
def get_products(
    season: Optional[str] = Query(None, description="Season name"),
    garment_type: Optional[str] = Query(None, description="Garment type filter (Tops, Dresses, Outerwear, Pants)"),
    cut: Optional[str] = Query(None, description="Cut filter")
):
    """Retrieve retail fashion suggestions matching the user's palette."""
    return serp_service.get_products(
        season_name=season or "Deep Winter",
        garment_type=garment_type,
        cut=cut
    )

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_photos(
    face_image: UploadFile = File(..., description="Illuminated close-up face photo"),
    body_image: Optional[UploadFile] = File(None, description="Optional full-body outfit photo")
):
    """
    Ingest user photo(s), extract facial/hair/iris regions deterministically using MediaPipe and OpenCV,
    compute CIELAB color coordinates and ITA, and classify into one of 12 seasonal palettes.
    """
    try:
        face_bytes = await face_image.read()
        if len(face_bytes) == 0:
            raise HTTPException(status_code=400, detail="Face image file is empty.")

        # 1. Deterministic Computer Vision Feature Extraction
        features = cv_service.process_face_image(face_bytes)

        # 2. 12-Season Classification in CIELAB space
        season_result = classifier_service.classify(features)

        # 3. Inspiration & Product Suggestions
        inspiration = serp_service.get_inspiration(season_result.season_name, season_result.season_family)
        products = serp_service.get_products(season_result.season_name)

        return AnalysisResponse(
            features=features,
            season=season_result,
            inspiration=inspiration,
            products=products
        )
    except ValueError as val_err:
        raise HTTPException(status_code=422, detail=str(val_err))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline error: {str(exc)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
