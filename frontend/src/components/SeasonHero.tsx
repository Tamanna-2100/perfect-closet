"use client";

import React from "react";
import { SeasonResult, ExtractedFeatures } from "@/types";
import { Sparkles, Compass, Eye, Scissors, RotateCcw } from "lucide-react";

interface SeasonHeroProps {
  season: SeasonResult;
  features: ExtractedFeatures;
  onReset: () => void;
}

export const SeasonHero: React.FC<SeasonHeroProps> = ({ season, features, onReset }) => {
  return (
    <div className="w-full bg-stone-900/40 border border-stone-800 rounded-3xl p-6 sm:p-10 backdrop-blur-md shadow-2xl relative overflow-hidden">
      {/* Subtle chromatic ambient glow based on season family */}
      <div className="absolute -top-24 -right-24 w-96 h-96 rounded-full bg-gradient-to-br from-amber-500/10 via-rose-500/10 to-indigo-500/10 blur-3xl pointer-events-none" />

      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-8 relative z-10">
        <div className="max-w-2xl">
          <div className="flex items-center gap-3 flex-wrap mb-4">
            <span className="text-xs uppercase tracking-widest font-mono text-amber-400 bg-amber-950/50 border border-amber-800/60 px-3 py-1 rounded-full flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              {season.season_family} Archetype
            </span>
            <span className="text-xs uppercase tracking-wider text-stone-300 bg-stone-800/60 px-3 py-1 rounded-full border border-stone-700/60">
              {season.undertone} Undertone
            </span>
            <span className="text-xs uppercase tracking-wider text-stone-300 bg-stone-800/60 px-3 py-1 rounded-full border border-stone-700/60">
              {season.value} Value
            </span>
            <span className="text-xs uppercase tracking-wider text-stone-300 bg-stone-800/60 px-3 py-1 rounded-full border border-stone-700/60">
              {season.chroma}
            </span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-serif tracking-tight text-stone-100 font-normal">
            {season.season_name}
          </h1>

          <p className="mt-2 text-base text-amber-200/80 italic font-serif">
            &ldquo;{season.tagline}&rdquo;
          </p>

          <p className="mt-4 text-sm text-stone-300 font-light leading-relaxed">
            {season.description}
          </p>

          <div className="mt-6 flex flex-wrap items-center gap-2">
            <span className="text-xs text-stone-400 uppercase tracking-wider font-mono mr-2">
              Flattering Metals:
            </span>
            {season.recommended_metals.map((metal, idx) => (
              <span
                key={idx}
                className="text-xs text-stone-200 bg-stone-950/80 border border-stone-800 px-3 py-1 rounded-lg shadow-sm"
              >
                {metal}
              </span>
            ))}
          </div>
        </div>

        {/* Feature telemetry block */}
        <div className="w-full lg:w-80 bg-stone-950/70 border border-stone-800/90 rounded-2xl p-5 shadow-lg">
          <div className="flex items-center justify-between pb-3 border-b border-stone-800">
            <span className="text-xs font-mono uppercase tracking-wider text-stone-400">
              Colorimetry Metrics
            </span>
            <button
              onClick={onReset}
              className="text-xs text-amber-400/90 hover:text-amber-200 bg-amber-950/40 hover:bg-amber-950/70 border border-amber-800/60 px-2.5 py-1 rounded-lg flex items-center gap-1.5 transition-all shadow-sm group"
              title="Upload new photos and retest"
            >
              <RotateCcw className="w-3 h-3 transition-transform group-hover:-rotate-90" />
              Retest
            </button>
          </div>

          <div className="mt-4 space-y-3">
            {/* Skin coordinates */}
            <div className="flex items-center justify-between text-xs">
              <span className="text-stone-400 flex items-center gap-1.5">
                <span
                  className="w-3 h-3 rounded-full border border-stone-600 inline-block"
                  style={{ backgroundColor: features.skin.hex_code }}
                />
                Skin Tone (L*, a*, b*)
              </span>
              <span className="font-mono text-stone-200">
                {features.skin.L.toFixed(0)}, {features.skin.a.toFixed(0)}, {features.skin.b.toFixed(0)}
              </span>
            </div>

            {/* Hair coordinates */}
            <div className="flex items-center justify-between text-xs">
              <span className="text-stone-400 flex items-center gap-1.5">
                <span
                  className="w-3 h-3 rounded-full border border-stone-600 inline-block"
                  style={{ backgroundColor: features.hair.hex_code }}
                />
                Hair Pigment
              </span>
              <span className="font-mono text-stone-200">
                L* {features.hair.L.toFixed(0)}
              </span>
            </div>

            {/* Iris coordinates */}
            <div className="flex items-center justify-between text-xs">
              <span className="text-stone-400 flex items-center gap-1.5">
                <span
                  className="w-3 h-3 rounded-full border border-stone-600 inline-block"
                  style={{ backgroundColor: features.iris.hex_code }}
                />
                Iris Pigment
              </span>
              <span className="font-mono text-stone-200">
                L* {features.iris.L.toFixed(0)}
              </span>
            </div>

            {/* ITA angle */}
            <div className="flex items-center justify-between text-xs pt-2 border-t border-stone-900">
              <span className="text-stone-400">Typology Angle (ITA)</span>
              <span className="font-mono text-amber-300 font-medium">
                {features.skin.ita.toFixed(1)}°
              </span>
            </div>

            {/* Contrast Ratio */}
            <div className="flex items-center justify-between text-xs">
              <span className="text-stone-400">Visual Contrast</span>
              <span className="font-mono text-emerald-400 font-medium">
                {features.contrast_ratio.toFixed(0)}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
