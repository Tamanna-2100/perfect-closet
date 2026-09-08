"use client";

import React, { useState, useRef } from "react";
import { UploadCloud, X, Camera, Sparkles, Image as ImageIcon } from "lucide-react";

interface ImageUploadZoneProps {
  onAnalyze: (faceFile: File, bodyFile: File | null) => void;
  isLoading: boolean;
}

export const ImageUploadZone: React.FC<ImageUploadZoneProps> = ({ onAnalyze, isLoading }) => {
  const [faceFile, setFaceFile] = useState<File | null>(null);
  const [facePreview, setFacePreview] = useState<string | null>(null);
  const [bodyFile, setBodyFile] = useState<File | null>(null);
  const [bodyPreview, setBodyPreview] = useState<string | null>(null);
  const [dragOverFace, setDragOverFace] = useState(false);
  const [dragOverBody, setDragOverBody] = useState(false);

  const faceInputRef = useRef<HTMLInputElement>(null);
  const bodyInputRef = useRef<HTMLInputElement>(null);

  const handleFaceSelect = (file: File) => {
    if (!file.type.startsWith("image/")) return;
    setFaceFile(file);
    setFacePreview(URL.createObjectURL(file));
  };

  const handleBodySelect = (file: File) => {
    if (!file.type.startsWith("image/")) return;
    setBodyFile(file);
    setBodyPreview(URL.createObjectURL(file));
  };

  const loadSampleFace = async () => {
    // Generate a high quality synthetic demo canvas face for instant evaluation
    const canvas = document.createElement("canvas");
    canvas.width = 300;
    canvas.height = 300;
    const ctx = canvas.getContext("2d");
    if (ctx) {
      // Soft studio gradient background
      const bgGrad = ctx.createLinearGradient(0, 0, 300, 300);
      bgGrad.addColorStop(0, "#2b2d42");
      bgGrad.addColorStop(1, "#1e1e24");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, 300, 300);

      // Hair
      ctx.fillStyle = "#1a1412";
      ctx.beginPath();
      ctx.arc(150, 140, 95, 0, Math.PI * 2);
      ctx.fill();

      // Face oval (cool porcelain tone)
      ctx.fillStyle = "#e8c3b9";
      ctx.beginPath();
      ctx.ellipse(150, 160, 65, 80, 0, 0, Math.PI * 2);
      ctx.fill();

      // Forehead highlight
      ctx.fillStyle = "#edd2c9";
      ctx.beginPath();
      ctx.ellipse(150, 130, 35, 25, 0, 0, Math.PI * 2);
      ctx.fill();

      // Eyes & Irises
      ctx.fillStyle = "#2c2a29";
      ctx.beginPath();
      ctx.arc(125, 155, 9, 0, Math.PI * 2);
      ctx.arc(175, 155, 9, 0, Math.PI * 2);
      ctx.fill();

      ctx.fillStyle = "#1e3d59"; // Deep sapphire iris
      ctx.beginPath();
      ctx.arc(125, 155, 5, 0, Math.PI * 2);
      ctx.arc(175, 155, 5, 0, Math.PI * 2);
      ctx.fill();

      // Cheeks (rosy flush)
      ctx.fillStyle = "rgba(220, 140, 140, 0.35)";
      ctx.beginPath();
      ctx.arc(115, 185, 18, 0, Math.PI * 2);
      ctx.arc(185, 185, 18, 0, Math.PI * 2);
      ctx.fill();
    }

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], "sample_studio_portrait.png", { type: "image/png" });
        handleFaceSelect(file);
      }
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!faceFile) return;
    onAnalyze(faceFile, bodyFile);
  };

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="text-center mb-10">
        <h2 className="text-3xl sm:text-4xl font-serif text-stone-100 font-normal tracking-wide">
          Unlock Your Seasonal Palette
        </h2>
        <p className="mt-3 text-sm text-stone-400 max-w-xl mx-auto font-light leading-relaxed">
          Upload an illuminated close-up face portrait. Our deterministic computer vision engine isolates facial skin, hair, and iris pigments in CIELAB space to uncover your 12-season color archetype.
        </p>
        <div className="mt-4 flex items-center justify-center gap-3">
          <button
            type="button"
            onClick={loadSampleFace}
            className="inline-flex items-center gap-2 text-xs font-medium text-amber-300 hover:text-amber-200 bg-amber-950/40 hover:bg-amber-900/50 border border-amber-800/60 px-4 py-2 rounded-full transition-all duration-200 shadow-sm"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Try with Sample Studio Portrait
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* 1. Face Portrait Card */}
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragOverFace(true);
            }}
            onDragLeave={() => setDragOverFace(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOverFace(false);
              if (e.dataTransfer.files[0]) handleFaceSelect(e.dataTransfer.files[0]);
            }}
            className={`relative rounded-2xl border-2 border-dashed p-6 transition-all duration-200 flex flex-col items-center justify-center min-h-[300px] text-center ${
              dragOverFace
                ? "border-amber-400 bg-amber-950/20"
                : faceFile
                ? "border-stone-700 bg-stone-900/40"
                : "border-stone-800 bg-stone-900/20 hover:border-stone-700 hover:bg-stone-900/30"
            }`}
          >
            <input
              type="file"
              ref={faceInputRef}
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                if (e.target.files?.[0]) handleFaceSelect(e.target.files[0]);
              }}
            />

            {facePreview ? (
              <div className="relative w-full h-64 rounded-xl overflow-hidden group">
                <img
                  src={facePreview}
                  alt="Face preview"
                  className="w-full h-full object-cover rounded-xl"
                />
                <button
                  type="button"
                  onClick={() => {
                    setFaceFile(null);
                    setFacePreview(null);
                  }}
                  className="absolute top-3 right-3 p-1.5 rounded-full bg-stone-950/80 text-stone-300 hover:text-white hover:bg-rose-900/80 transition-all shadow-md"
                >
                  <X className="w-4 h-4" />
                </button>
                <div className="absolute bottom-2 left-2 right-2 px-3 py-1.5 bg-stone-950/80 backdrop-blur-sm rounded-lg text-[11px] text-stone-300 flex items-center justify-between">
                  <span>Portrait Loaded</span>
                  <span className="text-emerald-400 font-medium">Ready</span>
                </div>
              </div>
            ) : (
              <div
                onClick={() => faceInputRef.current?.click()}
                className="cursor-pointer flex flex-col items-center p-4"
              >
                <div className="w-14 h-14 rounded-full bg-stone-800/80 flex items-center justify-center mb-4 text-amber-300">
                  <Camera className="w-6 h-6" />
                </div>
                <h3 className="text-sm font-medium text-stone-200 uppercase tracking-wider">
                  Illuminated Face Portrait
                </h3>
                <span className="text-[11px] text-amber-400/90 font-mono mt-0.5 font-semibold">
                  * Required
                </span>
                <p className="text-xs text-stone-400 mt-2 max-w-xs">
                  Even natural light, no heavy filters or sunglasses. Look directly into the camera.
                </p>
                <span className="mt-4 text-xs text-amber-300/80 underline decoration-amber-500/50 underline-offset-4 font-medium">
                  Browse file or drag here
                </span>
              </div>
            )}
          </div>

          {/* 2. Full-Body Photo Card */}
          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragOverBody(true);
            }}
            onDragLeave={() => setDragOverBody(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOverBody(false);
              if (e.dataTransfer.files[0]) handleBodySelect(e.dataTransfer.files[0]);
            }}
            className={`relative rounded-2xl border-2 border-dashed p-6 transition-all duration-200 flex flex-col items-center justify-center min-h-[300px] text-center ${
              dragOverBody
                ? "border-indigo-400 bg-indigo-950/20"
                : bodyFile
                ? "border-stone-700 bg-stone-900/40"
                : "border-stone-800 bg-stone-900/20 hover:border-stone-700 hover:bg-stone-900/30"
            }`}
          >
            <input
              type="file"
              ref={bodyInputRef}
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                if (e.target.files?.[0]) handleBodySelect(e.target.files[0]);
              }}
            />

            {bodyPreview ? (
              <div className="relative w-full h-64 rounded-xl overflow-hidden group">
                <img
                  src={bodyPreview}
                  alt="Body preview"
                  className="w-full h-full object-cover rounded-xl"
                />
                <button
                  type="button"
                  onClick={() => {
                    setBodyFile(null);
                    setBodyPreview(null);
                  }}
                  className="absolute top-3 right-3 p-1.5 rounded-full bg-stone-950/80 text-stone-300 hover:text-white hover:bg-rose-900/80 transition-all shadow-md"
                >
                  <X className="w-4 h-4" />
                </button>
                <div className="absolute bottom-2 left-2 right-2 px-3 py-1.5 bg-stone-950/80 backdrop-blur-sm rounded-lg text-[11px] text-stone-300 flex items-center justify-between">
                  <span>Full-Body Loaded</span>
                  <span className="text-indigo-400 font-medium">Style Context Added</span>
                </div>
              </div>
            ) : (
              <div
                onClick={() => bodyInputRef.current?.click()}
                className="cursor-pointer flex flex-col items-center p-4"
              >
                <div className="w-14 h-14 rounded-full bg-stone-800/80 flex items-center justify-center mb-4 text-stone-400">
                  <ImageIcon className="w-6 h-6" />
                </div>
                <h3 className="text-sm font-medium text-stone-200 uppercase tracking-wider">
                  Full-Body Outfit Photo
                </h3>
                <span className="text-[11px] text-stone-400 font-mono mt-0.5">
                  Optional (Style Silhouette)
                </span>
                <p className="text-xs text-stone-400 mt-2 max-w-xs">
                  Helps calibrate garment proportions and overall visual contrast against your silhouette.
                </p>
                <span className="mt-4 text-xs text-stone-300/80 underline decoration-stone-600 underline-offset-4 font-medium">
                  Browse file or drag here
                </span>
              </div>
            )}
          </div>
        </div>

        <div className="flex justify-center pt-2">
          <button
            type="submit"
            disabled={!faceFile || isLoading}
            className={`px-8 py-4 rounded-full text-xs font-semibold uppercase tracking-widest transition-all duration-300 flex items-center gap-3 shadow-xl ${
              !faceFile || isLoading
                ? "bg-stone-800 text-stone-500 cursor-not-allowed border border-stone-700/50"
                : "bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600 text-white hover:brightness-110 hover:shadow-amber-500/20 active:scale-[0.98]"
            }`}
          >
            <Sparkles className="w-4 h-4" />
            {isLoading ? "Analyzing Chromatic Profile..." : "Analyze My Color Palette"}
          </button>
        </div>
      </form>
    </div>
  );
};
