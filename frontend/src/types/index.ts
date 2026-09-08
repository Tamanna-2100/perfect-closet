export interface ColorMetrics {
  L: number;
  a: number;
  b: number;
  ita: number;
  chroma: number;
  hex_code: string;
}

export interface ExtractedFeatures {
  skin: ColorMetrics;
  hair: ColorMetrics;
  iris: ColorMetrics;
  contrast_ratio: number;
}

export interface ColorSwatch {
  hex: string;
  name: string;
  L: number;
  a: number;
  b: number;
}

export interface SeasonResult {
  season_name: string;
  season_family: "Spring" | "Summer" | "Autumn" | "Winter" | string;
  undertone: string;
  value: string;
  chroma: string;
  tagline: string;
  description: string;
  palette: ColorSwatch[];
  complementary_colors: ColorSwatch[];
  recommended_metals: string[];
  colors_to_avoid: string[];
  styling_tips: string[];
}

export interface InspirationPin {
  id: string;
  title: string;
  image_url: string;
  pin_url: string;
  description: string;
  season: string;
  style_category: string;
}

export interface ProductSuggestion {
  id: string;
  title: string;
  price: string;
  merchant: string;
  product_url: string;
  image_url: string;
  garment_type: string;
  cut: string;
  color_name: string;
  color_hex: string;
  match_score: number;
}

export interface AnalysisResponse {
  features: ExtractedFeatures;
  season: SeasonResult;
  inspiration: InspirationPin[];
  products: ProductSuggestion[];
}
