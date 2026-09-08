import math
from typing import Dict, List
from backend.schemas.models import SeasonResult, ColorSwatch

def hex_to_lab(hex_str: str):
    """Convert hex string to CIELAB (D65 illuminant, sRGB standard)."""
    hex_clean = hex_str.lstrip("#")
    r_val = int(hex_clean[0:2], 16) / 255.0
    g_val = int(hex_clean[2:4], 16) / 255.0
    b_val = int(hex_clean[4:6], 16) / 255.0

    # sRGB to linear RGB
    def linearize(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r_lin = linearize(r_val)
    g_lin = linearize(g_val)
    b_lin = linearize(b_val)

    # Linear RGB to XYZ (D65)
    X = r_lin * 0.4124564 + g_lin * 0.3575761 + b_lin * 0.1804375
    Y = r_lin * 0.2126729 + g_lin * 0.7151522 + b_lin * 0.0721750
    Z = r_lin * 0.0193339 + g_lin * 0.1191920 + b_lin * 0.9503041

    # Normalize by D65 reference white
    xn, yn, zn = 0.95047, 1.00000, 1.08883
    xr = X / xn
    yr = Y / yn
    zr = Z / zn

    def f(t):
        return t ** (1.0 / 3.0) if t > 0.008856 else (7.787 * t) + (16.0 / 116.0)

    fx = f(xr)
    fy = f(yr)
    fz = f(zr)

    L = max(0.0, min(100.0, (116.0 * fy) - 16.0))
    a = 500.0 * (fx - fy)
    b = 200.0 * (fy - fz)
    return round(L, 2), round(a, 2), round(b, 2)

def make_swatch(hex_code: str, name: str) -> ColorSwatch:
    l_val, a_val, b_val = hex_to_lab(hex_code)
    return ColorSwatch(hex=hex_code, name=name, L=l_val, a=a_val, b=b_val)

SEASONS_DATA: Dict[str, SeasonResult] = {
    "Deep Winter": SeasonResult(
        season_name="Deep Winter",
        season_family="Winter",
        undertone="Cool",
        value="Deep",
        chroma="Clear",
        tagline="High contrast, rich saturation, and midnight depths.",
        description="Deep Winter is characterized by intense, dark, and highly saturated coloring. Your high visual contrast pairs best with stark, dramatic jewel tones and vivid cool hues.",
        palette=[
            make_swatch("#0B132B", "Midnight Navy"),
            make_swatch("#1C2541", "Obsidian Blue"),
            make_swatch("#480CA8", "Imperial Purple"),
            make_swatch("#7209B7", "Royal Violet"),
            make_swatch("#B5179E", "Vivid Magenta"),
            make_swatch("#780000", "Bordeaux Crimson"),
            make_swatch("#004B23", "Deep Forest"),
            make_swatch("#000000", "True Black"),
            make_swatch("#FFFFFF", "Pure White"),
            make_swatch("#3A0CA3", "Cobalt Indigo"),
        ],
        complementary_colors=[
            make_swatch("#0077B6", "Ice Cerulean"),
            make_swatch("#F72585", "Electric Fuchsia"),
            make_swatch("#10002B", "Deep Plum"),
            make_swatch("#E0AAFF", "Icy Lavender"),
        ],
        recommended_metals=["Platinum", "White Gold", "Polished Sterling Silver", "Black Rhodium"],
        colors_to_avoid=["Mustard Yellow", "Warm Beige", "Rusty Orange", "Olive Drab", "Peach"],
        styling_tips=[
            "Lean into high-contrast monochrome (pure black paired with crisp white or electric jewel accents).",
            "Select structured tailoring with sharp silhouettes and clean lapels.",
            "Choose high-luster jewelry in platinum or silver to accentuate cool contrast.",
        ],
    ),
    "Cool Winter": SeasonResult(
        season_name="Cool Winter",
        season_family="Winter",
        undertone="Cool",
        value="Medium-Deep",
        chroma="Clear/Icy",
        tagline="Crisp frosted tones, royal blues, and sparkling clarity.",
        description="Cool Winter is undeniably cool-toned with crystal clarity. Your best colors have zero yellow warmth, favoring pure icy tones, bright sapphire, and deep emerald.",
        palette=[
            make_swatch("#001219", "Deepest Sapphire"),
            make_swatch("#005F73", "Dark Teal"),
            make_swatch("#0A9396", "Ocean Viridian"),
            make_swatch("#94D2BD", "Icy Mint"),
            make_swatch("#EE9B00", "Frost Primrose"),
            make_swatch("#CA6702", "Arctic Ruby"),
            make_swatch("#BB3E03", "Cool Scarlet"),
            make_swatch("#AE2012", "Cranberry"),
            make_swatch("#9B2226", "Garnet Red"),
            make_swatch("#F8F9FA", "Snow White"),
        ],
        complementary_colors=[
            make_swatch("#2B2D42", "Slate Indigo"),
            make_swatch("#D90429", "Cherry Red"),
            make_swatch("#4361EE", "Royal Azure"),
            make_swatch("#E2EAFC", "Frosted Ice"),
        ],
        recommended_metals=["Sterling Silver", "White Gold", "Bright Platinum"],
        colors_to_avoid=["Goldenrod", "Warm Camel", "Terracotta", "Olive Green"],
        styling_tips=[
            "Avoid any warm golden or earthy hues next to your face.",
            "Pair icy pastels with deep primary blues for a striking look.",
            "Choose matte finishes for structured outerwear, accented by brilliant silver hardware.",
        ],
    ),
    "Bright Winter": SeasonResult(
        season_name="Bright Winter",
        season_family="Winter",
        undertone="Neutral-Cool",
        value="Medium",
        chroma="High Brightness",
        tagline="Vivid pop colors, electric accents, and stark high clarity.",
        description="Bright Winter combines the cool depth of Winter with the vibrant brilliance of Spring. You can effortlessly carry intense electric hues that would overwhelm softer seasons.",
        palette=[
            make_swatch("#FF0054", "Hot Ruby"),
            make_swatch("#FF5400", "Neon Poppy"),
            make_swatch("#9E0059", "Electric Berry"),
            make_swatch("#390099", "Deep Royal"),
            make_swatch("#00F5D4", "Bright Turquoise"),
            make_swatch("#00BBF9", "Electric Cyan"),
            make_swatch("#FEE440", "Bright Acid Lemon"),
            make_swatch("#050505", "Jet Black"),
            make_swatch("#F8F9FA", "Pure White"),
            make_swatch("#7B2CBF", "Vivid Amethyst"),
        ],
        complementary_colors=[
            make_swatch("#06D6A0", "Neon Emerald"),
            make_swatch("#118AB2", "Bold Cerulean"),
            make_swatch("#FF006E", "Shocking Pink"),
            make_swatch("#8338EC", "Ultra Violet"),
        ],
        recommended_metals=["High-Polished Silver", "Platinum", "Bright White Gold"],
        colors_to_avoid=["Muted Taupe", "Dull Gray", "Dusty Rose", "Earthy Browns"],
        styling_tips=[
            "Embrace color-blocking with vibrant jewel tones against stark black or white.",
            "Incorporate sharp, geometric prints and glossy accessories.",
            "Opt for high-shine patent leather or metallic accessories.",
        ],
    ),
    "Light Spring": SeasonResult(
        season_name="Light Spring",
        season_family="Spring",
        undertone="Warm",
        value="Light",
        chroma="Clear/Luminous",
        tagline="Delicate golden sunshine, peach blossoms, and pastel radiance.",
        description="Light Spring is delicate, warm, and radiant with high lightness. Your palette consists of sunny, cheerful pastels infused with golden warmth.",
        palette=[
            make_swatch("#FFE8D6", "Vanilla Cream"),
            make_swatch("#FFB5A7", "Warm Peach"),
            make_swatch("#FCD5CE", "Soft Apricot"),
            make_swatch("#F8EDEB", "Alabaster Pink"),
            make_swatch("#D8E2DC", "Pistachio Foam"),
            make_swatch("#B7E4C7", "Spring Meadow"),
            make_swatch("#95D5B2", "Mint Sorbet"),
            make_swatch("#52B788", "Fresh Grass"),
            make_swatch("#FFC6FF", "Warm Lilac"),
            make_swatch("#FDFFB6", "Buttercup Yellow"),
        ],
        complementary_colors=[
            make_swatch("#FFADAD", "Coral Petal"),
            make_swatch("#CAFFBF", "Celery Dew"),
            make_swatch("#9BF6FF", "Aqua Mist"),
            make_swatch("#A0C4FF", "Sunny Cornflower"),
        ],
        recommended_metals=["Light Yellow Gold", "Rose Gold", "Polished Brass"],
        colors_to_avoid=["Heavy Black", "Burgundy", "Dark Navy", "Muddy Olive"],
        styling_tips=[
            "Keep outfits luminous; replace black with warm ivory, camel, or golden tan.",
            "Choose lightweight, breezy fabrics like silk, linen, and chiffon.",
            "Accessorize with delicate yellow gold or warm freshwater pearls.",
        ],
    ),
    "Warm Spring": SeasonResult(
        season_name="Warm Spring",
        season_family="Spring",
        undertone="Warm",
        value="Medium-Light",
        chroma="Vibrant/Warm",
        tagline="Golden honey, ripe mango, and vivid tropical blooms.",
        description="Warm Spring features rich golden undertones and sunny vibrancy. Your palette radiates warmth, evoking tropical foliage, marigolds, and coral reefs.",
        palette=[
            make_swatch("#FF7B00", "Warm Tangerine"),
            make_swatch("#FF9500", "Golden Honey"),
            make_swatch("#FFB703", "Marigold Amber"),
            make_swatch("#FB8500", "Papaya Orange"),
            make_swatch("#E76F51", "Warm Coral"),
            make_swatch("#F4A261", "Sunlit Terracotta"),
            make_swatch("#2A9D8F", "Warm Teal"),
            make_swatch("#588157", "Lush Leaf Green"),
            make_swatch("#3A5A40", "Warm Fern"),
            make_swatch("#FFF3B0", "Warm Butter"),
        ],
        complementary_colors=[
            make_swatch("#E07A5F", "Terracotta Rose"),
            make_swatch("#81B29A", "Warm Sage"),
            make_swatch("#F2CC8F", "Warm Wheat"),
            make_swatch("#3D405B", "Warm Ink"),
        ],
        recommended_metals=["Rich Yellow Gold", "Warm Bronze", "Polished Copper"],
        colors_to_avoid=["Icy Blue", "Cool Slate", "Stark White", "Cool Magenta"],
        styling_tips=[
            "Layer rich golden neutrals like cognac, camel, and warm wheat as your wardrobe base.",
            "Infuse outfits with bold pop accents of coral, marigold, or warm turquoise.",
            "Choose tortoiseshell and warm amber accessories.",
        ],
    ),
    "Bright Spring": SeasonResult(
        season_name="Bright Spring",
        season_family="Spring",
        undertone="Neutral-Warm",
        value="Medium",
        chroma="High Vibrancy",
        tagline="Tropical energy, vivid watermelon, and brilliant turquoise.",
        description="Bright Spring sits between Spring and Winter, blending blazing warmth with electric intensity. You shine in bright, saturated colors with lively contrast.",
        palette=[
            make_swatch("#FF007F", "Watermelon Pink"),
            make_swatch("#FF3E00", "Flamingo Vermilion"),
            make_swatch("#FF9F1C", "Bright Clementine"),
            make_swatch("#FFE600", "Electric Daffodil"),
            make_swatch("#2EC4B6", "Brilliant Turquoise"),
            make_swatch("#011627", "Rich Petrol Navy"),
            make_swatch("#38B000", "Lime Chartreuse"),
            make_swatch("#70E000", "Electric Green"),
            make_swatch("#9D4EDD", "Bright Violet"),
            make_swatch("#FFFFFF", "Warm Clean White"),
        ],
        complementary_colors=[
            make_swatch("#00B4D8", "Vivid Lagoon"),
            make_swatch("#F72585", "Bright Raspberry"),
            make_swatch("#FFBE0B", "Solar Gold"),
            make_swatch("#FB5607", "Electric Amber"),
        ],
        recommended_metals=["Yellow Gold", "Rose Gold", "Bright Brass"],
        colors_to_avoid=["Dull Taupe", "Faded Dusty Mauve", "Ash Gray", "Drab Olive"],
        styling_tips=[
            "Don't shy away from dynamic contrast; pair vibrant tops with bold bottoms.",
            "Use clear, saturated accessories like colorful eyewear or statement footwear.",
            "Opt for high-energy prints with clear edges.",
        ],
    ),
    "Light Summer": SeasonResult(
        season_name="Light Summer",
        season_family="Summer",
        undertone="Cool",
        value="Light",
        chroma="Muted/Delicate",
        tagline="Seafoam mist, powder blue, and soft ballet pink.",
        description="Light Summer is airy, cool, and gentle. The palette is dominated by dreamy pastels, frosted blues, and muted rose tones that highlight delicate features.",
        palette=[
            make_swatch("#E8DFF5", "Lilac Mist"),
            make_swatch("#FCE1E4", "Ballet Slipper"),
            make_swatch("#FCF4DD", "Frosted Lemon"),
            make_swatch("#DDEDEA", "Seafoam Dew"),
            make_swatch("#DAEAF6", "Powder Blue"),
            make_swatch("#BEE1E6", "Sky Pastel"),
            make_swatch("#CDDAFD", "Cornflower Pastel"),
            make_swatch("#DFCCF1", "Lavender Haze"),
            make_swatch("#7B9E89", "Soft Eucalyptus"),
            make_swatch("#8E9AAF", "Muted Slate"),
        ],
        complementary_colors=[
            make_swatch("#CBC0D3", "Muted Thistle"),
            make_swatch("#EFD3D7", "Rose Quartz"),
            make_swatch("#FEE180", "Soft Primrose"),
            make_swatch("#A3C4BC", "Pale Jade"),
        ],
        recommended_metals=["Brushed Silver", "White Gold", "Soft Rose Gold"],
        colors_to_avoid=["Heavy Black", "Bright Orange", "Mustard", "Deep Burgundy"],
        styling_tips=[
            "Choose soft, muted neutrals like slate grey, soft taupe, and pearl white over black.",
            "Select fluid, flowing fabrics like cashmere, lightweight wool, and silk georgette.",
            "Keep jewelry delicate and matte-finished.",
        ],
    ),
    "Cool Summer": SeasonResult(
        season_name="Cool Summer",
        season_family="Summer",
        undertone="Cool",
        value="Medium",
        chroma="Muted/Gentle",
        tagline="Lavender fields, heather blue, and soft smoky plums.",
        description="Cool Summer is the classic epitome of cool, soft elegance. Without any warm or yellow influence, your palette favors soothing purples, rose-browns, and serene ocean blues.",
        palette=[
            make_swatch("#4A5759", "Smoky Blue-Grey"),
            make_swatch("#588B8B", "Sea Teal"),
            make_swatch("#B4A0E5", "Cool Periwinkle"),
            make_swatch("#9D8189", "Dusty Mauve"),
            make_swatch("#F4ACB7", "Soft Tea Rose"),
            make_swatch("#D8E2DC", "Cool Pearl"),
            make_swatch("#22223B", "Smoky Navy"),
            make_swatch("#4A4E69", "Dusky Violet"),
            make_swatch("#6B705C", "Muted Sage"),
            make_swatch("#B7B7A4", "Cool Ash"),
        ],
        complementary_colors=[
            make_swatch("#8E9AAF", "Cool Denim"),
            make_swatch("#C9ADA7", "Rose Taupe"),
            make_swatch("#F2E9E4", "Alabaster White"),
            make_swatch("#6D6875", "Smoky Amethyst"),
        ],
        recommended_metals=["Sterling Silver", "Antique Silver", "White Gold"],
        colors_to_avoid=["Warm Tan", "Terracotta", "Golden Ochre", "Rust Red"],
        styling_tips=[
            "Tone-on-tone dressing (e.g. layering shades of slate and dusty rose) creates effortless sophistication.",
            "Choose soft suede and matte leather textures over high gloss.",
            "Use cool berry tones for accent pieces.",
        ],
    ),
    "Soft Summer": SeasonResult(
        season_name="Soft Summer",
        season_family="Summer",
        undertone="Neutral-Cool",
        value="Medium",
        chroma="Muted/Smoky",
        tagline="Ethereal fog, weathered driftwood, and antique velvet roses.",
        description="Soft Summer sits on the border of Summer and Autumn. Low contrast, smoky undertones, and gentle complexity define this refined, muted palette.",
        palette=[
            make_swatch("#6C757D", "Smoky Heather"),
            make_swatch("#495057", "Charcoal Slate"),
            make_swatch("#8395A7", "Muted Airforce Blue"),
            make_swatch("#576574", "Storm Cloud"),
            make_swatch("#A39BA8", "Antique Amethyst"),
            make_swatch("#C8D6E5", "Muted Chambray"),
            make_swatch("#8395A7", "Glacier Grey"),
            make_swatch("#6C5B7B", "Dusty Plum"),
            make_swatch("#C06C84", "Vintage Rose"),
            make_swatch("#F8F9FA", "Soft Bone"),
        ],
        complementary_colors=[
            make_swatch("#5C6B73", "Deep Muted Slate"),
            make_swatch("#9DB4C0", "Muted Duck Egg"),
            make_swatch("#E0AFA0", "Muted Warm Mauve"),
            make_swatch("#463F3A", "Espresso Taupe"),
        ],
        recommended_metals=["Brushed Silver", "Pewter", "Matte Rose Gold"],
        colors_to_avoid=["Neon Yellow", "Electric Orange", "Pure Stark White", "Jet Black"],
        styling_tips=[
            "Opt for heathered fabrics, washed linens, and knits with visual depth.",
            "Replace stark black with dark charcoal or deep plum.",
            "Combine analogous soft colors for a cohesive, understated look.",
        ],
    ),
    "Soft Autumn": SeasonResult(
        season_name="Soft Autumn",
        season_family="Autumn",
        undertone="Neutral-Warm",
        value="Medium",
        chroma="Muted/Earthy",
        tagline="Golden dunes, roasted almonds, and weathered terracotta.",
        description="Soft Autumn blends warm earthiness with the muted softness of Summer. Your palette is comforting, subtle, and composed of toasted neutrals and olive foliage.",
        palette=[
            make_swatch("#DDBEA9", "Warm Biscuit"),
            make_swatch("#FFE8D6", "Cream Silk"),
            make_swatch("#B7B7A4", "Olive Sage"),
            make_swatch("#A5A58D", "Herb Green"),
            make_swatch("#6B705C", "Forest Moss"),
            make_swatch("#CB997E", "Toasted Ochre"),
            make_swatch("#A37081", "Dusty Marsala"),
            make_swatch("#7F5539", "Warm Walnut"),
            make_swatch("#9C6644", "Chestnut Brown"),
            make_swatch("#EDE0D4", "Oatmeal"),
        ],
        complementary_colors=[
            make_swatch("#8C5383", "Muted Blackberry"),
            make_swatch("#C47335", "Muted Cinnamon"),
            make_swatch("#7D8471", "Soft Eucalyptus"),
            make_swatch("#5F506B", "Dusky Violet"),
        ],
        recommended_metals=["Antique Brass", "Warm Bronze", "Brushed Yellow Gold"],
        colors_to_avoid=["Electric Blue", "Icy Pink", "Stark Pure White", "Bright Magenta"],
        styling_tips=[
            "Layer textural fabrics: suede, chunky wool, corduroy, and cashmere.",
            "Make warm camel and rich olive the backbone of your wardrobe.",
            "Opt for matte, organic jewelry stones such as tiger's eye, jasper, and jade.",
        ],
    ),
    "Warm Autumn": SeasonResult(
        season_name="Warm Autumn",
        season_family="Autumn",
        undertone="Warm",
        value="Medium-Deep",
        chroma="Rich/Warm",
        tagline="Maple harvest, burnished copper, and spiced cider.",
        description="Warm Autumn is the quintessential autumn palette: rich, deeply golden, and earthy. Rich spicy tones like paprika, rust, golden ochre, and moss green will make your features sing.",
        palette=[
            make_swatch("#9B2226", "Deep Spiced Apple"),
            make_swatch("#AE2012", "Burnt Vermilion"),
            make_swatch("#BB3E03", "Rust Copper"),
            make_swatch("#CA6702", "Spiced Pumpkin"),
            make_swatch("#EE9B00", "Burnished Gold"),
            make_swatch("#94D2BD", "Warm Sea Green"),
            make_swatch("#0A9396", "Warm Peacock"),
            make_swatch("#005F73", "Deep Teal Lake"),
            make_swatch("#582F0E", "Rich Mahogany"),
            make_swatch("#7F4F24", "Cinnamon Wood"),
        ],
        complementary_colors=[
            make_swatch("#656D4A", "Olive Army"),
            make_swatch("#414833", "Forest Timber"),
            make_swatch("#A68A56", "Rich Khaki"),
            make_swatch("#D4A373", "Warm Sandstone"),
        ],
        recommended_metals=["Yellow Gold", "Copper", "Antique Brass", "Bronze"],
        colors_to_avoid=["Icy Blue", "Silver", "Fuchsia", "Stark Black"],
        styling_tips=[
            "Use deep rust and chocolate brown instead of black for coats and footwear.",
            "Incorporate artisanal prints and woven leather accessories.",
            "Wear warm metals and amber or tortoiseshell finishes.",
        ],
    ),
    "Deep Autumn": SeasonResult(
        season_name="Deep Autumn",
        season_family="Autumn",
        undertone="Warm",
        value="Deep",
        chroma="Deep/Rich",
        tagline="Dark chocolate, espresso velvet, and midnight mahogany.",
        description="Deep Autumn is dark, intense, and grounded in rich warmth. Sharing depth with Winter, your palette features the deepest forest greens, black-browns, and rich jewel-toned garnets.",
        palette=[
            make_swatch("#2B1B17", "Black Coffee"),
            make_swatch("#3D0C02", "Black Cherry"),
            make_swatch("#5C1D24", "Deep Burgundy"),
            make_swatch("#800E13", "Oxblood Red"),
            make_swatch("#38040E", "Dark Blackberry"),
            make_swatch("#253D2C", "Deepest Forest"),
            make_swatch("#1B4965", "Dark Marine Teal"),
            make_swatch("#582F0E", "Roasted Cocoa"),
            make_swatch("#B07D62", "Warm Toffee"),
            make_swatch("#F7EBE8", "Warm Cream"),
        ],
        complementary_colors=[
            make_swatch("#641220", "Ruby Wine"),
            make_swatch("#6A040F", "Crimson Smoke"),
            make_swatch("#003566", "Deepest Petrol"),
            make_swatch("#DDA15E", "Caramel Amber"),
        ],
        recommended_metals=["Rich 18k Yellow Gold", "Antique Bronze", "Rose Gold"],
        colors_to_avoid=["Pastel Lavender", "Baby Blue", "Dusty Pink", "Stark Chalk White"],
        styling_tips=[
            "Choose luxurious deep textures: velvet, heavy knits, and full-grain leather.",
            "Anchor outfits with espresso brown or oxblood instead of stark black.",
            "Add accents of burnished bronze or warm gold hardware.",
        ],
    ),
}

def get_season_data(season_name: str) -> SeasonResult:
    """Retrieve SeasonResult by name, defaulting to Deep Winter if not found."""
    return SEASONS_DATA.get(season_name, SEASONS_DATA["Deep Winter"])
