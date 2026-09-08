"use client";

import React, { useEffect, useState } from "react";
import { Loader2, ScanFace, Palette, Compass, Sparkles } from "lucide-react";

const STEPS = [
  { icon: ScanFace, label: "Isolating facial contour, cheeks & iris landmarks" },
  { icon: Palette, label: "Translating BGR pixels to standard CIELAB space" },
  { icon: Compass, label: "Computing Individual Typology Angle (ITA) & Chroma" },
  { icon: Sparkles, label: "Mapping to 12-season chromatic centroids" },
];

export const AnalysisLoading: React.FC = () => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 650);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-lg mx-auto p-8 rounded-3xl bg-stone-900/60 border border-stone-800 backdrop-blur-xl text-center shadow-2xl">
      <div className="relative w-20 h-20 mx-auto mb-6 flex items-center justify-center">
        <div className="absolute inset-0 rounded-full border-2 border-stone-800 border-t-amber-400 animate-spin" />
        <div className="w-14 h-14 rounded-full bg-stone-950 flex items-center justify-center shadow-inner">
          <Loader2 className="w-6 h-6 text-amber-300 animate-spin" />
        </div>
      </div>

      <h3 className="text-xl font-serif text-stone-100 tracking-wide">
        Analyzing Chromatic Profile
      </h3>
      <p className="text-xs text-stone-400 mt-1 font-light">
        Running deterministic mathematical colorimetry...
      </p>

      <div className="mt-8 space-y-3.5 text-left">
        {STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <div
              key={idx}
              className={`flex items-center gap-3.5 p-3 rounded-xl transition-all duration-300 ${
                isCurrent
                  ? "bg-amber-950/30 border border-amber-800/50 text-amber-200"
                  : isDone
                  ? "text-stone-300 opacity-80"
                  : "text-stone-600 opacity-40"
              }`}
            >
              <div
                className={`w-7 h-7 rounded-full flex items-center justify-center text-xs ${
                  isDone
                    ? "bg-emerald-950/80 text-emerald-400 border border-emerald-800/60"
                    : isCurrent
                    ? "bg-amber-500/20 text-amber-300 border border-amber-500/50 animate-pulse"
                    : "bg-stone-800 text-stone-500"
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
              </div>
              <span className="text-xs font-medium tracking-wide">{step.label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
