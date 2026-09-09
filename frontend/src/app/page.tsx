"use client";

import React, { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { ImageUploadZone } from "@/components/ImageUploadZone";
import { AnalysisLoading } from "@/components/AnalysisLoading";
import { SeasonHero } from "@/components/SeasonHero";
import { PaletteViewer } from "@/components/PaletteViewer";
import { InspirationGrid } from "@/components/InspirationGrid";
import { ProductCatalog } from "@/components/ProductCatalog";
import { AnalysisResponse } from "@/types";
import { AlertCircle, ArrowLeft, RotateCcw } from "lucide-react";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [analysis, setAnalysis] = useState<AnalysisResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleAnalyze = async (faceFile: File, bodyFile: File | null) => {
    setIsLoading(true);
    setErrorMessage(null);

    const formData = new FormData();
    formData.append("face_image", faceFile);
    if (bodyFile) {
      formData.append("body_image", bodyFile);
    }

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `Server responded with status ${response.status}`);
      }

      const data: AnalysisResponse = await response.json();
      setAnalysis(data);
      // Smooth scroll to top of results
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err: any) {
      setErrorMessage(
        err.message || "Failed to analyze photos. Please ensure the backend server is running."
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setAnalysis(null);
    setErrorMessage(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    <div className="min-h-screen bg-stone-950 text-stone-100 flex flex-col font-sans selection:bg-amber-500/30 selection:text-amber-200">
      <Navbar hasAnalysis={!!analysis} onReset={handleReset} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        {errorMessage && (
          <div className="max-w-2xl mx-auto mb-8 p-4 rounded-2xl bg-rose-950/40 border border-rose-900/60 text-rose-300 text-xs flex items-center gap-3">
            <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
            <span className="flex-1">{errorMessage}</span>
            <button
              onClick={() => setErrorMessage(null)}
              className="text-rose-400 hover:text-rose-200 text-xs font-mono font-medium"
            >
              Dismiss
            </button>
          </div>
        )}

        {isLoading ? (
          <div className="py-16 flex items-center justify-center">
            <AnalysisLoading />
          </div>
        ) : analysis ? (
          <div className="space-y-12 animate-in fade-in duration-500">
            {/* Top Back / Navigation Bar */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-stone-800/60">
              <button
                onClick={handleReset}
                className="inline-flex items-center gap-2.5 px-4 py-2.5 rounded-xl bg-stone-900/90 hover:bg-stone-800 border border-stone-800 hover:border-stone-700 text-stone-200 hover:text-white text-sm font-medium transition-all shadow-lg hover:shadow-stone-900/50 group w-fit"
                title="Return to photo upload screen to analyze different photos"
              >
                <ArrowLeft className="w-4 h-4 text-amber-400 transition-transform group-hover:-translate-x-1" />
                <span>Back to Upload Photos</span>
              </button>

              <div className="flex items-center gap-3 text-xs text-stone-400 font-mono">
                <span className="hidden md:inline-block">
                  Current Result: <strong className="text-amber-300 font-normal">{analysis.season.season_name}</strong>
                </span>
                <span className="hidden md:inline-block text-stone-600">•</span>
                <button
                  onClick={handleReset}
                  className="text-stone-400 hover:text-amber-300 transition-colors flex items-center gap-1.5"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Analyze New Photos</span>
                </button>
              </div>
            </div>

            <SeasonHero
              season={analysis.season}
              features={analysis.features}
              onReset={handleReset}
            />

            <PaletteViewer season={analysis.season} />

            <InspirationGrid
              pins={analysis.inspiration}
              seasonName={analysis.season.season_name}
            />

            <ProductCatalog products={analysis.products} />
          </div>
        ) : (
          <div className="py-6 sm:py-10">
            <ImageUploadZone onAnalyze={handleAnalyze} isLoading={isLoading} />
          </div>
        )}
      </main>

      <footer className="border-t border-stone-900 py-8 bg-stone-950 text-center text-xs text-stone-500">
        <div className="max-w-7xl mx-auto px-4">
          <p className="tracking-wide">
            Perfect Closet • Deterministic Colorimetry &amp; 12-Season Color Analysis Engine
          </p>
          <p className="mt-1 text-[11px] text-stone-600 font-mono">
            Pure CIELAB &amp; ITA Computation — No Generative Hallucinations
          </p>
        </div>
      </footer>
    </div>
  );
}
