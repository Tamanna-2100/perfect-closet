"use client";

import React from "react";
import { InspirationPin } from "@/types";
import { ExternalLink } from "lucide-react";

interface InspirationGridProps {
  pins: InspirationPin[];
  seasonName: string;
}

export const InspirationGrid: React.FC<InspirationGridProps> = ({ pins, seasonName }) => {
  if (!pins || pins.length === 0) return null;

  return (
    <div className="w-full space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-serif text-stone-100 font-normal">
            Outfit Inspiration
          </h2>
          <p className="text-xs text-stone-400 mt-1">
            Curated style aesthetics calibrated for {seasonName}.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {pins.map((pin) => (
          <div
            key={pin.id}
            className="group rounded-2xl bg-stone-900/40 border border-stone-800 overflow-hidden hover:border-stone-700 transition-all duration-300 flex flex-col shadow-lg"
          >
            <div className="relative aspect-[4/5] overflow-hidden bg-stone-950">
              <img
                src={pin.image_url}
                alt={pin.title}
                className="w-full h-full object-cover object-top transition-transform duration-500 group-hover:scale-105"
              />
              <div className="absolute top-3 left-3 bg-stone-950/80 backdrop-blur-sm border border-stone-800/80 text-[10px] uppercase tracking-wider text-amber-300 px-2.5 py-1 rounded-full font-mono">
                {pin.style_category}
              </div>
            </div>

            <div className="p-5 flex-1 flex flex-col justify-between">
              <div>
                <h4 className="text-sm font-medium text-stone-200 font-serif line-clamp-2">
                  {pin.title}
                </h4>
                <p className="text-xs text-stone-400 mt-2 font-light line-clamp-2">
                  {pin.description}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-stone-800/60 flex items-center justify-between">
                <span className="text-[11px] text-stone-500 font-mono">Pinterest Look</span>
                <a
                  href={pin.pin_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-xs text-amber-400 hover:text-amber-300 font-medium flex items-center gap-1 transition-colors"
                >
                  Explore <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
