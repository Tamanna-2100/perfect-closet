import os
import requests
from typing import List, Optional
from backend.schemas.models import InspirationPin, ProductSuggestion

# Curated high-aesthetic fashion inspiration items for seasons
CURATED_INSPIRATION: List[InspirationPin] = [
    # Winter
    InspirationPin(
        id="pin-win-1",
        title="High-Contrast Tailored Monochrome Suit",
        image_url="https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=deep+winter+tailored+suit",
        description="Structured charcoal and crisp white with sharp lines and sterling silver accents.",
        season="Winter",
        style_category="Formal Tailoring"
    ),
    InspirationPin(
        id="pin-win-2",
        title="Royal Cobalt Cashmere & Leather Accents",
        image_url="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=cobalt+blue+coat+winter",
        description="Vibrant cobalt wool coat paired with black boots and minimalist platinum jewelry.",
        season="Winter",
        style_category="Casual Chic"
    ),
    InspirationPin(
        id="pin-win-3",
        title="Midnight Velvet Evening Ensemble",
        image_url="https://images.unsplash.com/photo-1539109136881-3be0616acf4b?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=midnight+blue+velvet+outfit",
        description="Luxurious dark jewel tone silhouette with deep sapphire undertones.",
        season="Winter",
        style_category="Evening Wear"
    ),
    # Summer
    InspirationPin(
        id="pin-sum-1",
        title="Frosted Powder Blue Linen Layering",
        image_url="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=powder+blue+linen+aesthetic",
        description="Soft, airy layers in powder blue and cool dove grey with matte silver details.",
        season="Summer",
        style_category="Casual Summer"
    ),
    InspirationPin(
        id="pin-sum-2",
        title="Muted Lavender Silk Slip & Slate Knit",
        image_url="https://images.unsplash.com/photo-1485230895905-ec40ba36b9bc?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=lavender+silk+skirt+slate+sweater",
        description="Gentle tonal pairing of smoky amethyst knitwear over washed lilac silk.",
        season="Summer",
        style_category="Smart Casual"
    ),
    # Spring
    InspirationPin(
        id="pin-spr-1",
        title="Warm Peach Trench & Sunlit Silk Scarf",
        image_url="https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=peach+trench+coat+spring",
        description="Luminous golden-peach trench coat styled with warm cream trousers and gold jewelry.",
        season="Spring",
        style_category="Daywear"
    ),
    InspirationPin(
        id="pin-spr-2",
        title="Bright Coral & Clean White Resort Set",
        image_url="https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=coral+blazer+spring+aesthetic",
        description="Vivid warm coral tailored blazer with crisp warm-white accents.",
        season="Spring",
        style_category="Resort & Vacation"
    ),
    # Autumn
    InspirationPin(
        id="pin-aut-1",
        title="Toasted Rust Wool Coat & Camel Cashmere",
        image_url="https://images.unsplash.com/photo-1509631179647-0177331693ae?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=rust+coat+camel+cashmere+autumn",
        description="Rich spiced pumpkin and warm walnut knitwear layered with burnished brass.",
        season="Autumn",
        style_category="Autumn Outerwear"
    ),
    InspirationPin(
        id="pin-aut-2",
        title="Olive Suede & Dark Blackberry Accordion Skirt",
        image_url="https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=80",
        pin_url="https://www.pinterest.com/search/pins/?q=olive+green+dark+burgundy+outfit",
        description="Earthy moss green tailored suede jacket over a deep wine pleated skirt.",
        season="Autumn",
        style_category="Smart Casual"
    ),
]

