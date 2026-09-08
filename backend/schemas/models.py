from typing import List, Optional
from pydantic import BaseModel, Field

class ColorMetrics(BaseModel):
    L: float = Field(..., description="CIELAB Lightness (0-100)")
    a: float = Field(..., description="CIELAB a* axis (green to red)")
    b: float = Field(..., description="CIELAB b* axis (blue to yellow)")
    ita: float = Field(..., description="Individual Typology Angle in degrees")
    chroma: float = Field(..., description="Chroma / Saturation sqrt(a^2 + b^2)")
    hex_code: str = Field(..., description="Hexadecimal representation #RRGGBB")

class ExtractedFeatures(BaseModel):
    skin: ColorMetrics
    hair: ColorMetrics
    iris: ColorMetrics
    contrast_ratio: float = Field(..., description="Lightness contrast between skin and hair/eyes (0 to 100)")

class ColorSwatch(BaseModel):
    hex: str = Field(..., description="Hex color code #RRGGBB")
    name: str = Field(..., description="Readable color name")
    L: float
    a: float
    b: float

class SeasonResult(BaseModel):
    season_name: str = Field(..., description="e.g. Deep Winter, Soft Summer")
    season_family: str = Field(..., description="Spring, Summer, Autumn, or Winter")
    undertone: str = Field(..., description="Cool, Warm, or Neutral-Warm / Neutral-Cool")
    value: str = Field(..., description="Light, Medium, or Deep")
    chroma: str = Field(..., description="Clear/Bright or Soft/Muted")
    tagline: str
    description: str
    palette: List[ColorSwatch]
    complementary_colors: List[ColorSwatch]
    recommended_metals: List[str]
    colors_to_avoid: List[str]
    styling_tips: List[str]

class InspirationPin(BaseModel):
    id: str
    title: str
    image_url: str
    pin_url: str
    description: str
    season: str
    style_category: str

class ProductSuggestion(BaseModel):
    id: str
    title: str
    price: str
    merchant: str
    product_url: str
    image_url: str
    garment_type: str
    cut: str
    color_name: str
    color_hex: str
    match_score: float

class AnalysisResponse(BaseModel):
    features: ExtractedFeatures
    season: SeasonResult
    inspiration: List[InspirationPin]
    products: List[ProductSuggestion]
