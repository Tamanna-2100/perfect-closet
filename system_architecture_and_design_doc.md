# System Architecture & Design Document (SDD)

## 1. Overview

This system analyzes user appearance from two uploaded images and returns a seasonal color palette, visual outfit inspiration, and retail product suggestions. The design emphasizes deterministic computer vision and mathematical analysis over generative AI for core classification tasks.

## 2. System Purpose

The platform allows a user to:

- upload one full-body photo and one illuminated close-up face photo;
- receive an automated seasonal color analysis;
- view outfit inspiration based on the identified palette; and
- discover current retail products matching the selected style attributes.

## 3. High-Level System Architecture

### 3.1 System Flow

```text
User Client (Web)
        |
        | 1. Upload 2 photos
        v
FastAPI Core Engine
        |
        | - MediaPipe face/hair/iris isolation
        | - RGB -> CIELAB -> ITA conversion
        | - 12-season palette classification
        v
Season Palette Result
        |
        | 2. Return palette + style context
        v
SERP Service Layer
        |-- Pinterest inspiration retrieval
        |-- Google Shopping product retrieval
        v
User Client (Web)
```

### 3.2 Core Components

- Frontend: Next.js with TypeScript, Tailwind CSS, Lucide Icons, and Shadcn UI.
- Backend: FastAPI using Python 3.11+, Pydantic, OpenCV, MediaPipe, NumPy, and Scikit-learn.
- Data and Cache: PostgreSQL (local or Supabase) for storing user profiles and palettes; Redis for caching SERP API responses.

## 4. Component Breakdown

### 4.1 Frontend Layer

Responsibilities:
- collect user image uploads;
- display the generated season palette;
- render outfit inspiration cards and retail product results; and
- allow user selection of garment attributes such as color, cut, and type.

### 4.2 Backend Processing Layer

Responsibilities:
- ingest and validate input images;
- isolate relevant facial and hair regions;
- compute color values and seasonal classification metrics; and
- prepare structured queries for external inspiration and shopping services.

### 4.3 External Service Layer

Responsibilities:
- retrieve Pinterest-based outfit inspiration content; and
- retrieve current Google Shopping product listings with merchant URLs.

## 5. Software Requirements Document (SRD)

### 5.1 Functional Requirements

- FR-1 Image Ingestion: The system shall accept two images per user, including one full-body photo and one illuminated close-up face photo, in standard JPEG or PNG format.
- FR-2 Automated Region Extraction: The system shall isolate skin pixels (cheek/forehead), hair pixels, and iris pixels without manual masking.
- FR-3 Deterministic Palette Classification: The system shall compute $L^*$, $a^*$, and $b^*$ values and Individual Typology Angle (ITA) to map users to one of 12 seasonal palettes such as Deep Winter or Soft Summer.
- FR-4 External Inspiration Retrieval: The system shall construct contextual search queries and retrieve structured inspiration pins using Pinterest-based interfaces.
- FR-5 E-Commerce Link Match: The system shall use user-selected garment properties such as color, cut, and type to retrieve current Google Shopping product listings with direct merchant URLs.

### 5.2 Non-Functional Requirements

- NFR-1 Determinism: Face analysis logic shall produce identical season results for identical input images.
- NFR-2 Latency: Color extraction and classification shall complete in less than 1,500 ms on server CPU.
- NFR-3 Token Conservation: Generative AI APIs shall not be used for tasks that can be solved through mathematical or computer vision operations.

## 6. Design Considerations

- The analysis pipeline should prioritize deterministic outputs and clear numerical thresholds.
- The system should minimize external API costs through caching and selective querying.
- The design should keep the core classification logic independent from generative AI dependencies to preserve performance and consistency.