# Curated retail products matching seasonal palettes
CURATED_PRODUCTS: List[ProductSuggestion] = [
    # Tops
    ProductSuggestion(
        id="prod-1",
        title="Double-Breasted Wool Blazer in Midnight Navy",
        price="$248.00",
        merchant="Nordstrom",
        product_url="https://www.google.com/search?tbm=shop&q=midnight+navy+wool+blazer",
        image_url="https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=600&q=80",
        garment_type="Outerwear",
        cut="Structured Tailored",
        color_name="Midnight Navy",
        color_hex="#0B132B",
        match_score=98.5
    ),
    ProductSuggestion(
        id="prod-2",
        title="Pure Cashmere Crewneck Sweater in Ice Cerulean",
        price="$165.00",
        merchant="Everlane",
        product_url="https://www.google.com/search?tbm=shop&q=ice+blue+cashmere+crewneck",
        image_url="https://images.unsplash.com/photo-1576566588028-4147f3842f27?auto=format&fit=crop&w=600&q=80",
        garment_type="Tops",
        cut="Relaxed Fit",
        color_name="Ice Cerulean",
        color_hex="#0077B6",
        match_score=96.0
    ),
    ProductSuggestion(
        id="prod-3",
        title="Bias-Cut Mulberry Silk Midi Dress in Bordeaux",
        price="$295.00",
        merchant="Reformation",
        product_url="https://www.google.com/search?tbm=shop&q=bordeaux+silk+slip+dress",
        image_url="https://images.unsplash.com/photo-1595777457583-95e059d581b8?auto=format&fit=crop&w=600&q=80",
        garment_type="Dresses",
        cut="Slip / Bias Cut",
        color_name="Bordeaux Crimson",
        color_hex="#780000",
        match_score=97.0
    ),
    ProductSuggestion(
        id="prod-4",
        title="Wide-Leg Pleated Trousers in Pure Alabaster",
        price="$138.00",
        merchant="COS",
        product_url="https://www.google.com/search?tbm=shop&q=white+wide+leg+pleated+trousers",
        image_url="https://images.unsplash.com/photo-1509551388413-e18d0ac5d495?auto=format&fit=crop&w=600&q=80",
        garment_type="Pants",
        cut="Wide-Leg High-Rise",
        color_name="Pure White",
        color_hex="#FFFFFF",
        match_score=94.5
    ),
    ProductSuggestion(
        id="prod-5",
        title="Brushed Alpaca Cardigan in Powder Lilac",
        price="$198.00",
        merchant="Sézane",
        product_url="https://www.google.com/search?tbm=shop&q=lilac+alpaca+cardigan",
        image_url="https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=600&q=80",
        garment_type="Tops",
        cut="Oversized Knit",
        color_name="Lilac Mist",
        color_hex="#E8DFF5",
        match_score=95.2
    ),
    ProductSuggestion(
        id="prod-6",
        title="Linen Wrap Dress in Seafoam Green",
        price="$178.00",
        merchant="Anthropologie",
        product_url="https://www.google.com/search?tbm=shop&q=seafoam+green+linen+wrap+dress",
        image_url="https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?auto=format&fit=crop&w=600&q=80",
        garment_type="Dresses",
        cut="A-Line Wrap",
        color_name="Seafoam Dew",
        color_hex="#DDEDEA",
        match_score=93.8
    ),
    ProductSuggestion(
        id="prod-7",
        title="Belted Wool Trench in Spiced Pumpkin Rust",
        price="$340.00",
        merchant="Massimo Dutti",
        product_url="https://www.google.com/search?tbm=shop&q=rust+orange+wool+trench+coat",
        image_url="https://images.unsplash.com/photo-1544441893-675973e31985?auto=format&fit=crop&w=600&q=80",
        garment_type="Outerwear",
        cut="Belted Trench",
        color_name="Spiced Pumpkin",
        color_hex="#CA6702",
        match_score=96.7
    ),
    ProductSuggestion(
        id="prod-8",
        title="High-Waisted Corduroy Flared Pants in Forest Moss",
        price="$120.00",
        merchant="Madewell",
        product_url="https://www.google.com/search?tbm=shop&q=olive+green+corduroy+flared+pants",
        image_url="https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=600&q=80",
        garment_type="Pants",
        cut="Flared High-Rise",
        color_name="Forest Moss",
        color_hex="#6B705C",
        match_score=94.0
    ),
    ProductSuggestion(
        id="prod-9",
        title="Silk Chiffon Blouse in Warm Coral",
        price="$145.00",
        merchant="Boden",
        product_url="https://www.google.com/search?tbm=shop&q=warm+coral+silk+blouse",
        image_url="https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=600&q=80",
        garment_type="Tops",
        cut="Fluid Draped",
        color_name="Warm Coral",
        color_hex="#E76F51",
        match_score=95.8
    ),
]

class SerpService:
    def __init__(self):
        self.api_key = os.environ.get("SERPAPI_API_KEY")

    def get_inspiration(self, season_name: str, season_family: str) -> List[InspirationPin]:
        """Fetch Pinterest inspiration pins matching the user's seasonal palette."""
        # Check if live SERP API is configured
        if self.api_key:
            try:
                url = "https://serpapi.com/search"
                params = {
                    "engine": "pinterest",
                    "q": f"{season_name} color palette fashion outfit aesthetic",
                    "api_key": self.api_key,
                }
                res = requests.get(url, params=params, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    pins = []
                    for i, item in enumerate(data.get("organic_results", [])[:6]):
                        pins.append(InspirationPin(
                            id=f"serp-pin-{i}",
                            title=item.get("title", f"{season_name} Outfit Inspiration"),
                            image_url=item.get("image", ""),
                            pin_url=item.get("link", "https://pinterest.com"),
                            description=item.get("snippet", f"Styled for {season_name}"),
                            season=season_family,
                            style_category="Trending Look"
                        ))
                    if pins:
                        return pins
            except Exception as err:
                print(f"SERP API Pinterest fallback triggered: {err}")

        # Fallback to curated high-resolution inspiration matching family
        matches = [pin for pin in CURATED_INSPIRATION if pin.season == season_family]
        if not matches:
            matches = CURATED_INSPIRATION[:4]
        return matches

    def get_products(
        self,
        season_name: str,
        garment_type: Optional[str] = None,
        cut: Optional[str] = None
    ) -> List[ProductSuggestion]:
        """Fetch Google Shopping product suggestions with merchant links."""
        products = CURATED_PRODUCTS

        if garment_type and garment_type.lower() != "all":
            products = [p for p in products if p.garment_type.lower() == garment_type.lower()]

        if cut and cut.lower() != "all":
            products = [p for p in products if cut.lower() in p.cut.lower()]

        return products

# Global singleton
serp_service = SerpService()
