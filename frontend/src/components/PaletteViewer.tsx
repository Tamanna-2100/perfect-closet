"use client";

import React, { useState } from "react";
import { ColorSwatch, SeasonResult } from "@/types";
import { Check, Copy, CheckCircle2, XCircle, Lightbulb } from "lucide-react";

interface PaletteViewerProps {
  season: SeasonResult;
}

export const PaletteViewer: React.FC<PaletteViewerProps> = ({ season }) => {
  const [copiedHex, setCopiedHex] = useState<string | null>(null);

  const copyHex = (hex: string) => {
    navigator.clipboard.writeText(hex);
    setCopiedHex(hex);
    setTimeout(() => setCopiedHex(null), 1800);
  };

  return (
    <div className="w-full space-y-12">
      {/* 1. Primary Palette Swatches */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-serif text-stone-100 font-normal">
              Signature Palette Swatches
            </h2>
            <p className="text-xs text-stone-400 mt-1">
              Harmonized in CIELAB color space. Click any swatch to copy its hexadecimal code.
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
          {season.palette.map((swatch, idx) => (
            <div
              key={idx}
              onClick={() => copyHex(swatch.hex)}
              className="group cursor-pointer rounded-2xl bg-stone-900/50 border border-stone-800 p-3 hover:border-stone-700 transition-all duration-200 hover:-translate-y-1 shadow-md"
            >
              <div
                className="w-full h-24 rounded-xl shadow-inner relative overflow-hidden transition-transform duration-200 group-hover:scale-[1.02]"
                style={{ backgroundColor: swatch.hex }}
              >
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors flex items-center justify-center">
                  <span className="opacity-0 group-hover:opacity-100 transition-opacity bg-stone-950/80 text-white text-[11px] px-2.5 py-1 rounded-full font-mono flex items-center gap-1 shadow">
                    {copiedHex === swatch.hex ? (
                      <>
                        <Check className="w-3 h-3 text-emerald-400" />
                        Copied
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" />
                        Copy
                      </>
                    )}
                  </span>
                </div>
              </div>
              <div className="mt-3">
                <div className="text-xs font-medium text-stone-200 truncate font-serif">
                  {swatch.name}
                </div>
                <div className="flex items-center justify-between mt-1 text-[11px] text-stone-400 font-mono">
                  <span>{swatch.hex}</span>
                  <span className="text-stone-500">L*{swatch.L.toFixed(0)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 2. Complementary Accents */}
      <div>
        <h3 className="text-lg font-serif text-stone-200 mb-4">
          Complementary Accent Tones
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {season.complementary_colors.map((swatch, idx) => (
            <div
              key={idx}
              onClick={() => copyHex(swatch.hex)}
              className="group cursor-pointer rounded-xl bg-stone-900/30 border border-stone-800/80 p-3 hover:border-stone-700 transition-all duration-200 flex items-center gap-3"
            >
              <div
                className="w-10 h-10 rounded-lg shrink-0 border border-stone-800 shadow-sm"
                style={{ backgroundColor: swatch.hex }}
              />
              <div className="min-w-0">
                <div className="text-xs text-stone-200 truncate font-medium">{swatch.name}</div>
                <div className="text-[10px] text-stone-400 font-mono">{swatch.hex}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 3. Guidelines & Wardrobe Strategy */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Colors to embrace */}
        <div className="rounded-2xl bg-stone-900/30 border border-stone-800/80 p-6">
          <div className="flex items-center gap-2 text-emerald-400 text-sm font-medium mb-4">
            <CheckCircle2 className="w-4 h-4" />
            <span>Colors to Embrace</span>
          </div>
          <ul className="space-y-2 text-xs text-stone-300 font-light">
            {season.palette.slice(0, 5).map((color, idx) => (
              <li key={idx} className="flex items-center gap-2">
                <span
                  className="w-2.5 h-2.5 rounded-full inline-block shrink-0"
                  style={{ backgroundColor: color.hex }}
                />
                <span>{color.name}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Colors to avoid */}
        <div className="rounded-2xl bg-stone-900/30 border border-stone-800/80 p-6">
          <div className="flex items-center gap-2 text-rose-400 text-sm font-medium mb-4">
            <XCircle className="w-4 h-4" />
            <span>Colors to Avoid</span>
          </div>
          <ul className="space-y-2 text-xs text-stone-400 font-light">
            {season.colors_to_avoid.map((color, idx) => (
              <li key={idx} className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-rose-500/80 shrink-0" />
                <span>{color}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Styling tips */}
        <div className="rounded-2xl bg-stone-900/30 border border-stone-800/80 p-6">
          <div className="flex items-center gap-2 text-amber-400 text-sm font-medium mb-4">
            <Lightbulb className="w-4 h-4" />
            <span>Haute Styling Rules</span>
          </div>
          <ul className="space-y-2.5 text-xs text-stone-300 font-light">
            {season.styling_tips.map((tip, idx) => (
              <li key={idx} className="leading-relaxed">
                • {tip}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};
