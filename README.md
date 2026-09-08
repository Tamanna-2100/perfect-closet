# Perfect Closet 👗✨

**Perfect Closet** is an automated seasonal color analysis and personal styling platform. It uses deterministic computer vision and mathematical colorimetry to analyze user skin tone, hair, and eye contrast, accurately mapping individuals to one of the **12 Seasonal Color Palettes** (e.g., *Deep Winter*, *Soft Summer*, *Warm Autumn*, *Light Spring*), paired with curated outfit inspiration and real-time shoppable retail recommendations.

---

## 🌟 Key Features

- **Deterministic Computer Vision Pipeline**:
  - Facial feature & physiological skin segmentation using OpenCV Haar Cascades and YCrCb chrominance modeling.
  - Robust fallback mechanisms ensuring consistent results across diverse lighting and skin tones.
- **Mathematical Colorimetry & 12-Season Classification**:
  - RGB $\to$ CIELAB color space transformation.
  - Individual Typology Angle (ITA) computation for skin tone undertone and depth.
  - Contrast ratio calculation between skin, hair, and eye features.
  - Euclidean distance matching against seasonal centroids across 12 sub-seasons.
- **Inspiration & Retail Matching**:
  - Dynamic Pinterest-style outfit inspiration boards tailored to the detected season.
  - Google Shopping integration with direct merchant URLs and filterable garment attributes (tops, bottoms, dresses, outerwear).
- **Luxury-Grade Web Experience**:
  - Built with Next.js 16 (App Router), React 19, TypeScript, and Tailwind CSS.
  - Interactive dual-image upload zone (close-up portrait + full-body outfit).
  - Interactive palette explorer with hex copy, contrast badges, and seasonal guides.

---

## 🏗 System Architecture

```text
User Client (Next.js 16)
         │
         │ 1. Upload 2 Photos (Face + Full-Body)
         ▼
FastAPI Core Engine (:8000)
         │
         ├── Face / Skin / Iris Isolation (OpenCV / MediaPipe)
         ├── RGB ➔ CIELAB ➔ ITA Math Transformation
         └── 12-Season Centroid Classifier
         │
         ▼
Season Result & Style Attributes
         │
         ├── SerpApi: Pinterest Inspiration Retrieval
         └── SerpApi: Google Shopping E-Commerce Links
         │
         ▼
Interactive UI & Personal Styling Studio
```

---

## 📁 Repository Structure

```tree
perfect-closet/
├── backend/
│   ├── main.py                     # FastAPI application & API endpoints
│   ├── models/                     # Trained seasonal classifier models
│   ├── schemas/
│   │   └── models.py               # Pydantic schemas for request/response validation
│   ├── services/
│   │   ├── classifier_service.py   # 12-season distance & ITA classification
│   │   ├── cv_service.py           # Computer vision & skin extraction engine
│   │   ├── palette_data.py         # Curated 12-season palette color database
│   │   └── serp_service.py         # Pinterest & Google Shopping retrieval
│   └── tests/
│       └── test_backend.py         # Pytest test suite for CV and classification
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js App Router (page, layout, styles)
│   │   ├── components/             # UI components (UploadZone, PaletteViewer, etc.)
│   │   └── types/                  # TypeScript interfaces matching backend models
│   ├── package.json
│   └── tsconfig.json
├── scripts/
│   ├── download_datasets.py        # Dataset downloader (CelebA)
│   ├── extract_features.py         # Feature extraction script
│   └── train_classifier.py         # Seasonal model training script
├── requirements.txt                # Python backend dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python**: 3.11 or higher
- **Node.js**: 18.x or higher
- **npm** or **pnpm** / **yarn**

---

### 1. Backend Setup

1. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   *(Optional)* Add your `SERPAPI_API_KEY` for live shopping & inspiration queries. If omitted, the service gracefully provides high-quality curated fallbacks.

4. **Run the FastAPI server**:
   ```bash
   uvicorn backend.main:app --reload --port 8000
   ```
   API interactive docs will be live at `http://localhost:8000/docs`.

5. **Run Backend Tests**:
   ```bash
   pytest backend/tests/test_backend.py -v
   ```

---

### 2. Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the Next.js development server**:
   ```bash
   npm run dev
   ```
   Open `http://localhost:3000` in your browser.

---

## 🧪 Testing the Pipeline

1. Launch both the backend (`:8000`) and frontend (`:3000`).
2. Navigate to `http://localhost:3000`.
3. Upload:
   - **Photo 1**: A clear, well-lit portrait photo of your face.
   - **Photo 2**: A full-body photo showing clothing or silhouette.
4. Click **"Run Color & Style Analysis"**.
5. View your detected Season, ITA score, undertone, contrasting swatches, outfit moodboard, and shopping items!

---

## 📜 License

This project is licensed under the MIT License.
